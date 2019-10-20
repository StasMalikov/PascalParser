import tests
import lexer
import os

print(lexer.build_tree(tests.data), sep=os.linesep)
