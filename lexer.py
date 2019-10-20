# coding=utf8
import ply.lex as lex
from ast_nodes import *
import ply.yacc as yacc
import re
import tests

tokens = [
    'NUMBER', 
    'IDENT',
    'PLUS', 
    'ASSIGN',
    'LPAREN', 
    'RPAREN',
    'MUL',
    'LBRACE', 
    'RBRACE',
    'SEMICOLON',
    'GT', 
    'LT', 
    'GE', 
    'LE',
    'EQUALS',
    'MINUS',
    'FSLASH',
    'COLON',
    'SQUOTE',
    'QUOTE',
    'COMMA',
    'OR', 
    'AND',
]

reserved = {
    'while': 'WHILE',
    'do': 'DO',
    'write': 'WRITE',
    'writeln': 'WRITELN',
    'read': 'READ',
    'readln': 'READLN',
    'inc': 'INC',
    'dec': 'DEC',
    'abs': 'ABS',
    'begin': 'BEGIN',
    'end': 'END',
    'program': 'PROGRAM',
    'var': 'VAR',
    'char': 'CHAR',
    'integer': 'INT',
    'Boolean': 'BOOL',
    'div': 'DIV',
    'mod': 'MOD',
    'not': 'NOT',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'true': 'TRUE',
    'false': 'FALSE',
    'for': 'FOR',
    'function': 'FUNCTION',
    'to': 'TO'
}

tokens += reserved.values()

t_PLUS = r'\+'
t_ASSIGN = r'\:='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_MUL = r'\*'
t_LBRACE = r'\['
t_RBRACE = r'\]'
t_SEMICOLON = r';'
t_GT = r'>'
t_LT = r'<'
t_GE = r'>='
t_LE = r'<='
t_EQUALS = r'='
t_MINUS = r'\-'
t_FSLASH = r'/'
t_COLON = r'\:'
t_SQUOTE = r'\''
t_QUOTE = r'\"'
t_COMMA = r'\,'
t_OR = r'\|'
t_AND = r'&'

t_ignore = ' \r\t'

def t_IDENT(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_NUMBER(t):
    r'[-]?\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ccode_comment(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

# if __name__=="__main__":

#     lexer.input(tests.data)

#     while True:
#         tok = lexer.token() # читаем следующий токен
#         if not tok: break      # закончились печеньки
#         print(tok)

def p_expr_list(t):
    '''expr_list :
                 | expr_list statement'''
    if len(t) > 1:
        if t[2]:
            t[1].add_child(t[2])
        t[0] = t[1]
    else:
        t[0] = ExprListNode()

def p_statement(t):
    '''statement : expr_statement
                 | block
                 | selection_statement
                 | iteration_statement
                 | var_block'''
    t[0] = t[1]

def p_expr_statement(t):
    '''expr_statement : semicolons
                      | expression semicolons'''
    t[0] = t[1]

def p_block(t):
    'block : BEGIN expr_list END'
    t[0] = t[2]

def p_selection_statement(t):
    'selection_statement : if'
    t[0] = t[1]

def p_iteration_statement(t):
    '''iteration_statement : for
                           | while
                           | dowhile'''
    t[0] = t[1]

def p_expression(t):
    '''expression : logical_expression
                  | assignment
                  | function
                  | identification'''
    t[0] = t[1]

def p_logical_expression(t):
    'logical_expression : logical_or_expression'
    t[0] = t[1]


def p_logical_or_expression(t):
    '''logical_or_expression : logical_and_expression
                             | logical_or_expression OR logical_and_expression'''
    if len(t) > 2:
        t[0] = BinOpNode(BinOp(t[2]), t[1], t[3])
    else:
        t[0] = t[1]


def p_logical_and_expression(t):
    '''logical_and_expression : equality_expression
                              | logical_and_expression AND equality_expression'''
    if len(t) > 2:
        t[0] = BinOpNode(BinOp(t[2]), t[1], t[3])
    else:
        t[0] = t[1]

def p_equality_expression(t):
    '''equality_expression : relational_expression
                           | equality_expression EQUALS relational_expression'''
    if len(t) > 2:
        t[0] = BinOpNode(BinOp(t[2]), t[1], t[3])
    else:
        t[0] = t[1]

def p_relational_expression(t):
    '''relational_expression : additive_expression
                             | relational_expression GT additive_expression
                             | relational_expression LT additive_expression
                             | relational_expression GE additive_expression
                             | relational_expression LE additive_expression'''
    if len(t) > 2:
        t[0] = BinOpNode(BinOp(t[2]), t[1], t[3])
    else:
        t[0] = t[1]

def p_additive_expression(t):
    '''additive_expression : multiplicative_expression
                           | additive_expression PLUS multiplicative_expression
                           | additive_expression MINUS multiplicative_expression'''
    if len(t) > 2:
        t[0] = BinOpNode(BinOp(t[2]), t[1], t[3])
    else:
        t[0] = t[1]

def p_multiplicative_expression(t):
    '''multiplicative_expression : unary_expression
                                 | multiplicative_expression MUL unary_expression 
                                 | multiplicative_expression FSLASH unary_expression
                                 | multiplicative_expression DIV unary_expression
                                 | multiplicative_expression MOD unary_expression'''
    if len(t) > 2:
        t[0] = BinOpNode(BinOp(t[2]), t[1], t[3])
    else:
        t[0] = t[1]

def p_unary_expression(t):
    '''unary_expression : group
                        | NOT group
                        | MINUS group'''
    if len(t) > 2:
        t[0] = UnOpNode(UnOp(t[1]), t[2])
    else:
        t[0] = t[1]

def p_group(t):
    '''group : ident
             | LPAREN logical_expression RPAREN
             | number
             | bool_value'''
    if len(t) > 2:
        t[0] = t[2]
    else:
        t[0] = t[1]

def p_if(t):
    '''if : IF LPAREN expression RPAREN statement
          | IF LPAREN expression RPAREN statement ELSE statement'''

    if len(t) > 6:
        t[0] = IfNode(t[3], t[5], t[7])
    else:
        t[0] = IfNode(t[3], t[5])

def p_statement_assign(t):
    'assignment : ident ASSIGN logical_expression'
    t[0] = AssignNode(t[1], t[3])

def p_var_block(t):
    '''var_block : VAR identification_list
                 | VAR identification'''
    t[0] = VarIdentificationNode(t[2])

def p_identification_list(t):
    '''identification_list :
                           | identification_list identification'''
    if len(t) > 1:
        if t[2]:
            t[1].add_child(t[2])
        t[0] = t[1]
    else:
        t[0] = IdentificationListNode()

def p_identification(t):
    '''identification : ident COLON type'''
    t[0] = IdentificationNode(t[1], t[3])


def p_type(t):
    '''type : INT
            | BOOL
            | CHAR'''
    t[0] = t[1]

def p_for(t):
    '''for : FOR expression TO expression DO statement'''
    t[0] = ForNode(t[2], t[4], t[6])

def p_dowhile(t):
    '''dowhile : DO statement WHILE LPAREN expression RPAREN
               | DO statement WHILE expression'''
    if len(t) > 6:
        t[0] = DoWhileNode(t[2], t[5])
    else:
        t[0] = DoWhileNode(t[2], t[4])

def p_while(t):
    '''while : WHILE LPAREN expression RPAREN DO statement
             | WHILE expression DO statement'''
    if len(t) > 6:
        t[0] = WhileNode(t[3], t[6])
    else:
        t[0] = WhileNode(t[2], t[4])

def p_write(t):
    'write : WRITE LPAREN logical_expression RPAREN'
    t[0] = WriteNode(t[3])

def p_read(t):
    'read : READ LPAREN ident RPAREN'
    t[0] = ReadNode(t[3])

def p_function(t):
    '''function : read
                | write '''
    t[0] = t[1]

def p_ident(t):
    '''ident : IDENT'''
    t[0] = IdentNode(t[1])

def p_bool_value(t):
    '''bool_value : TRUE
                  | FALSE'''
    t[0] = BoolValueNode(t[1])

def p_expression_number(t):
    'number : NUMBER'
    t[0] = NumNode(t[1])

def p_semicolons(p):
    '''semicolons : SEMICOLON
                  | semicolons SEMICOLON'''

def p_error(t):
    print("Syntax error in input!")
    global prog
    prog = None

parser = yacc.yacc()

def build_tree(s):
    return parser.parse(s).tree