class Tree:
    def __init__(self):
        self.nodes = []
        self.idents = []
        self.begin_index = 0
        self.expr_list = {}

    def add_block(self, indexes_string):
        if indexes_string is not None:
            arr_indexes = indexes_string.split(' ')
            body = []
            for i in range(len(arr_indexes)):
                if arr_indexes[i] in self.expr_list:
                    body.append(self.expr_list[arr_indexes[i]])
        
            self.nodes.append(Block(body))

    def print_expression(self, node, attachment, last):
        if attachment > 0:
            if last:
                print("│" + " "*attachment + "└ " + node.operator)
                print("│" + " "*attachment + "  ├ " + node.value1)
                print("│" + " "*attachment + "  └ " + node.value2)
            else:
                print("│" + " "*attachment + "├ " + node.operator)
                print("│" + " "*attachment + "│ ├ " + node.value1)
                print("│" + " "*attachment + "│ └ " + node.value2)
                
        else:
            print("├ " + node.operator)
            print("│ ├ " + node.value1)
            print("│ └ " + node.value2)
    
    def print_identification(self, node, attachment, last):
        if attachment > 0:
            if last:
                if len(node._type.split(' ')) > 1 :
                    x = node._type.split()
                    print("│" + " "*attachment + "└ array [ 1 .. " + x[0] + " ] of "+ " " + x[1])
                else:
                    print("│" + " "*attachment + "└ " + node._type)

                for j in range(len(node.values)):
                    if j == len(node.values) - 1:
                        print("│" + " "*attachment+ "  └ " + node.values[j])
                    else:
                        print("│" + " "*attachment + "  ├ " + node.values[j])

            else:
                if len(node._type.split(' ')) > 1 :
                    x = node._type.split()
                    print("│" + " "*attachment + "├ array [ 1 .. " + x[0] + " ] of "+ " " + x[1])
                else:
                    print("│" + " "*attachment + "├ " + node._type)

                for j in range(len(node.values)):
                    if j == len(node.values) - 1:
                        print("│" + " "*attachment+ "│ └ " + node.values[j])
                    else:
                        print("│" + " "*attachment + "│ ├ " + node.values[j])

        else:
            if len(node._type.split(' ')) > 1 :
                x = node._type.split()
                print("├ array [ 1 .. " + x[0] + " ] of "+ " " + x[1])
            else:
                print("├ " + node._type)

            for j in range(len(node.values)):
                if j == len(node.values) - 1:
                    print("│ └ " + node.values[j])
                else:
                    print("│ ├ " + node.values[j])

    def print_tree_recursion(self, attachment, nodes_rec):
        pass


    def print_tree(self):
        print("...")
        attachment = 0
        for i in range(len(self.nodes)):
            if self.nodes[i].classtype == "ident":
                if i == len(self.nodes) - 1:
                    self.print_identification(self.nodes[i], self.nodes[i].attachment, True)
                else:
                    self.print_identification(self.nodes[i], self.nodes[i].attachment, False)
            
            if self.nodes[i].classtype == "block":
                for j in range(len(self.nodes[i].body)):

                    if self.nodes[i].body[j].classtype == "ident":
                        if j == len(self.nodes[i].body) - 1:
                            self.print_identification(self.nodes[i].body[j], self.nodes[i].attachment, True)
                        else:
                            self.print_identification(self.nodes[i].body[j], self.nodes[i].attachment, False)

                    if self.nodes[i].body[j].classtype == "expr":
                        if j == len(self.nodes[i].body) - 1:
                            self.print_expression(self.nodes[i].body[j], attachment + 1, True)
                        else:
                            self.print_expression(self.nodes[i].body[j], attachment + 1, False)

                    
class Block:
    def __init__(self, body):
        self.body = body
        self.classtype = "block"

class IdentificationNode:
    def __init__(self, values, _type, begin_index):
        self.classtype = "ident"
        self._type = _type
        self.values = values
        self.attachment = begin_index

class ExpressionNode:
    def __init__(self, value1, op, value2):
        self.classtype = "expr"
        self.value1 = value1
        self.value2 = value2
        self.operator = op

class Unary:
    @staticmethod
    def define(oper, value):
        if oper == "-":
            return oper + value
        
        if oper == "not":
            if value == "true":
                return "false"

            if value == "false":
                return "true"