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

        elif node.classtype == "if_block":
            self.print_if_block(node, attachment, last)
             
        elif node.classtype == "for_block":
            self.print_for_block(node, attachment, last)
        
        elif node.classtype == "while_block":
            self.print_while_block(node, attachment, last)

        elif node.classtype == "do_while_block":
            self.print_do_while_block(node, attachment, last)

        elif node.classtype == "procedure_call":
            self.print_procedure_call(node, attachment, last)


    def print_if_block(self, node, attachment, last):
        print("│" + " "*attachment + "├ if")
        self.fork(self.expr_list[node.condition], attachment, False)
        print("│" + " "*attachment + "├ then")
        for i in range(len(node.then_block)):
            if node.then_block[i] in self.expr_list:
                self.fork(self.expr_list[node.then_block[i]], attachment, False)
        if node.else_block is not None:
            print("│" + " "*attachment + "├ else")
            for i in range(len(node.else_block)):
                if node.else_block[i] in self.expr_list:
                    self.fork(self.expr_list[node.else_block[i]], attachment, False)
    
    def print_for_block(self, node, attachment, last):
        print("│" + " "*attachment + "├ for")
        self.fork(self.expr_list[node.start_condition_index], attachment, False)
        print("│" + " "*attachment + "├ to " + str(node.end_number))
        for i in range(len(node.body)):
            if node.body[i] in self.expr_list:
                self.fork(self.expr_list[node.body[i]], attachment, False)

    def print_while_block(self, node, attachment, last):
        print("│" + " "*attachment + "├ while")
        self.fork(self.expr_list[node.condition_index], attachment, False)
        print("│" + " "*attachment + "├ do")
        for i in range(len(node.body)):
            if node.body[i] in self.expr_list:
                self.fork(self.expr_list[node.body[i]], attachment, False)

    def print_do_while_block(self, node, attachment, last):
        print("│" + " "*attachment + "├ dowhile")
        self.fork(self.expr_list[node.condition_index], attachment, False)
        print("│" + " "*attachment + "├ do")
        for i in range(len(node.body)):
            if node.body[i] in self.expr_list:
                self.fork(self.expr_list[node.body[i]], attachment, False)

    def print_procedure_call(self ,node, attachment, last):
        print("│" + " "*attachment + "├ procedure_call " + node.name)
        if len(node.params) > 0:
            print("│" + " "*attachment + "├ params:")
            for i in range(len(node.params)):
                print("│" + " "*attachment + "  ├ " + str(node.params[i]))

    def print_procedure(self ,node, attachment, last):
        print("│" + " "*attachment + "├ procedure " + node.name)
        print("│" + " "*attachment + "├ params:")
        for i in range(len(node.param_list_index)):
            if node.param_list_index[i] in self.expr_list:
                self.print_identification(self.expr_list[node.param_list_index[i]], attachment, False)
        print("│" + " "*attachment + "├ body:")
        for i in range(len(node.body)):
            if node.body[i] in self.expr_list:
                self.fork(self.expr_list[node.body[i]], attachment, False)
    

    def print_additive(self, node, attachment, last):
            if attachment > 0:
                if last:
                    if node.op is not None:
                        print("│" + " "*attachment + "└ " + node.op)
                    if node.left_index in self.expr_list:
                        self.fork(self.expr_list[node.left_index], attachment , last)
                    if node.right_index in self.expr_list:
                        self.fork(self.expr_list[node.right_index], attachment, last)
                else:
                    if node.op is not None:
                        print("│" + " "*attachment + "├ " + node.op)
                    if node.left_index in self.expr_list:
                        self.fork(self.expr_list[node.left_index], attachment , last)
                    if node.right_index in self.expr_list:
                        self.fork(self.expr_list[node.right_index], attachment , last)
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
                        print("│ "*attachment + "│ ├ " + str(node.value1))
                    if node.value2 is not None:
                        print("│ "*attachment + "│ └ " + str(node.value2))
                    
            else:
                if node.operator is not None:
                    print("├ " + node.operator)
                if node.value1 is not None:
                    print("│ ├ " + str( node.value1))
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

                    elif self.nodes[i].body[j].classtype == "procedure":
                        self.print_procedure(self.nodes[i].body[j], attachment + 1, False)

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

class ForNode:
    def __init__(self, start_condition_index, end_number, body):
        self.classtype = "for_block"
        self.start_condition_index = start_condition_index
        self.end_number = end_number
        if body is not None:
            self.body = body.split(' ')

class Procedure:
    def __init__(self, name, param_list_index, body):
        self.classtype = "procedure"
        self.name = name
        if body is not None:
            self.body = body.split(' ')

        if param_list_index is not None:
            self.param_list_index = param_list_index.split(' ')

class ProcedureCall:
    def __init__(self, name, params):
        self.classtype = "procedure_call"
        self.name = name
        self.params = []
        if params is not None:
            for i in range(len(params)):
                if params[i] is not None:
                    self.params.append(params[i])
        # if params is not None:
        #     self.params = params.split(' ')

class WhileNode:
    def __init__(self, condition_index, body):
        self.classtype = "while_block"
        self.condition_index = condition_index
        if body is not None:
            self.body = body.split(' ')

class DoWhileNode:
    def __init__(self, condition_index, body):
        self.classtype = "do_while_block"
        self.condition_index = condition_index
        if body is not None:
            self.body = body.split(' ')

class IfBlock:
    def __init__(self, condition, then_block, else_block):
        self.classtype = "if_block"
        self.condition = condition

        if then_block is not None:
            self.then_block = then_block.split(' ')

        if else_block is not None:
            self.else_block = else_block.split(' ')
        else:
            self.else_block = None

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