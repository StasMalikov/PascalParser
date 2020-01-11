class SemanticAnalyzer:
    def __init__(self, tree):
        self.tree = tree

    def check(self):
        pass

    def print_idents(self):
        for i in range(len(self.tree.nodes)):
            for j in range(len(self.tree.nodes[i].body)):
                if self.tree.nodes[i].body[j].classtype == "ident":
                    print()

class Ident:
    def __init__(self, node):
        self.name
        self.index
        self.type

        if node.classtype == "ident":
            self.kind
            self.value
            self.
            self.
            self.
        elif node.classtype == "procedure":
            self.
            self.
            self.
            self.
            self.
            self.