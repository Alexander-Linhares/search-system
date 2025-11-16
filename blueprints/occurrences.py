from flask import Blueprint, render_template

occurrences_bp = Blueprint('occurrences', __name__, url_prefix='/Occurrences')

@occurrences_bp.route('/', defaults={'subpath': ''})
@occurrences_bp.route('/<path:subpath>')
def occurrences_handler(subpath):
    """
        Função que lida com todas as requisições que chegam em /Logs/
        e subpastas, como /Logs/teste/ ou /Logs/teste/subpasta
    """

    if not subpath:
        print(f'você está na rota Occurrences: {occurrences_bp.name}')
        #Temporário
        title = "Occurrences"
        files = ["Arquivo um", "Arquivo dois", "Arquivo 3"]

        #rederiza o html 
        return render_template('logs.j2', title=title, files=files)

    return f'Conteúdo dinâmico {subpath}'