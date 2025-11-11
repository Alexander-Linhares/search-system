class DictTree:
    def __init__(self, root: str):
        """
            Inicializa a árvore de dicionários.
            Parameters: 
            root: definie o nome de qual será o diretório prin
        """

        self.tree_structure = {} 

    def display(self, current_node: dict, level: int = 0):
        ident = '    ' * level
        for key, value in current_node.items():
            if isinstance(value, dict):
                print(ident + key + '/')
                self.display(value, level+1)
            elif key == 'files' and isinstance(value, list):
                for file in value:
                    print(ident + file)
    

    



if __name__ == "__main__":
    db_struct = DictTree()