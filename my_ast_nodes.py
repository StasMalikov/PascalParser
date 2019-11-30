class Tree:
    def __init__(self):
        self.nodes = []
        self.idents = []
        self.begin_index = 0
        self.expr_list = {}
        self.var_global = False
        self.var_block = False

    def add_block(self, indexes_string):
        if indexes_string is not None:
            arr_indexes = indexes_string.split(' ')
            body = []
            for i in range(len(arr_indexes)):
                if arr_indexes[i] in self.expr_list:
                    body.append(self.expr_list[arr_indexes[i]])
        
            self.nodes.append(Block(body))

    """Выбирает метод для отрисовки элементов AST дерева """
    def fork(self, node, attachment, last):
        if node.classtype == "additive":
            self.print_additive(node, attachment, last)

        elif node.classtype == "expr":
            self.print_expression(node, attachment, last)

        elif node.classtype == "assign":
            self.print_assign(node, attachment, last)

    def print_additive(self, node, attachment, last):
            if attachment > 0:
                if last:
                    if node.op is not None:
                        print("│" + " "*attachment + "└ " + node.op)
                    if node.left_index in self.expr_list:
                        self.fork(self.expr_list[node.left_index], attachment, last)
                    if node.right_index in self.expr_list:
                        self.fork(self.expr_list[node.right_index], attachment, last)
                else:
                    if node.op is not None:
                        print("│" + " "*attachment + "├ " + node.op)
                    if node.left_index in self.expr_list:
                        self.fork(self.expr_list[node.left_index], attachment, last)
                    if node.right_index in self.expr_list:
                        self.fork(self.expr_list[node.right_index], attachment, last)
            else:
                if node.op is not None:
                    print("├ " + node.op)
                if node.left_index in self.expr_list:
                    self.fork(self.expr_list[node.left_index],  2, last)
                if node.right_index in self.expr_list:
                    self.fork(self.expr_list[node.right_index], 2, last)


    def print_assign(self, node, attachment, last):
        if attachment > 0:
            if last:
                print("│" + " "*attachment + "└ " + ":=")
                print("│" + " "*attachment + "  ├ " + node.ident)
                self.fork(self.expr_list[node.body_index], attachment + 2, last)
            else:
                print("│" + " "*attachment + "├ " + ":=")
                print("│" + " "*attachment + "│ ├ " + node.ident)
                self.fork(self.expr_list[node.body_index], attachment + 2, last)
        else:
            print("├ " + ":=")
            print("│ ├ " + node.ident)
            self.fork(self.expr_list[node.body_index], 0, last)


    def print_expression(self, node, attachment, last):
            if attachment > 0:
                if last:
                    if node.operator is not None:
                        print("│ "*attachment + "└ " + node.operator)
                    if node.value1 is not None:
                        print("│ "*attachment  + "  ├ " + str(node.value1))
                    if node.value2 is not None:
                        print("│ "*attachment  + "  └ " + node.value2)
                else:
                    if node.operator is not None:
                        print("│ "*attachment + "├ " + node.operator)
                    if node.value1 is not None:
                        print("│ "*attachment + "│ ├ " + node.value1)
                    if node.value2 is not None:
                        print("│ "*attachment + "│ └ " + node.value2)
                    
            else:
                if node.operator is not None:
                    print("├ " + node.operator)
                if node.value1 is not None:
                    print("│ ├ " + node.value1)
                if node.value2 is not None:
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
            if self.nodes[i].classtype == "block":
                for j in range(len(self.nodes[i].body)):

                    if self.nodes[i].body[j].classtype == "ident":
                        if j == len(self.nodes[i].body) - 1:
                            self.print_identification(self.nodes[i].body[j], self.nodes[i].body[j].attachment, True)
                        else:
                            self.print_identification(self.nodes[i].body[j], self.nodes[i].body[j].attachment, False)

                    else:
                        if j == len(self.nodes[i].body) - 1:
                            self.fork(self.nodes[i].body[j], attachment + 1, True)
                        else:
                            self.fork(self.nodes[i].body[j], attachment + 1, False)

                    

                    
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

class AdditiveNode:
    def __init__(self,left_index, op, right_index):
        self.classtype = "additive"
        self.left_index = left_index
        self.op = op
        self.right_index = right_index

class AssignNode:
    def __init__(self, ident, body_index):
        self.classtype = "assign"
        self.ident = ident
        self.body_index = body_index

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