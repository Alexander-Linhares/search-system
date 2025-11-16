from flask import Blueprint, render_template

permit_bp = Blueprint('permit', __name__, url_prefix='/Permit')

@permit_bp.route('/', defaults={'subpath': ''})
@permit_bp.route('/<path:subpath>')
def logs_handler(subpath):
    """
        Função que lida com todas as requisições que chegam em /Logs/
        e subpastas, como /Logs/teste/ ou /Logs/teste/subpasta
    """

    if not subpath:
        print(f'você está na rota Permit: {permit_bp.name}')
        #Temporário
        title = "Permit"
        files = ["Arquivo um", "Arquivo dois", "Arquivo 3"]

        #rederiza o html 
        return render_template('logs.j2', title=title, files=files)

    return f'Conteúdo dinâmico {subpath}'