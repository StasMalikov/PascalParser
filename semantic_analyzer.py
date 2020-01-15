class SemanticAnalyzer:
    def __init__(self, tree):
        self.tree = tree
        self.idents = []
        self.global_index = 0
        self.set_idents()

    def check(self):
        pass

    def print_idents(self):
        for item in self.idents:
            print(item.name + " " + item.type + " " + str(item.index) + " " + item.index_type + " " + str(item.value) + "\n")

    def set_idents(self):
        for i in range(len(self.tree.nodes)):
            if self.tree.nodes[i].type == "ident_block":
                for j in range(len(self.tree.nodes[i].body)):
                    for k in range(len(self.tree.nodes[i].body[j].values)):
                        self.idents.append(Ident(self.tree.nodes[i].body[j].values[k], self.tree.nodes[i].body[j]._type, self.global_index, "g", None))
                        self.global_index += 1

            # if self.tree.nodes[i].type == "func_proc_block":


            # if self.tree.nodes[i].type == "block_dot":


            # for j in range(len(self.tree.nodes[i].body)):
            #     if self.tree.nodes[i].body[j].classtype == "ident":
            #         print()

class Ident:
    def __init__(self, name, vtype, index, index_type, value):
        self.name = name
        self.type = vtype
        self.index = index
        self.index_type = index_type
        self.value = value
        if len(vtype.split(" ")) > 1:
            tmp = vtype.split()
            self.type = "array"
            self.arr_type = tmp[1]
            self.len = tmp[0]
            self.value = []

    # def __init__(self, node):
    #     self.name
    #     self.index
    #     self.type

    #     if node.classtype == "ident":
    #         self.kind
    #         self.value
    #         self.
    #         self.
    #         self.
    #     elif node.classtype == "procedure":
    #         self.
    #         self.
    #         self.
    #         self.
    #         self.
    #         self.