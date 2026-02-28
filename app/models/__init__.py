# Import all models so they register with SQLAlchemy
from app.models.supplier import Supplier  # noqa: F401
from app.models.catalog import PromProduct  # noqa: F401
from app.models.supplier_product import SupplierProduct  # noqa: F401
from app.models.product_match import ProductMatch  # noqa: F401
from app.models.sync_run import SyncRun  # noqa: F401
from app.models.user import User  # noqa: F401
