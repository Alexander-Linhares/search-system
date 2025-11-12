from pathlib import Path

def root_dir(target: str) -> Path:
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
def match_file(node: Path, file_name: str):
    matched_files = []
    for element in node.iterdir():
        if element.is_dir():
            sub_matches = match_file(element, file_name)
            matched_files.extend(sub_matches)
        elif element.is_file():
            if file_name.lower() in element.name.lower():
                matched_files.append(element.absolute())
            
    return matched_files

some_csv_file_path = match_file(DATABASE, 'regi')[0]

def readfile(file_path: str):
    table = {}
    with open(file_path, 'r') as file:
        first_line = file.readline().split(',')
        for column in first_line:
            table[column.replace('\n', '').strip('"')] = []
        
        i = 0
        while i < 10:
            line = file.readline().split(',')
            for j, column in enumerate(line):
                keys = list(table.keys())[j]
                table[keys].append(column.strip('"').replace('\n', ''))
            i+=1

    return table

def dict_table_to_matrix(d: dict):
    #header representa as chaves do dicionário em uma lista 
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

t = readfile(some_csv_file_path)
m = dict_table_to_matrix(t)
print_matrix(m)
