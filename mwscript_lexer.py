import ply.lex as lex

keywords = {
    'begin': 'BEGIN',
    'end': 'END',
    'if': 'IF',
    'endif': 'ENDIF',
    'else': 'ELSE',
    'elseif': 'ELSEIF',
    'while': 'WHILE',
    'endwhile': 'ENDWHILE',
    'return': 'RETURN',
    'set': 'SET',
    'to': 'TO',
    'short': 'SHORT',
    'long': 'LONG',
    'float': 'FLOAT',
}

#tokens = list(set(keywords.values()) + [
#    'IDENT', 'NUMBER', 'EQUALS', 'OPENPAREN', 'CLOSEPAREN'
#])

tokens = list(set(keywords.values()).union([
    'NUMBER', 'IDENT', 'STRING', 'EQUALS', 'OPENPAREN', 'CLOSEPAREN', 'NOTEQUAL', 'LT', 'LE', 'GT', 'GE', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ARROW', 'COMMA'
]))

#tokens = (
#    'BEGIN', 'END', 'IF', 'ENDIF', 'RETURN',
#    'SET', 'TO', 'IDENT', 'NUMBER', 'EQUALS',
#    'OPENPAREN', 'CLOSEPAREN',
#)

t_ignore = ' \t'

t_BEGIN = r'begin'
t_END = r'end'
t_IF = r'if'
t_ENDIF = r'endif'
t_ELSE = r'else'
t_ELSEIF = r'elseif'
t_WHILE = r'while'
t_ENDWHILE = r'endwhile'
t_RETURN = r'return'
t_SET = r'set'
t_TO = r'to'
t_EQUALS = r'=='
t_OPENPAREN = r'\('
t_CLOSEPAREN = r'\)'
t_NOTEQUAL = r'!='
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ARROW = r'\->'
t_COMMA = r','
t_SHORT = r'short'
t_LONG = r'long'
t_FLOAT = r'float'


#def t_IDENT(t):
#    r'[A-Za-z_][A-Za-z0-9_]*'
#    return t

def t_IDENT(t):
    r'[A-Za-z_][A-Za-z0-9_\.]*'
    #r'[A-Za-z0-9_][A-Za-z0-9_]*'
    t.type = keywords.get(t.value.lower(), 'IDENT')  # Use keyword if matched
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_STRING(t):
    r'"([^"\\]*(\\.[^"\\]*)*)"'
    t.value = t.value[1:-1]  # remove quotes
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

def t_comment(t):
    r';[^\n]*'
    pass  # skip comments

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
