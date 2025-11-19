from .index import index_bp
from .dashboard import dashboard_bp
from .api import API_ROUTES

ROUTES = [
    index_bp,
    dashboard_bp,
    *API_ROUTES
]

__all__ = [
    'ROUTES'
    ]