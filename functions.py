from pathlib import Path
from asyncio import Task, run


def root_dir(target: str) -> Path:
    r"""
        Encontra dinamicamente a raiz de um diretório dado o 
        caminho do arquivo em execução. root_dir percorre por meio da árvore 
        de diretórios antecessores do caminho atual, encontrando a 
        raiz desejada independente da localização hierárquica do arquivo.

        Parameters
        ----------

        :param target: O álvo para o arquivo desejado
        :type target: str

        Raises
        ------

        :raise FileNotFoundError: Retorna um erro caso não seja possível encontrar a raiz passada por target.
        Returns
        -------

        :return: Retorna um objeto Path que representa o nó final para target_root
        :rtype: Path
    """
    TARGET_ROOT_DIR = target
    starting_path = Path(__file__).resolve()
    for parent in starting_path.parents:
        if parent.name == TARGET_ROOT_DIR:
            ROOT_DIR = parent
            break
    else:
        raise FileNotFoundError(f"Não foi possível encontrar o diretório raiz {TARGET_ROOT_DIR} nos ancestrais de {starting_path}")
    return ROOT_DIR

rd = root_dir("search-system")
DATABASE = rd / "database"
def match_files(node: Path, file_name: str):
    r"""
        Busca por arquivos de forma recursiva na árvore de diretórios,
        percorrendo cada diretório e listando seus subcomponentes.

        Parameters
        ----------
        node : pathlib.Path
            O nó inicial da busca. É um objeto Path da biblioteca pathlib.
        file_name : str
            Pode ser o nome do arquivo completo ou apenas uma substring que pertença
            ao nome do arquivo.

        Returns
        -------
        str ou list of str
            O caminho absoluto para o arquivo, incluindo a extensão e a resolução de
            links simbólicos (se houver).
            
        Notes
        -----
        A função pode retornar uma *lista* de caminhos de arquivos se 'file_name' for
        compatível com mais de um arquivo, independentemente da hierarquia do nó da árvore.
        Se apenas um arquivo for encontrado, uma única string pode ser retornada.
    """
    matched_files = []
    for element in node.iterdir():
        if element.is_dir():
            sub_matches = match_files(element, file_name)
            #Concatena regressivamente o resultado da stack anterior (sub_matches) 
            matched_files.extend(sub_matches)
        elif element.is_file():
            if file_name.lower() in element.name.lower():
                matched_files.append(element.absolute())
            
    return matched_files

def read_csv(file_path: str):

    table: dict[list] = {}
    file = Path(file_path)
    #Verifica se o arquivo realmente existe para evitar erros durante
    #a execução caso o arquivo seja excluído, ou o caminho não exista
    if file.exists():
        with open(file_path, 'r', encoding="latin-1") as f:
            #Coleta informações da primeira linha (cabeçalho) e as transforma em chaves para o dicionário table
            # first_line = f.readline().split(',')
            # for column in first_line:
            #     key = column.replace('\n', '').strip('"')
            #     table[key] = [] #O nome do cabeçalho se torna uma chave de acesso para uma coluna

            total_lines = 0
            print("abri o arquivo")
            for line in f:
                l = list(map(lambda col: col.strip('\\n"\\n'), line.split(',')))
                for j, value in enumerate(l):
                    if total_lines == 0:
                        table[value] = []
                    else:
                        try:
                            print(next(keys))
                        except StopIteration as e:
                            print(f"o valor da coluna {j} impediu com que a linha fosse impressa corretametne {value}")
                            return 0
                keys = iter(table.keys())
                total_lines+=1
                

    return table

def dict_table_to_matrix(d: dict):
    """header representa as chaves do dicionário em uma lista """
    header = list(d.keys())
    matrix = []
    for j in range(len(list(d.values())[0])):
        line = []
        for i in range(len(header)):
            line.append(d[header[i]][j])
        matrix.append(line)
    matrix.insert(0, header)
    return matrix

def print_matrix(m: list[list]):
    for i in range(len(m)):
        for j in range(len(m[i])):
            cell = m[i][j]
            print(f'{cell.center(10, ' ')}', end=' ')
        print()

def split_with_enclosure(line: str) -> list:
    """
        Divide uma linha de um arquivo de forma inteligênte, utilizando a técnica 
        de cerceamento de estado para identificar se os separadores da divisão são parte de um
        texto ou se são de fato separadores.
    """
    is_inside_quotes = False
    splited = []
    word = ''

    for n, letter in enumerate(line):
        if letter == '"': 
            is_inside_quotes = not is_inside_quotes

        # a partir daqui ele começará a inserir caso esteja dentro das aspas
            
        if letter == ',' and not is_inside_quotes:
            splited.append(word)
            word = ''
        else:
            word += letter
        
    
    return splited



if __name__ == "__main__":
    some_csv_file_path = match_files(DATABASE, 'regi')[0]
    print(type(some_csv_file_path))


    #t = read_csv(some_csv_file_path)
    #m = dict_table_to_matrix(t)
    #print(t)
    #print_matrix(m)

    a = ['"marlon", "indivíduo armado, até os dentes", "copo delito", 1, 1200']
    print(split_with_enclosure(a[0]))

