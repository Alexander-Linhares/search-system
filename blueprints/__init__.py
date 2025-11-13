from .logs import logs_bp

BLUEPRINTS_TO_REGISTER = [
    logs_bp
]

__all__ = [
    'BLUEPRINTS_TO_REGISTER'
    ]