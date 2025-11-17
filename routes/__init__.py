from .index import index_bp
from .dashboard import dashboard_bp
import routes.api 

ROUTES = [
    index_bp,
    dashboard_bp,
    *routes.api.API_ROUTES
]

__all__ = [
    'ROUTES'
    ]