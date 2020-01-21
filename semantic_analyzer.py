import my_ast_nodes 

class SemanticAnalyzer:
    def __init__(self, tree):
        self.tree = tree
        self.idents = []
        self.blocs = []
        self.global_index = 0
        self.set_idents()

    def semantics_check(self):
        for node in self.tree.nodes:
            if node.type == "block_dot":
                if not self.dot_block_check(node.body):
                    return False

        print("Ошибок не обнаружено.")
        return True

    def dot_block_check(self, body):
        for node in body:
            if node.classtype == "ident":
                continue

            if node.classtype == "assign":
                if not self.check_assign(node):
                    return False

            if node.classtype == "if_block":
                if not self.check_if(node):
                    return False
            
            if node.classtype == "procedure_call":
                if not self.choose_func(node):
                    return False

            if node.classtype == "for_block":
                if not self.check_for(node):
                    return False

            if node.classtype == "while_block":
                if not self.check_while(node):
                    return False

            if node.classtype == "do_while_block":
                if not self.check_dowhile(node):
                    return False

        return True


    def check_dowhile(self, node):
        condition = self.tree.expr_list[node.condition_index]
        if not self.choose_func(condition):
            return False

        for index in node.body:
            if index != "None":
                tmp_node = self.tree.expr_list[index]
                if not self.choose_func(tmp_node):
                    return False

        return True

    def check_while(self, node):
        condition = self.tree.expr_list[node.condition_index]
        if not self.choose_func(condition):
            return False

        for index in node.body:
            if index != "None":
                tmp_node = self.tree.expr_list[index]
                if not self.choose_func(tmp_node):
                    return False

        return True

    def check_for(self, node):
        condition = self.tree.expr_list[node.start_condition_index]
        self.idents.append(Ident(condition.ident, "integer", 0, "for", None, False, None, None))

        if not self.choose_func(condition):
            return False

        for index in node.body:
            if index != "None":
                tmp_node = self.tree.expr_list[index]
                if not self.choose_func(tmp_node):
                    return False

        return True


    def check_if(self, node):
        condition = self.tree.expr_list[node.condition]
        if not self.choose_func(condition):
            return False
        
        if node.then_block is not None:
            for index in node.then_block:
                if index != "None":
                    tmp_node = self.tree.expr_list[index]
                    if not self.choose_func(tmp_node):
                        return False

        if node.else_block is not None:
            for index in node.else_block:
                if index != "None":
                    tmp_node = self.tree.expr_list[index]
                    if not self.choose_func(tmp_node):
                        return False


        return True

    def check_assign(self, node):
        if not self.find_var(node.ident):
            return False

        body = self.tree.expr_list[node.body_index]
        if not self.choose_func(body):
            return False

        return True
                
    def find_var(self, name):
        tmp = name.split('[')
        if len(tmp) > 1:
            for ident in self.idents:
                if tmp[0] == ident.name:
                    tmp2 = tmp[1].split("]")[0]
                    if tmp2.isdigit():
                        if int(tmp2) > 0 and int(tmp2) <= int(ident.len):
                            return True
                        else:
                            print("Ошибка! Выход за пределы массива " + tmp[0])
                            return False
                    else:
                        return self.find_var(tmp2)

        else:    
            for ident in self.idents:
                if ident.name == name:
                    return True

        print("Ошибка! Переменной '" + name + "' не существует.")
        return False

    def get_var_value(self, name, index = None):
        for ident in self.idents:
            if ident.name == name:
                if index is not None:
                    if (index > 0) and (index <= ident.len):
                        return ident.value[index - 1]
                else:
                    return ident.value
        return None


    def check_additive(self, node):
        if (node.left_index is not None) and (node.right_index is not None):
            left = self.tree.expr_list[node.left_index]
            right = self.tree.expr_list[node.right_index]
            return True if self.choose_func(left) and self.choose_func(right) else False

        else:
            if (node.left_index is not None):
                left = self.tree.expr_list[node.left_index]
                return True if self.choose_func(left) else False

            if (node.right_index is not None):
                right = self.tree.expr_list[node.right_index]
                return True if self.choose_func(right) else False

    def check_expr(self, node):
        if node.operator is not None:
            if node.operator == "function":
                func_call = self.tree.expr_list[node.value1]
                return self.choose_func(func_call)

        if (node.value1 is not None) and (node.value2 is not None):
            return True if self.check_value(node.value1) and self.check_value(node.value2) else False

        else:
            if (node.value1 is not None):
                return self.check_value(node.value1)

            if (node.value2 is not None):
                return self.check_value(node.value2)

    def check_func_call(self, node):
        for ident in self.idents:
            if ident.name == node.name:
                return True

        print("Ошибка! Функция " + node.name + " не найдена.")
        return False


    def check_proc_call(self, node):
        for ident in self.idents:
            if ident.name == node.name:
                return True

        print("Ошибка! Процедура " + node.name + " не найдена.")
        return False


    def check_value(self, value):
        if str(value).isdigit():
            return True

        elif len(value.split("'")) > 2:
            return True

        elif value == "True" or value == "False":
            return True

        else:
            return self.find_var(value)

    def choose_func(self, node):
        if node.classtype == "additive":
            return self.check_additive(node)

        if node.classtype == "expr":
            return self.check_expr(node)

        if node.classtype == "assign":
            return self.check_assign(node)

        if node.classtype == "function_call":
            return self.check_func_call(node)

        if node.classtype == "procedure_call":
            return self.check_proc_call(node)

    def print_idents(self):
        for item in self.idents:
            if not item.func:
                print(item.name + " " + item.type + " " + str(item.index) + " " + item.index_type + " " + str(item.value) + "\n")

            else:
                if item.type == "function":
                    print("function " + item.name + " " + "return " + item.return_type + "\n")
                else:
                    print("procedure " + item.name + "\n")
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
        write = my_ast_nodes.Procedure("Write", None, None)
        read = my_ast_nodes.Function("Read", None, None, "char", None)
        inc = my_ast_nodes.Function("Inc", None, None, "integer", None)
        dec = my_ast_nodes.Function("Dec", None, None, "integer", None)
        abc = my_ast_nodes.Function("Abs", None, None, "integer", None)

        self.idents.append(Ident(None, None, None, None, None, True, write, self.tree.expr_list))
        self.idents.append(Ident(None, None, None, None, None, True, read, self.tree.expr_list))
        self.idents.append(Ident(None, None, None, None, None, True, inc, self.tree.expr_list))
        self.idents.append(Ident(None, None, None, None, None, True, dec, self.tree.expr_list))
        self.idents.append(Ident(None, None, None, None, None, True, abc, self.tree.expr_list))
        

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
            if self.type == "function":
                self.return_type = node.return_type
            self.body = []
            self.local_idents = []
            if node.body is not None:
                for i in range(len(node.body)):
                    if node.body[i] != 'None':
                        self.body.append(node.body[i])

            for i in range(len(self.body)):
                self.body[i] = expr_list[self.body[i]]
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