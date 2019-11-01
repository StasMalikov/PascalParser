from cTreeParser import *
import os

s = '''

    int с :=  a + b;
    '''
print(*build_tree(s), sep=os.linesep)
