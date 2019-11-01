class Tree:
    def __init__(self):
        self.nodes = []
        self.idents = []

    def print_tree(self):
        print("...")
        for i in self.nodes:
            if i.classtype == "ident":
                print("├ " + i._type)
                for j in range(len(i.values)):
                    if j == len(i.values)-1:
                        print("│  └ " + i.values[j])
                    else:
                        print("│  ├ " + i.values[j])


class IdentificationNode:
    def __init__(self, values, _type):
        self.classtype = "ident"
        self._type = _type
        self.values = values