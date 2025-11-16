from .logs import logs_bp
from .occurrences import occurrences_bp
from .permit import permit_bp
from .requiriments import requirements_bp

BLUEPRINTS_TO_REGISTER = [
    logs_bp,
    occurrences_bp,
    permit_bp,
    requirements_bp
]

__all__ = [
    'BLUEPRINTS_TO_REGISTER'
    ]