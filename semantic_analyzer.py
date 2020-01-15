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
            if not item.func:
                print(item.name + " " + item.type + " " + str(item.index) + " " + item.index_type + " " + str(item.value) + "\n")

            else:
                print("function \n")
                print("params:")
                for param in item.params:
                    print("----" + param.name + " " + param.type + " " + str(param.index) + " " + param.index_type + " " + str(param.value) + "\n")
                print("local vars:")
                for local in item.local_idents:
                    print("----" + local.name + " " + local.type + " " + str(local.index) + " " + local.index_type + " " + str(local.value) + "\n")

    def set_idents(self):
        for i in range(len(self.tree.nodes)):
            local_index = 0
            if self.tree.nodes[i].type == "ident_block":
                for j in range(len(self.tree.nodes[i].body)):
                    for k in range(len(self.tree.nodes[i].body[j].values)):
                        self.idents.append(Ident(self.tree.nodes[i].body[j].values[k], self.tree.nodes[i].body[j]._type, self.global_index, "g", None, False, None, None))
                        self.global_index += 1

            elif self.tree.nodes[i].type == "block_dot":
                for j in range(len(self.tree.nodes[i].body)):
                    if self.tree.nodes[i].body[j].classtype == "ident":
                        for k in range(len(self.tree.nodes[i].body[j].values)):
                            self.idents.append(Ident(self.tree.nodes[i].body[j].values[k], self.tree.nodes[i].body[j]._type, local_index, "l", None, False, None, None))
                            local_index += 1

            elif self.tree.nodes[i].type == "func_proc_block":
                for j in range(len(self.tree.nodes[i].body)):
                    self.idents.append(Ident(None, None, None, None, None, True, self.tree.nodes[i].body[j], self.tree.expr_list))

class Ident:
    def __init__(self, name, vtype, index, index_type, value, func, node = None, expr_list = None):
        self.func = func
        if not func:
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
        else:
            self.name = node.name
            self.type = node.classtype
            self.body = []
            self.local_idents = []
            for i in range(len(node.body)):
                if node.body[i] != 'None':
                    self.body.append(node.body[i])

            for i in range(len(self.body)):
                self.body[i] = expr_list['%s'% i]
                if self.body[i].classtype == "ident":
                    for j in range(len(self.body[i].values)):
                        self.local_idents.append(Ident(self.body[i].values[j], self.body[i]._type, len(self.local_idents), "l", None, False, None, None))

            self.params = []
            if node.param_list_index is not None:
                for i in range(len(node.param_list_index)):
                    if node.param_list_index[i] != 'None':
                        tmp = expr_list[node.param_list_index[i]]
                        for j in range(len(tmp.values)):
                            self.params.append(Ident(tmp.values[j], tmp._type, len(self.params), 'p', None, False, None, None))