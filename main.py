# coding=utf8
import ply.lex as lex
import re

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
    'COMMA'
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
    'boolean': 'BOOL',
    'div': 'DIV',
    'mod': 'MOD',
    'not': 'NOT',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'true': 'TRUE',
    'false': 'FALSE',
    'for': 'FOR',
    'function': 'FUNCTION'
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

t_ignore = ' \r\t'

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

data = '''
program coprimes;
var M,N: integer;

function notcoprime(M,N: integer): boolean;

var
    K, i, myint: integer;
    Res: Boolean;
begin
    myint:=6;
    Res := false;
    if N > M then K := M else K := N;
    for i := 2 to K do
    Res := Res or (N mod i = 0) and (M mod i = 0);
    notcoprime := Res;
end;
'''

lexer.input(data)

while True:
    tok = lexer.token() # читаем следующий токен
    if not tok: break      # закончились печеньки
    print(tok)