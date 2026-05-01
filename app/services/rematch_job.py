"""In-memory background job runner for `POST /matches/rematch`.

The matcher takes minutes on the full catalog. A blocking HTTP request can
time out in the browser/proxy before it finishes; that leaves the UI with no
feedback while the job keeps running server-side. This module runs the job
in a daemon thread and exposes polling endpoints so the UI can show progress.

Only one rematch can run at a time (serialized with a lock). Jobs older than
1 hour after they finish are garbage-collected.
"""

from __future__ import annotations

import json
import threading
import time
import uuid
from datetime import datetime

from app.extensions import db
from app.models.audit_log import AuditLog
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct

_LOCK = threading.Lock()
_JOBS: dict[str, dict] = {}
_JOB_TTL_SECONDS = 3600


def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _gc_old_jobs_locked() -> None:
    now = time.time()
    stale = [
        jid for jid, j in _JOBS.items()
        if j["status"] in ("done", "error")
        and (now - j.get("finished_ts", 0)) > _JOB_TTL_SECONDS
    ]
    for jid in stale:
        _JOBS.pop(jid, None)


def get_job(job_id: str) -> dict | None:
    with _LOCK:
        j = _JOBS.get(job_id)
        return _public_copy(j) if j else None


def get_active_job() -> dict | None:
    with _LOCK:
        for j in _JOBS.values():
            if j["status"] in ("pending", "running"):
                return _public_copy(j)
        return None


def _public_copy(j: dict) -> dict:
    # Deep-copy the nested progress dict so callers can't mutate our state.
    return {
        **j,
        "progress": {k: dict(v) for k, v in j.get("progress", {}).items()},
        "result": dict(j["result"]) if j.get("result") else None,
    }


def create_job(scope_raw, user_id: int | None, user_name: str | None) -> tuple[str | None, dict | None]:
    """Try to create a new job. Returns (job_id, None) on success, (None, active_job)
    if another rematch is already running.
    """
    with _LOCK:
        _gc_old_jobs_locked()
        for j in _JOBS.values():
            if j["status"] in ("pending", "running"):
                return None, _public_copy(j)
        jid = uuid.uuid4().hex[:10]
        _JOBS[jid] = {
            "id": jid,
            "scope": scope_raw,
            "status": "pending",
            "phase": "queued",
            "progress": {},
            "started_at": _now_iso(),
            "finished_at": None,
            "finished_ts": 0,
            "result": None,
            "error": None,
            "backup": None,
            "user_id": user_id,
            "user_name": user_name,
        }
        return jid, None


def _set(jid: str, **fields) -> None:
    with _LOCK:
        j = _JOBS.get(jid)
        if j is not None:
            j.update(fields)


def _update_progress(jid: str, supplier_id: int, supplier_name: str, done: int, total: int) -> None:
    with _LOCK:
        j = _JOBS.get(jid)
        if j is None:
            return
        j["progress"][supplier_id] = {
            "supplier_id": supplier_id,
            "supplier_name": supplier_name,
            "done": done,
            "total": total,
        }


def start_thread(flask_app, job_id: str) -> threading.Thread:
    t = threading.Thread(target=run_job, args=(flask_app, job_id), daemon=True, name=f"rematch-{job_id}")
    t.start()
    return t


def run_job(flask_app, job_id: str) -> None:
    """Execute a rematch job in a worker thread.

    Always called inside `flask_app.app_context()` so `db.session` works.
    The session is torn down in the `finally` so it does not leak.
    """
    from scripts.backup_db import backup as _backup
    from app.services.matcher import run_matching_for_supplier

    with flask_app.app_context():
        j = get_job(job_id)
        if j is None:
            return
        user_id = j["user_id"]
        user_name = j["user_name"]
        scope_raw = j["scope"]

        try:
            _set(job_id, status="running", phase="backup")
            _backup_result = _backup()
            backup_path = str(_backup_result) if _backup_result else "skipped (postgresql)"
            _set(job_id, backup=backup_path)

            _set(job_id, phase="load_suppliers")
            if scope_raw == "all":
                suppliers = db.session.execute(
                    db.select(Supplier).where(Supplier.is_enabled == True)  # noqa: E712
                    .order_by(Supplier.id)
                ).scalars().all()
            else:
                sup = db.session.get(Supplier, int(scope_raw))
                suppliers = [sup] if sup else []

            if not suppliers:
                raise RuntimeError("Нет поставщиков в scope")

            # Seed progress with 0/total per supplier so UI knows how many and in what order.
            for sup in suppliers:
                sp_total = db.session.execute(
                    db.select(db.func.count(SupplierProduct.id))
                    .where(SupplierProduct.supplier_id == sup.id)
                ).scalar() or 0
                _update_progress(job_id, sup.id, sup.name, 0, sp_total)

            # Audit: start.
            db.session.add(AuditLog(
                user_id=user_id, user_name=user_name, action="rematch_start",
                details=json.dumps({
                    "job_id": job_id,
                    "scope": scope_raw if scope_raw == "all" else f"supplier:{scope_raw}",
                    "backup": backup_path,
                    "supplier_ids": [s.id for s in suppliers],
                }, ensure_ascii=False),
            ))
            db.session.commit()

            results = []
            total_deleted = 0
            total_created = 0

            for sup in suppliers:
                _set(job_id, phase=f"matching:{sup.name}")

                protected = db.session.execute(
                    db.select(db.func.count(ProductMatch.id))
                    .join(SupplierProduct, ProductMatch.supplier_product_id == SupplierProduct.id)
                    .where(
                        SupplierProduct.supplier_id == sup.id,
                        ProductMatch.status.in_(("confirmed", "manual")),
                    )
                ).scalar() or 0

                wipe = db.delete(ProductMatch).where(
                    ProductMatch.status == "candidate",
                    ProductMatch.supplier_product_id.in_(
                        db.select(SupplierProduct.id).where(SupplierProduct.supplier_id == sup.id)
                    ),
                ).execution_options(synchronize_session=False)
                deleted = db.session.execute(wipe).rowcount or 0
                db.session.commit()

                sup_id = sup.id
                sup_name = sup.name

                def _cb(done, total, _sid=sup_id, _sname=sup_name):
                    _update_progress(job_id, _sid, _sname, done, total)

                created = run_matching_for_supplier(sup.id, progress_cb=_cb)

                total_deleted += deleted
                total_created += created
                results.append({
                    "supplier_id": sup.id,
                    "supplier_name": sup.name,
                    "protected": protected,
                    "deleted": deleted,
                    "created": created,
                })

                # Mark supplier row as done (in case matcher returned before final cb).
                total_sp = db.session.execute(
                    db.select(db.func.count(SupplierProduct.id))
                    .where(SupplierProduct.supplier_id == sup.id)
                ).scalar() or 0
                _update_progress(job_id, sup.id, sup.name, total_sp, total_sp)

            # Safe auto-confirm pass (R1-R4): promote identical-token candidates
            # so the user sees 100% matches already confirmed after a rematch.
            _set(job_id, phase="auto_confirm")
            from scripts.bulk_auto_confirm import apply_rules as _apply_safe_rules
            auto_stats = _apply_safe_rules(apply=True, confirmed_by="rematch:bulk_auto_confirm")

            # Audit: finish.
            db.session.add(AuditLog(
                user_id=user_id, user_name=user_name, action="rematch_finish",
                details=json.dumps({
                    "job_id": job_id,
                    "scope": scope_raw if scope_raw == "all" else f"supplier:{scope_raw}",
                    "backup": backup_path,
                    "total_deleted": total_deleted,
                    "total_created": total_created,
                    "suppliers": results,
                    "auto_stats": auto_stats,
                }, ensure_ascii=False),
            ))
            db.session.commit()

            _set(
                job_id,
                status="done",
                phase="done",
                finished_at=_now_iso(),
                finished_ts=time.time(),
                result={
                    "backup": backup_path,
                    "total_deleted": total_deleted,
                    "total_created": total_created,
                    "suppliers": results,
                    "auto_stats": auto_stats,
                },
            )

        except Exception as exc:
            db.session.rollback()
            _set(
                job_id,
                status="error",
                phase="error",
                error=str(exc),
                finished_at=_now_iso(),
                finished_ts=time.time(),
            )
            try:
                db.session.add(AuditLog(
                    user_id=user_id, user_name=user_name, action="rematch_error",
                    details=json.dumps(
                        {"job_id": job_id, "error": str(exc)}, ensure_ascii=False
                    ),
                ))
                db.session.commit()
            except Exception:
                db.session.rollback()
        finally:
            db.session.remove()
