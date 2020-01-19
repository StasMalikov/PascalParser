class CodeGenerator:
    def __init__(self, idents, tree):
        self.idents = idents
        self.tree = tree
        self.instructions = []
        self.tab = "    "


    def set_instructions(self):
        for node in self.tree.nodes:
            if node.type == "block_dot":
                self.parce_dot(node.body)

            # if node.type == "func_proc_block":
            #     self.parce_func_proc(node.body)
            
    def parce_func_proc(self, nodes):
        for node in nodes:
            if node.classtype == "function":
                self.parce_func(node)
            
            if node.classtype == "procedure":
                self.parce_proc(node)


    def parce_dot(self, nodes):
        for node in nodes:
            if node.classtype == "ident":
                continue

            if node.classtype == "assign":
                self.parce_assign(node)

            if node.classtype == "if_block":
                self.parce_if(node)

            if node.classtype == "procedure_call":
                self.parce_proc_call(node)

            if node.classtype == "for_block":
                self.parce_for(node)
                
            if node.classtype == "while_block":
                self.parce_while(node)

            if node.classtype == "do_while_block":
                self.parce_do_while(node)


    def parce_do_while(self, node):
        condition = self.tree.expr_list[node.condition_index]
        instructoin = "while True:\n"
        for index in node.body:
            if index != "None":
                tmp_node = self.tree.expr_list[index]
                instructoin +=  self.tab + self.choose_def(tmp_node) + "\n"

        instructoin += self.tab + "if not " + self.choose_def(condition) + ":\n" + self.tab*2 + "break"
        
        self.instructions.append(instructoin)
        return instructoin


    def parce_while(self, node):
        condition = self.tree.expr_list[node.condition_index]
        instructoin = "while " + self.choose_def(condition) + ":\n"
        for index in node.body:
            if index != "None":
                tmp_node = self.tree.expr_list[index]
                instructoin +=  self.tab + self.choose_def(tmp_node) + "\n"
        
        self.instructions.append(instructoin)
        return instructoin


    def parce_for(self, node):
        condition = self.tree.expr_list[node.start_condition_index]
        tmp_cond = self.choose_def(condition)
        instructoin = tmp_cond + "\n" + "while " + tmp_cond.split()[0] + " <= " + str(node.end_number) + ":\n"
        for index in node.body:
            if index != "None":
                tmp_node = self.tree.expr_list[index]
                instructoin +=  self.tab + self.choose_def(tmp_node) + "\n"
        
        self.instructions.append(instructoin)
        return instructoin


    def parce_func_call(self, node):
        instructoin = node.name + "("
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


    def parce_proc_call(self, node):
        instructoin = node.name + "("
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

            

    def parce_if(self, node):
        instructoin = "if "
        condition = self.tree.expr_list[node.condition]
        instructoin += self.choose_def(condition) + ":" + "\n"
        if node.then_block is not None:
            for index in node.then_block:
                if index != "None":
                    tmp_node = self.tree.expr_list[index]
                    instructoin +=  self.tab + self.choose_def(tmp_node) + "\n"

        if node.else_block is not None:
            instructoin += "else:\n"
            for index in node.else_block:
                if index != "None":
                    tmp_node = self.tree.expr_list[index]
                    instructoin +=  self.tab + self.choose_def(tmp_node)

        self.instructions.append(instructoin)
        return instructoin



    def parce_assign(self, node):
        instructoin = node.ident + " = "
        body = self.tree.expr_list[node.body_index]
        instructoin += self.choose_def(body)
        self.instructions.append(instructoin)
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
            instructon += str(node.value1)

        if node.operator is not None:
            if node.operator == "function":
                func_call = self.tree.expr_list[node.value1]
                return self.choose_def(func_call)
                 
            else:
                instructon += " " + node.operator + " "

        if node.value2 is not None:
            instructon += str(node.value2)

        return instructon
            

    def choose_def(self, node):
        if node.classtype == "additive":
            return self.parce_additive(node)

        if node.classtype == "expr":
            return self.parce_expr(node)

        if node.classtype == "assign":
            return self.parce_assign(node)

        if node.classtype == "function_call":
            return self.parce_func_call(node)


    def parce_func(self, node):
        pass

    def parce_proc(self, node):
        pass

    def write(self):
        f = open('output.py', 'w')
        for line in self.instructions:
            f.write(line + "\n")
        f.close()
