class Tree:
    def __init__(self):
        self.nodes = []
        self.idents = []

    def print_tree(self):
        print("...")
        for i in self.nodes:
            if i.classtype == "ident":
                if len(i._type.split(' ')) > 1 :
                    x = i._type.split()
                    print("├ array [ 1 .. " + x[0] + " ] of "+ " " + x[1])
                else:
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