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

print(match_file(DATABASE, 'regi'))

