from flask import Blueprint, render_template, request
from functions import match_files, DATABASE, generate_transposed, read_csv
from pathlib import Path
from functions import root_dir

PROJECT_ROOT = root_dir("search-system")
DATABASE = PROJECT_ROOT / 'database'

index_bp = Blueprint('index', __name__, url_prefix='/')

def build_uri(root: Path, subpath:str) -> Path:
    new_uri  = Path(root, subpath)
    if (new_uri.exists()):
        print("Essa uri é válida")
        return new_uri
    else:
        raise FileNotFoundError('Path não encontrado')


@index_bp.route('/', defaults={'subpath': ''})
@index_bp.route('/<path:subpath>')
def index_endpoint(subpath):

    

    uri: Path = build_uri(DATABASE, subpath)
    #verifica se a uri realmente existe, build_uri retorna none caso não consiga montar a uri 
    if uri:
        
        if uri.is_dir():
            title = 'Polícia Militar' if not subpath else uri.name
            #lista os diretórios
            #index é a visualização dos módulos
            path_components = {
                f'component-{n}': {
                    'name': component.name, 
                    'type': ('directory' if component.is_dir() else 'file'),
                    'uri': component.relative_to(DATABASE).as_posix()
                }
                for n, component in enumerate(uri.iterdir())
            }
            return render_template('index.j2', path_components=path_components, title=title)
        if uri.is_file():
            #leva para dashboard

            #dashboard será a página de visualização das métricas e da table overview
            return render_template('dashboard.j2')

    return '<p>Não foi possível encontrar o caminho especificado</p>'