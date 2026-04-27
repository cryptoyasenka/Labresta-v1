import re
from datetime import datetime, timezone

from sqlalchemy import event

from app.extensions import db

_CYR_TO_LAT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "ґ": "g", "д": "d", "е": "e",
    "ё": "e", "є": "ye", "ж": "zh", "з": "z", "и": "i", "і": "i", "ї": "yi",
    "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p",
    "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "h", "ц": "ts",
    "ч": "ch", "ш": "sh", "щ": "sch", "ъ": "", "ы": "y", "ь": "", "э": "e",
    "ю": "yu", "я": "ya",
}


def slugify_supplier_name(name: str) -> str:
    """Transliterate Cyrillic, lowercase, keep [a-z0-9-]. Empty input → 'supplier'."""
    if not name:
        return "supplier"
    out = []
    for ch in name.lower():
        out.append(_CYR_TO_LAT.get(ch, ch))
    text = "".join(out)
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:50] or "supplier"


class Supplier(db.Model):
    __tablename__ = "suppliers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(50), nullable=False, unique=True)
    feed_url = db.Column(db.String(500), nullable=True)
    discount_percent = db.Column(db.Float, default=0.0)  # e.g. 15.0 for 15%
    eur_rate_uah = db.Column(db.Float, default=51.15, server_default="51.15")  # used for min-margin calc
    # Min margin (UAH) the dealer wants to preserve per sale. Clamp reduces the
    # base discount (per_brand / flat / auto) so margin_uah stays >= this value.
    # 0 disables the clamp.
    min_margin_uah = db.Column(db.Float, default=500.0, server_default="500.0", nullable=False)
    # Cost rate: how much we pay the supplier as fraction of their retail.
    # e.g. 0.75 means our buy-price = supplier_retail * 0.75 (supplier gives us 25% off).
    cost_rate = db.Column(db.Float, default=0.75, server_default="0.75", nullable=False)
    # flat        — use Supplier.discount_percent for every match
    # per_brand   — look up SupplierBrandDiscount by sp.brand, fallback to discount_percent
    # auto_margin — apply calculate_auto_discount (MARESTO min-margin formula)
    pricing_mode = db.Column(
        db.String(20),
        nullable=False,
        default="flat",
        server_default="flat",
    )
    column_mapping = db.Column(db.Text, nullable=True)  # JSON: {"header_row": int, "columns": {col_idx: field}}
    # Parser type for xlsx/Sheets feeds: 'auto' (default, generic excel) or 'rp' (РП Україна section-grouped).
    parser_type = db.Column(db.String(20), nullable=False, default="auto", server_default="auto")
    is_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    last_fetched_at = db.Column(db.DateTime, nullable=True)
    last_fetch_status = db.Column(db.String(50), nullable=True)  # 'success', 'error'
    last_fetch_error = db.Column(db.Text, nullable=True)


@event.listens_for(Supplier, "before_insert")
def _autoset_slug(mapper, connection, target):
    if target.slug:
        return
    base = slugify_supplier_name(target.name or "")
    candidate = base
    n = 2
    table = Supplier.__table__
    while connection.execute(
        table.select().where(table.c.slug == candidate)
    ).first() is not None:
        candidate = f"{base}-{n}"
        n += 1
    target.slug = candidate
