import os

from flask import Flask, render_template, url_for

app = Flask(__name__)



database_path = os.path.normpath(
    os.path.join(os.path.abspath(__name__), '../search-system/database'))
database = [path for path in os.walk(database_path)]

def read_file(file_name: str):
    with open(file_name, 'r') as file:
        print(file.readline())

branches = {}

#começa em database
#walk é dividido em: abspath, directory_list, files
#primeiro lista os diretórios e os arquivos
#depois percorre cada diretório e lista seus subdiretórios e arquivos e repete o processo
#o primeiro loop é a raiz de todos os diretórios
"""
Saída esperada:

branches = {
  'search-system': {
    'database': {
      'Logs': {
        'files': [...],
        'teste': {
          'files': [...],
        }
      },
      'Requirements': {
        'files': [...]
      }
    }
  }
}
"""
def show_tree(current_node: dict, level: int = 0):
    ident = '    ' * level
    for key, value in current_node.items():
        if isinstance(value, dict):
            print(ident + key + '/')
            show_tree(value, level+1)
        elif key == 'files' and isinstance(value, list):
            for file in value:
                print(ident + file)
          


def translate_database():
    tree_structure = {}
    root = os.path.basename(database_path)
    for i, path in enumerate(database):
        absolute_path = path[0]
        directory_list = path[1]
        file_list = path[2]
        
        #a cada primerio loop o próximo loop reitera sobre cada nó da árvore
        current_level = tree_structure
        
        #separa os caminhos da árvore de diretórios 
        path_component = absolute_path.split(os.sep)
        #inicia na posição do diretório atual para não incluir outros que não queremos 
        path_component = path_component[path_component.index(root):] 

        # os componentes são os diretórios que estamos iterando
        for component in path_component:
            #verifica se o componente já foi incluido na árvore
            if component not in current_level: 
                current_level[component] = {}
            #atualiza o ponteiro dinâmico 
            current_level = current_level[component]
        
        #inclui informações adicionais para identificação do diretório
        current_level['abspath'] = absolute_path
        if file_list:
            current_level['files'] = file_list
        
    return tree_structure

          
        
            

branches = translate_database()
#     print(f'node: {node} | parent_node: {parent_node}')


    

show_tree(branches)
    

        

# @app.route('/')
# def root():
   
#     return render_template('index.html')

# if __name__ == "__main__":
#     app.run(debug=True)