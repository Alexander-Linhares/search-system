from .index import index_bp
from .dashboard import dashboard_bp

ROUTES = [
    index_bp,
    dashboard_bp
]

__all__ = [
    'ROUTES'
    ]