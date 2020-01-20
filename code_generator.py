class CodeGenerator:
    def __init__(self, idents, tree):
        self.idents = idents
        self.tree = tree
        self.instructions = []
        self.tab = "    "


    def set_instructions(self):
        for node in self.tree.nodes:
            if node.type == "block_dot":
                self.parce_dot(node.body, 0)

            if node.type == "func_proc_block":
                self.parce_func_proc(node.body)

            
    def parce_func_proc(self, nodes):
        for node in nodes:
            if node.classtype == "function":
                self.parce_func_proc_body(node, True)
            
            if node.classtype == "procedure":
                self.parce_func_proc_body(node, False)

    def parce_func_proc_body(self, node, func):
        instructoin = "def "+ node.name +"("
        lengh = len(node.param_list_index)
        for i in range(lengh):
            if node.param_list_index[i] != "None":
                tmp = self.tree.expr_list[node.param_list_index[i]]
                for j in range(len(tmp.values)):
                    if tmp.values[j] != "None":
                        if (i == 0 ) and (j == 0):
                            instructoin += tmp.values[j] + ","

                        elif (i == lengh - 1) and (j == len(tmp.values) -1):
                            instructoin += tmp.values[j]

                        else:
                            instructoin += " " + tmp.values[j] + ","
        
        instructoin += "):"
        self.instructions.append(instructoin)
        arr = []
        for node_index in node.body:
            if node_index != "None":
                arr.append(self.tree.expr_list[node_index]) 
        
        self.parce_dot(arr, 1)
        if func:
            self.instructions.append(self.tab + "return " + node.name)

    def parce_dot(self, nodes, multiplier):
        for node in nodes:
            if node.classtype == "ident":
                continue

            if node.classtype == "assign":
                self.instructions.append(self.parce_assign(node, multiplier))

            if node.classtype == "if_block":
                self.parce_if(node, multiplier)

            if node.classtype == "procedure_call":
                self.parce_proc_call(node, multiplier)

            if node.classtype == "for_block":
                self.parce_for(node, multiplier)
                
            if node.classtype == "while_block":
                self.parce_while(node, multiplier)

            if node.classtype == "do_while_block":
                self.parce_do_while(node, multiplier)


    def parce_do_while(self, node, multiplier):
        condition = self.tree.expr_list[node.condition_index]
        instructoin = multiplier*self.tab + "while True:\n"
        for index in node.body:
            if index != "None":
                tmp_node = self.tree.expr_list[index]
                instructoin +=  self.tab*(multiplier + 1)  + self.choose_def(tmp_node) + "\n"

        instructoin += self.tab*(multiplier + 1) + "if not " + self.choose_def(condition) + ":\n" + self.tab*(multiplier + 2) + "break"
        
        self.instructions.append(instructoin)
        return instructoin


    def parce_while(self, node, multiplier):
        condition = self.tree.expr_list[node.condition_index]
        instructoin = multiplier*self.tab + "while " + self.choose_def(condition) + ":\n"
        for index in node.body:
            if index != "None":
                tmp_node = self.tree.expr_list[index]
                instructoin +=  (multiplier + 1)*self.tab + self.choose_def(tmp_node) + "\n"
        
        self.instructions.append(instructoin)
        return instructoin


    def parce_for(self, node, multiplier):
        condition = self.tree.expr_list[node.start_condition_index]
        tmp_cond = self.choose_def(condition)
        instructoin = multiplier*self.tab + tmp_cond + "\n" + multiplier*self.tab + "while " + tmp_cond.split()[0] + " <= " + str(node.end_number) + ":\n"
        for index in node.body:
            if index != "None":
                tmp_node = self.tree.expr_list[index]
                instructoin +=  (multiplier + 1)*self.tab + self.choose_def(tmp_node) + "\n"
        
        self.instructions.append(instructoin)
        return instructoin


    def parce_func_call(self, node, multiplier):
        instructoin = multiplier*self.tab + node.name + "("
        lengh = len(node.params)
        for i in range(lengh):
            if i == lengh - 1:
                instructoin += " " + node.params[i]
            elif i == 0:
                instructoin += node.params[i] + ","
            else:
                instructoin += " " + node.params[i] + ","
        
        instructoin += ")"
        return instructoin


    def parce_proc_call(self, node, multiplier):
        instructoin = multiplier*self.tab + node.name + "("
        lengh = len(node.params)
        for i in range(lengh):
            if i == lengh - 1:
                instructoin += " " + node.params[i]
            elif i == 0:
                instructoin += node.params[i] + ","
            else:
                instructoin += " " + node.params[i] + ","
        
        instructoin += ")"
        self.instructions.append(instructoin)
        return instructoin

            

    def parce_if(self, node, multiplier):
        instructoin = multiplier*self.tab + "if "
        condition = self.tree.expr_list[node.condition]
        instructoin += self.choose_def(condition) + ":" + "\n"
        if node.then_block is not None:
            for index in node.then_block:
                if index != "None":
                    tmp_node = self.tree.expr_list[index]
                    instructoin +=  (multiplier + 1)*self.tab + self.choose_def(tmp_node) + "\n"

        if node.else_block is not None:
            instructoin +=  multiplier*self.tab + "else:\n"
            for index in node.else_block:
                if index != "None":
                    tmp_node = self.tree.expr_list[index]
                    instructoin +=  (multiplier + 1)*self.tab + self.choose_def(tmp_node)

        self.instructions.append(instructoin)
        return instructoin



    def parce_assign(self, node, multiplier):
        instructoin = multiplier*self.tab + self.decrement_arr(node.ident) + " = "
        body = self.tree.expr_list[node.body_index]
        instructoin += self.choose_def(body)
        return instructoin
        


    def parce_additive(self, node):
        instruction = ""
        if node.left_index is not None:
            left = self.tree.expr_list[node.left_index]
            instruction += self.choose_def(left)

        if node.op is not None:
            instruction+= " " + node.op + " "

        if node.right_index is not None:
            right = self.tree.expr_list[node.right_index]
            instruction += self.choose_def(right)

        return instruction

    def parce_expr(self, node):
        instructon = ""
        if node.value1 is not None:
            instructon += self.decrement_arr(str(node.value1))

        if node.operator is not None:
            if node.operator == "function":
                func_call = self.tree.expr_list[node.value1]
                return self.choose_def(func_call)
                 
            else:
                instructon += " " + node.operator + " "

        if node.value2 is not None:
            instructon += self.decrement_arr(str(node.value2))

        return instructon

    def decrement_arr(self, string):
        if len(string.split("[")) > 1:
            res = string.split("[")
            num = int(res[1].split("]")[0]) - 1
            return res[0] + "[" + str(num) + "]"
        else:
            return string
            

    def choose_def(self, node, multiplier = 0):
        if node.classtype == "additive":
            return self.parce_additive(node)

        if node.classtype == "expr":
            return self.parce_expr(node)

        if node.classtype == "assign":
            return self.parce_assign(node, multiplier)

        if node.classtype == "function_call":
            return self.parce_func_call(node, multiplier)


    def write(self):
        f = open('output.py', 'w')
        for line in self.instructions:
            f.write(line + "\n")
        f.close()
