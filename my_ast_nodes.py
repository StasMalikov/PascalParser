class Tree:
    def __init__(self):
        self.nodes = []
        self.idents = []
    
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
                    print("│  └ " + node.values[j])
                else:
                    print("│  ├ " + node.values[j])

    def print_tree(self):
        print("...")
        attachment = 0
        for i in range(len(self.nodes)):
            if self.nodes[i].classtype == "ident":
                if i == len(self.nodes) - 1:
                    self.print_identification(self.nodes[i], attachment, True)
                else:
                    self.print_identification(self.nodes[i], attachment, False)
                

class Block:
    def __init__(self,body):
        self.body=body
        self.classtype = "block"

class IdentificationNode:
    def __init__(self, values, _type):
        self.classtype = "ident"
        self._type = _type
        self.values = values