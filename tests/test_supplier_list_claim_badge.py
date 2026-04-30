"""Integration tests for the claimed-PP badge on /products/supplier?match_state=none.

When a supplier product (SP) without any match shares a brand+normalized model
with a catalog PP that's already confirmed/manual to a *different* supplier,
operators should see a "Уже у [Supplier]" badge — manually matching this SP is
pointless because the slot is taken.
"""

from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier import Supplier
from app.models.supplier_product import SupplierProduct


def _seed_two_suppliers(session):
    s1 = Supplier(name="Maresto", feed_url="http://m.xml",
                  discount_percent=0, is_enabled=True)
    s2 = Supplier(name="РП Україна", feed_url="http://rp.xml",
                  discount_percent=0, is_enabled=True)
    session.add_all([s1, s2])
    session.flush()
    return s1, s2


def test_sp_with_model_matching_another_supplier_pp_gets_badge(client, session):
    """SP brand+model collides with PP confirmed to a different supplier
    → badge "Уже у Maresto" is rendered next to "Без матча"."""
    s1, s2 = _seed_two_suppliers(session)
    pp = PromProduct(
        external_id="P1",
        name="Шафа Unox XEVC0511EZRMLP лінія ZERO",
        brand="Unox", price=400000,
    )
    session.add(pp)
    sp_claimer = SupplierProduct(
        supplier_id=s1.id, external_id="M1",
        name="Unox XEVC-0511-EZRM-LP пароконвектомат",
        brand="Unox", price_cents=400000, available=True,
    )
    sp_unmatched = SupplierProduct(
        supplier_id=s2.id, external_id="R1",
        name="Пароконвектомат UNOX XEVC-0511-EZRM-LP",
        brand="Unox", price_cents=400000, available=True,
    )
    session.add_all([sp_claimer, sp_unmatched])
    session.flush()
    session.add(ProductMatch(
        supplier_product_id=sp_claimer.id,
        prom_product_id=pp.id,
        status="confirmed",
        score=1.0,
    ))
    session.commit()

    resp = client.get(f"/products/supplier?supplier_id={s2.id}&match_state=none")
    assert resp.status_code == 200
    body = resp.data.decode("utf-8")
    assert "Без матча" in body
    assert "Уже у Maresto" in body


def test_sp_without_extractable_model_no_badge(client, session):
    """SP whose name yields no model code → no badge even if a PP is claimed."""
    s1, s2 = _seed_two_suppliers(session)
    pp = PromProduct(external_id="P1", name="Unox без модели",
                     brand="Unox", price=100000)
    session.add(pp)
    sp_claimer = SupplierProduct(
        supplier_id=s1.id, external_id="M1",
        name="Unox без модели прибор", brand="Unox",
        price_cents=100000, available=True,
    )
    sp_unmatched = SupplierProduct(
        supplier_id=s2.id, external_id="R1",
        name="Пароконвектомат Unox простой",
        brand="Unox", price_cents=100000, available=True,
    )
    session.add_all([sp_claimer, sp_unmatched])
    session.flush()
    session.add(ProductMatch(
        supplier_product_id=sp_claimer.id,
        prom_product_id=pp.id,
        status="confirmed",
        score=1.0,
    ))
    session.commit()

    resp = client.get(f"/products/supplier?supplier_id={s2.id}&match_state=none")
    body = resp.data.decode("utf-8")
    assert "Уже у" not in body


def test_sp_whose_pp_not_claimed_no_badge(client, session):
    """Catalog PP exists with same model but no confirmed/manual match → no badge."""
    s1, s2 = _seed_two_suppliers(session)
    pp = PromProduct(
        external_id="P1",
        name="Шафа Unox XEVC0511EZRMLP лінія ZERO",
        brand="Unox", price=400000,
    )
    session.add(pp)
    sp_unmatched = SupplierProduct(
        supplier_id=s2.id, external_id="R1",
        name="Пароконвектомат UNOX XEVC-0511-EZRM-LP",
        brand="Unox", price_cents=400000, available=True,
    )
    session.add(sp_unmatched)
    session.commit()

    resp = client.get(f"/products/supplier?supplier_id={s2.id}&match_state=none")
    body = resp.data.decode("utf-8")
    assert "Уже у" not in body


def test_same_supplier_claim_no_badge(client, session):
    """SP whose brand+model PP is claimed by the SAME supplier — no badge,
    because the operator wouldn't be steered away from their own catalog slot."""
    s1, _ = _seed_two_suppliers(session)
    pp = PromProduct(
        external_id="P1",
        name="Шафа Unox XEVC0511EZRMLP лінія ZERO",
        brand="Unox", price=400000,
    )
    session.add(pp)
    sp_claimer = SupplierProduct(
        supplier_id=s1.id, external_id="M1",
        name="Unox XEVC-0511-EZRM-LP пароконвектомат",
        brand="Unox", price_cents=400000, available=True,
    )
    sp_unmatched_same = SupplierProduct(
        supplier_id=s1.id, external_id="M2",
        name="Пароконвектомат UNOX XEVC-0511-EZRM-LP",
        brand="Unox", price_cents=400000, available=True,
    )
    session.add_all([sp_claimer, sp_unmatched_same])
    session.flush()
    session.add(ProductMatch(
        supplier_product_id=sp_claimer.id,
        prom_product_id=pp.id,
        status="confirmed",
        score=1.0,
    ))
    session.commit()

    resp = client.get(f"/products/supplier?supplier_id={s1.id}&match_state=none")
    body = resp.data.decode("utf-8")
    assert "Уже у" not in body
