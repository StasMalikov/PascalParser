import ply.lex as lex
import my_ast_nodes
import ply.yacc as yacc

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
    'DOTDOT'
]

reserved = {
    'of': 'OF',
    'array': 'ARRAY',
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

t_DOTDOT = r'\.\.'
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

mytree = my_ast_nodes.Tree()

def t_IDENT(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


def t_NUMBER(t):
    r'\d+'
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
def p_identification_block(t):
    '''identification_block : VAR identification_list'''

def p_identification_list(t):
    '''identification_list : 
                           | identification_list identification'''

def p_identification(t):
    '''identification : ident_list COLON type SEMICOLON
                      | ident_list COLON type_arr SEMICOLON'''
    mytree.nodes.append(my_ast_nodes.IdentificationNode(mytree.idents,t[3]))
    mytree.idents = []

def p_ident_list(t):
    '''ident_list : ident_list COMMA ident
                  | ident COMMA ident
                  | ident'''
    if len(t) > 2:
        if len(mytree.idents)> 0:
            mytree.idents.append(t[3])
        else:
            mytree.idents.append(t[1])
            mytree.idents.append(t[3])

    else:
        mytree.idents.append(t[1])


def p_ident(t):
    '''ident : IDENT'''
    t[0]=t[1]

def p_type_arr(t):
    '''type_arr : ARRAY LBRACE NUMBER DOTDOT NUMBER RBRACE OF type'''
    t[0] = str(t[5]) +' '+ t[8]


def p_type(t):
    '''type : INT
            | BOOL
            | CHAR'''
    t[0]=t[1]

def p_error(t):
    print("Syntax error in input!")
    global prog
    prog = None



data = '''
      var
      a : integer;  
      b : char;
      c, d : array [1 .. 3] of integer;
    '''

parser = yacc.yacc()
parser.parse(data, debug=True)

mytree.print_tree()
