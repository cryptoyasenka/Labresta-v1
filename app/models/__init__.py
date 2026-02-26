# Import all models so they register with SQLAlchemy
from app.models.supplier import Supplier  # noqa: F401
from app.models.catalog import PromProduct  # noqa: F401
from app.models.supplier_product import SupplierProduct  # noqa: F401
