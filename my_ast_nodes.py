class Tree:
    def __init__(self):
        self.nodes = []
        self.idents = []

    def print_tree(self):
        for i in self.nodes:
            if i.classtype == "ident":
                print(i._type)
                print(i.values)


class IdentificationNode:
    def __init__(self, values, _type):
        self.classtype = "ident"
        self._type = _type
        self.values = values