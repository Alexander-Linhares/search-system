from pathlib import Path
from itertools import batched
from typing import TypeAlias, Dict, List, Iterator, Any
from asyncio import Task, run

TableStructure: TypeAlias = Dict[str, List[str | None]]
TableFragment: TypeAlias = List[List[str | None]]
Vector: TypeAlias = List[Any]

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
                matched_files.append(element)
            
    return matched_files

def read_csv(file_path: str, encoding: str) -> TableStructure:
    r"""
        Lê um arquivo completo linha a linha com a extenção csv e retorna um dicionário de listas,
        permitindo o acesso à lista da coluna por meio da chave do cabeçalho do arquivo.

        Parameters
        ----------

        :param file_path: caminho absoluto para o arquivo .
        :type file_path: str
        :param encoding: a codificação do arquivo.
        :type encoding: str

        Raises
        ------

        :raise FileNotFoundError: Levanta um erro de arquivo não encontrado caso o caminho `file_path` resultar num arquivo não existente ou caso a extenção não seja equivalente ao arquivo que esta na pasta.

        Returns
        -------

        :return: Retorna um dicionário de listas completo, permitindo a agregação dados de forma eficaz.

        Limitations
        -----

        Pode não ser adqueda para obter arquivos muito extensos eficientemente
    """

    table: TableStructure = {}
    file = Path(file_path)
    #Verifica se o arquivo realmente existe para evitar erros durante
    #a execução caso o arquivo seja excluído, ou o caminho não exista mais
    if file.exists():
        with open(file_path, 'r', encoding=encoding) as f:
            total_lines = 0
            #Percorre linha a linha do arquivo 
            for line in f:
                
                #Temporário
                if total_lines == 40:
                    break
                #'"ANO_EMISSAO", "MES_MISSAO", "UF", "MUNICÍPIO",'
                #resumidamente oq slipt_with_enclosure faz: ['ANO_EMISSAO', 'MES_MISSAO', 'UF', 'MUNICÍPIO', '']
                treted_line = split_with_enclosure(line)
                if total_lines == 0:
                    #Aqui a compreensão de dicionários (dict comprehension) é fundamental para evitar 
                    #a mesma referência de objeto, apontando todos para a mesma lista
                    #Forma anterior: table = table.fromkeys(treted_line, [])
                    #O problema consistia em que fromkeys atribuia a mesma lista para toda chave, obtendo um resultado de duplicidade entre as chaves
                    #key: [] traz para cada chave do dicionário uma referência de lista distinta o que mantem a integridade do código
                    table = {key: [] for key in treted_line}
                else:
                    keys = table.keys()
                    #A função zip irá compilar chave e valor 
                    #A = [a, b, c, d, f]
                    #B =[banan, maça, pera, figo, melancia]
                    #C =((a, banana, ...), (b, maça), (c, pera), (d, figo), (f, melancia))
                    for key, new_value in zip(keys, treted_line):
                        clean_value = new_value.strip()
                        if not clean_value:
                            final_value = None
                        else:
                            final_value = clean_value
                        table[key].append(final_value)

                total_lines+=1
    else:
        raise FileNotFoundError(f'Não foi possível encontrar o arquivo {file.name}')
                

    return table

def generate_transposed(
        table: TableStructure, 
        batch_len: int = 10) -> Iterator[TableFragment]:
    """
        Comprime os valores da tabela em fragmentos menores de matriz e gera sobre eles linhas em lotes de dados.

        Parameters
        ----------

        :param table: Representa uma estrutura de dados baseada em colunas
        :type table: TableStructure
        :param batch_len: O tamanho máximo de cada lote
        :type batch_len: int

        Returns
        -------

        Retorna um `generator` dos fragmentos da tabela (`TableFragment`)
    """
    #Verifica se a tabela está vazia

    """
    ANO_EMISSÃO: [1999, 1923, 1823]

    """

    if not table:
        return
    #SPREAD
    #zip(table.values()) -> zip(
    # [ <- lista
    #   [...], [...], ...
    #]) -> zip(listazona)
    #zip(*table.values()) -> zip(lista1, lista2, lista3, lista4)
    #[[lista1[0], lista2[0], lista3[0], lista4[0]]]
    compressed_content = list(zip(*table.values()))
    yield from batched(compressed_content, batch_len)

def display_fragment(tf: TableFragment):
    for batch in tf:
        for line in batch:
            for column in line:
                print(column, end=' ')
            print()

def split_with_enclosure(line: str, *separators: str) -> list[str]:
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
    if not separators:
        separators = (',', ';')

    splited = []
    is_inside_quotes = False
    word = ''
    
    for i, letter in enumerate(line.replace('\n', '')):

        #1. se não estiver dentro de aspas: sabemos que toda vírgula pode ser inserida como texto -> word += letter,
        #2. se estiver fora de aspas: a vírgula representa uma separação -> a palavra é incluída sem espaços e é limpa
        #3. se for o último caracter: a última letra deve ser incluída e a palavra inserida
        #4. dedução: todo caracter deve ser incluído, ao menos se ele não estiver dentro de aspas e for uma vírgula
        #5. not is_inside_quotes and is_comma: é o caso em que a palavra deve ser dividida e incluída nas palavras separadas
        
        is_comma = letter in separators
        is_inside_quotes = not is_inside_quotes if letter == '"' else is_inside_quotes
        #não está dentro de aspas e não é uma vírgula
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
        splited.append(word.strip().strip('"'))
    
    return splited

if __name__ == "__main__":
    # some_csv_file_path = match_files(DATABASE, 'porte')[0]
    # print(type(some_csv_file_path))

    
    # t = read_csv(some_csv_file_path, 'latin-1')
    # m = generate_transposed(t)
    # print(t['MUNICIPIO'].count('ARAPIRACA'))


    def foo(*args): #args
        for arg in args:
            print(arg)

    foo(*['a', 'b', 'c']) # -> foo('a', 'b', 'c')

    # d = {'a': ['abacaxi', 'abajur'], 'b': ['banana', 'boia'], 'c': ['caju', 'chinelo']}
    # #d.values() # -> [[], [], []]
    # print(d['a'])

    # for element in zip(*d.values()):
    #     print(element)

    a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    lotes = batched(a, 2)
    for lote in lotes:
        print(lote)