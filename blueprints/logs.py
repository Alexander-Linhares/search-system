from flask import Blueprint, render_template, request
from functions import match_files, DATABASE, generate_transposed, read_csv

logs_bp = Blueprint('logs', __name__, url_prefix='/Logs')

@logs_bp.route('/', defaults={'subpath': ''})
@logs_bp.route('/<path:subpath>')
def logs_handler(subpath):
    """
        Função que lida com todas as requisições que chegam em /Logs/
        e subpastas, como /Logs/teste/ ou /Logs/teste/subpasta
    """
    #busca os arquivos
    files = match_files(DATABASE, 'porte')
    #pega a página 
    page = request.args.get("page", 1, int)

    if not subpath:
        print(f'você está na rota logs: {logs_bp.name}')
        #Temporário
        title = "Logs"
        
        #rederiza o html 
        return render_template('logs.j2', title=title, files=files, endpoint='logs.logs_handler')

    table = read_csv(files[0], 'latin-1')
    
    header = list(map(lambda x: x.replace('_', ' ').lower().title() ,table.keys()))
    body = next(generate_transposed(table))

    print(body)

    print(header)
    return render_template('dashboard.j2', header=header, body=body, page=page)