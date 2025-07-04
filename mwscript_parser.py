import ply.yacc as yacc
from mwscript_lexer import tokens

# Define precedence to resolve operator conflicts
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('nonassoc', 'LT', 'LE', 'GT', 'GE', 'EQUALS', 'NOTEQUAL'),
    ('left', 'ARROW'),  # Method calls have lower precedence than arithmetic
    ('right', 'UMINUS'),  # Unary minus has right associativity
)

def p_script(p):
    '''script : BEGIN IDENT statement_list END
              | BEGIN IDENT statement_list END IDENT'''
    p[0] = ('script', p[2], p[3])

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement_list_empty(p):
    'statement_list :'
    p[0] = []

def p_statement(p):
    '''statement : var_decl
                 | if_block
                 | while_block
                 | return_stmt
                 | set_stmt'''
    p[0] = p[1]

def p_statement_expr_wrapper(p):
    'statement : expression'
    p[0] = ('eval', p[1])

def p_var_decl(p):
    'var_decl : var_opt IDENT'
    p[0] = ('declare', p[1], p[2])

def p_var_opt(p):
    '''var_opt : SHORT
              | LONG
              | FLOAT'''
    p[0] = p[1]

def p_if_block(p):
    '''if_block : IF condition statement_list elseif_list else_opt ENDIF
                | IF check statement_list elseif_list else_opt ENDIF'''
    p[0] = ('if', p[2], p[3], p[4], p[5])

def p_elseif_list(p):
    '''elseif_list : elseif_list ELSEIF condition statement_list
                   | elseif_list ELSEIF check statement_list'''
    if len(p) == 5:
        p[0] = p[1] + [(p[3], p[4])]
    else:
        p[0] = []

def p_elseif_list_empty(p):
    'elseif_list :'
    p[0] = []

def p_else_opt(p):
    'else_opt : ELSE statement_list'
    p[0] = p[2]

def p_else_opt_empty(p):
    'else_opt :'
    p[0] = None

def p_while_block(p):
    '''while_block : WHILE condition statement_list ENDWHILE
                | WHILE check statement_list ENDWHILE'''
    p[0] = ('while', p[2], p[3])

def p_condition(p):
    '''condition : expression comp_op expression
                 | OPENPAREN expression comp_op expression CLOSEPAREN'''
    if len(p) == 4:
        p[0] = ('condition', p[1], p[2], p[3])
    else:
        p[0] = ('condition', p[2], p[3], p[4])

def p_check(p):
    '''check : OPENPAREN expression CLOSEPAREN'''
    p[0] = ('check', p[2], 'TRUE')

def p_comp_op(p):
    '''comp_op : EQUALS
               | NOTEQUAL
               | LT
               | LE
               | GT
               | GE'''
    p[0] = p[1]

def p_set_op(p):
    '''set_op : PLUS
              | MINUS
              | TIMES
              | DIVIDE'''
    p[0] = p[1]

def p_return_stmt(p):
    'return_stmt : RETURN'
    p[0] = ('return',)

def p_set_stmt(p):
    '''set_stmt : SET IDENT TO expression
                | SET STRING TO expression'''
    p[0] = ('set', p[2], p[4])

# Expression hierarchy - start with atoms, build up to complex expressions
def p_expression_atom(p):
    'expression : atom'
    p[0] = p[1]

def p_expression_binop(p):
    'expression : expression set_op expression'
    p[0] = ('calc', p[1], p[3])

def p_expression_method_call(p):
    'expression : expression ARROW IDENT expression_list'
    p[0] = ('callmethod', p[1], p[3], p[4])

def p_expression_function_call(p):
    'expression : IDENT OPENPAREN expression_list CLOSEPAREN'
    p[0] = ('call', p[1], p[3])

def p_expression_function_call_no_parens(p):
    '''expression : IDENT expression_list
                  | IDENT COMMA expression_list'''
    p[0] = ('call', p[1], p[2])

# Atom rules - the most basic expressions
def p_atom_number(p):
    'atom : NUMBER'
    p[0] = ('num', p[1])

def p_atom_string(p):
    'atom : STRING'
    p[0] = ('str', p[1])

def p_atom_var(p):
    'atom : IDENT'
    p[0] = ('var', p[1])

def p_atom_group(p):
    'atom : OPENPAREN expression CLOSEPAREN'
    p[0] = p[2]

def p_atom_uminus(p):
    'atom : MINUS atom %prec UMINUS'
    p[0] = ('neg', p[2])

# Expression list - for function arguments
def p_expression_list(p):
    '''expression_list : expression_list COMMA expression
                       | expression_list expression
                       | expression'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_expression_list_empty(p):
    'expression_list :'
    p[0] = []

def p_error(p):
    print("Syntax error at '%s'" % (p.value if p else 'EOF'))

parser = yacc.yacc() 