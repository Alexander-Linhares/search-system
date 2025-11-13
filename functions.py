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
    #a execução caso o arquivo seja excluído, ou o caminho não exista mais
    if file.exists():
        with open(file_path, 'r', encoding="latin-1") as f:
            total_lines = 0
            #Percorre linha a linha do arquivo 
            for line in f:

                #TEMP
                if total_lines == 10:
                    break

                treted_line = split_with_enclosure(line)

                if total_lines == 0:
                    table = {key: [] for key in treted_line}
                else:
                    for key, new_value in zip(table.keys(), treted_line):
                        table[key].append(new_value)

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

def split_with_enclosure(line: str) -> list[str]:
    r"""
        Divide uma linha de um arquivo CSV (delimitado por vírgulas) utilizando a técnica de cerceamento de estado para identificar separadores que estão fora do cerceamento por aspas (enclosure).

        Parameters
        ----------

        :param line: Representa uma linha de arquivo CSV 
        :type line: str

        Returns
        -------

        list[str]

        Retorna uma lista de strings assim como split 

        Notes
        -----
        Essa função pode ser utilizada em outro contextos assim como split, no entanto, é
        imporatnte notar que ela é especialmente destinada para arquivos csv
    """
    splited = []
    is_inside_quotes = False
    word = ''
    
    for letter in line.replace('\n', ''):

        #1. se não estiver dentro de aspas: sabemos que toda vírgula pode ser inserida como texto -> word += letter,
        #2. se estiver fora de aspas: a vírgula representa uma separação -> a palavra é incluída sem espaços e é limpa
        #3. se for o último caracter: a última letra deve ser incluída e a palavra inserida
        #4. dedução: todo caracter deve ser incluído, ao menos se ele não estiver dentro de aspas e for uma vírgula
        #5. not is_inside_quotes and is_comma: é o caso em que a palavra deve ser dividida e incluída nas palavras separadas
        
        is_comma = letter == ','
        is_inside_quotes = not is_inside_quotes if letter == '"' else is_inside_quotes
        is_separator_comma = not is_inside_quotes and is_comma

        if is_separator_comma:
            splited.append(word.strip().strip('"'))
            word = ''
            continue
        word += letter
    else:
        #A conclusão para essa função é que é necessário incluir 
        #a última palavra (a variável word) ao final da execução do for,
        #repetindo a linha de inclusão da palavra
        splited.append(word.strip())
    
    return splited

if __name__ == "__main__":
    some_csv_file_path = match_files(DATABASE, 'regi')[0]
    print(type(some_csv_file_path))


    t = read_csv(some_csv_file_path)
    m = dict_table_to_matrix(t)
    
    #print(t)
    print_matrix(m)

