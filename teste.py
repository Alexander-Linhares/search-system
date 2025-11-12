from pathlib import Path

def root_dir(target: str) -> Path:
    """
        Encontra dinamicamente 
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
            matched_files.extend(sub_matches)
        elif element.is_file():
            if file_name.lower() in element.name.lower():
                matched_files.append(element.absolute())
            
    return matched_files

some_csv_file_path = match_files(DATABASE, 'regi')[0]
print(type(some_csv_file_path))

def read_csv(file_path: str):
    table = {}
    with open(file_path, 'r', encoding="latin-1") as file:
        first_line = file.readline().split(',')
        for column in first_line:
            key = column.replace('\n', '').strip('"')
            table[key] = []
        
        i = 0
        while i < 10:
            line = file.readline().split(',')
            for j, column in enumerate(line):
                keys = list(table.keys())[j]
                table[keys].append(column.strip('"').replace('\n', ''))
            i+=1

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

t = read_csv(some_csv_file_path)
m = dict_table_to_matrix(t)
print_matrix(m)

