from flask import Blueprint

logs_bp = Blueprint('logs', __name__, url_prefix='/Logs')

@logs_bp.route('/', defaults={'subpath': ''})
@logs_bp.route('/<path:subpath>')
def logs_handler(subpath):
    """
        Função que lida com todas as requisições que chegam em /Logs/
        e subpastas, como /Logs/teste/ ou /Logs/teste/subpasta
    """

    if not subpath:
        return '<p>Rota raiz de Logs</p>'

    return f'Conteúdo dinâmico {subpath}'