import ply.lex as lex
import ply.yacc as yacc

import Utils
import SymbolTable
import AST

tokens = ('int_32_keyword',
          'if_keyword',
          'else_keyword',
          'while_keyword',

          'open_parenthesise',
          'close_parenthesise',

          'open_curly_brackets',
          'close_curly_brackets',

          'number',
          'string',

          'name',

          'equals_operator',

          'add_operator',
          'sub_operator',
          'mul_operator',
          'dev_operator',
          'dev_rest_operator',

          'equality_operator',
          'not_equals_operator',
          'greater_operator',
          'less_operator',

          'and_operator',
          'or_operator',

          'print',

          'semicolon',
          'new_line')


def t_new_line(t):
    r"""\n+"""

    Lex.get_instance().inc_line_number(len(t.value))


def t_int_32_keyword(t):
    r"""int_32"""
    return t


def t_if_keyword(t):
    r"""if"""
    return t


def t_else_keyword(t):
    r"""else"""
    return t


def t_while_keyword(t):
    r"""while"""
    return t


def t_print(t):
    r"""@print"""
    return t


t_open_parenthesise = r'\('
t_close_parenthesise = r'\)'

t_open_curly_brackets = r'\{'
t_close_curly_brackets = r'\}'

t_number = r'\d+'
t_string = r'\".+\"'

t_name = r'\w+'

t_semicolon = r';'

t_equals_operator = r'='

t_add_operator = r'\+'
t_sub_operator = r'\-'
t_mul_operator = r'\*'
t_dev_operator = r'/'

t_and_operator = r'&&'
t_or_operator = r'\|\|'

t_dev_rest_operator = r'%'

t_equality_operator = r'=='
t_not_equals_operator = r'!='
t_less_operator = r'<'
t_greater_operator = r'>'

t_ignore = " "


def t_error(t):
    Utils.Utils.handle_compiler_error(t.value + "Is not matching any token")


precedence = (
    ('left', 'add_operator', 'sub_operator'),
    ('left', 'mul_operator', 'dev_operator', 'dev_rest_operator'))


def p_program(p):
    """program : code_block"""

    p[0] = p[1]


def p_code_block(p):
    """code_block : statement
                    | code_block statement
                    | """

    if len(p) == 2:
        AST_code_block = AST.AST_CodeBlock()
        AST_code_block.add_statement(p[1])
    elif len(p) == 3:
        AST_code_block = p[1]
        AST_code_block.add_statement(p[2])
    else:
        AST_code_block = AST.AST_CodeBlock()

    p[0] = AST_code_block


def p_statement(p):
    """statement : basic_block_command
                   | block"""

    p[0] = p[1]


def p_basic_block_command(p):
    """basic_block_command : def_int semicolon
                             | int_assignment semicolon
                             | print_statement semicolon"""

    p[0] = p[1]


def p_block(p):
    """block : if_statement
               | while_statement"""

    p[0] = p[1]


def p_scope_start(p):
    """scope_start : open_curly_brackets"""

    SymbolTable.Tables.get_instance().push_table()

    p[0] = p[1]


def p_scope_end(p):
    """scope_end : close_curly_brackets"""

    SymbolTable.Tables.get_instance().pop_top_table()

    p[0] = p[1]


def p_scope(p):
    """scope : scope_start code_block scope_end"""

    p[0] = p[2]


def p_condition(p):
    """condition : simple_condition
                   | complex_condition"""

    p[0] = p[1]


def p_simple_condition(p):
    """simple_condition : les_condition
                        | grater_condition
                        | equality_condition
                        | not_equals_condition
                        | condition_in_parenthesise"""

    p[0] = p[1]


def p_complex_condition(p):
    """complex_condition : and_condition
                           | or_condition"""

    p[0] = p[1]


def p_or_condition(p):
    """or_condition : condition or_operator simple_condition"""

    AST_condition = AST.AST_ComplexCondition(p[1], AST.OrOperatorAST(), p[3])
    p[0] = AST_condition


def p_and_condition(p):
    """and_condition : condition and_operator simple_condition"""

    AST_condition = AST.AST_ComplexCondition(p[1], AST.AndOperator(), p[3])
    p[0] = AST_condition


def p_condition_in_parenthesise(p):
    """condition_in_parenthesise : open_parenthesise condition close_parenthesise"""

    p[0] = p[2]


def p_les_condition(p):
    """les_condition : expression less_operator expression"""

    AST_Condition = AST.AST_Condition(p[1], AST.LessOperatorAST(), p[3])
    p[0] = AST_Condition


def p_greater_condition(p):
    """grater_condition : expression greater_operator expression"""

    AST_Condition = AST.AST_Condition(p[1], AST.GreaterOperatorAST(), p[3])
    p[0] = AST_Condition


def p_equality_condition(p):
    """equality_condition : expression equality_operator expression"""

    AST_Condition = AST.AST_Condition(p[1], AST.EqualityOperatorAST(), p[3])
    p[0] = AST_Condition


def p_not_equals_condition(p):
    """not_equals_condition : expression not_equals_operator expression"""
    AST_Condition = AST.AST_Condition(p[1], AST.NotEqualsOperatorAST(), p[3])
    p[0] = AST_Condition


def p_if_statement(p):
    """if_statement : if_keyword open_parenthesise condition close_parenthesise scope else_statement
                      | if_keyword open_parenthesise condition close_parenthesise scope"""

    if len(p) is 7:
        AST_if_statement = AST.AST_IfStatement(p[3], p[5], p[6])
        p[0] = AST_if_statement
    else:
        AST_if_statement = AST.AST_IfStatement(p[3], p[5], None)
        p[0] = AST_if_statement


def p_else_statement(p):
    """else_statement : else_keyword scope"""

    AST_else_statement = AST.AST_ElseStatement(p[2])
    p[0] = AST_else_statement


def p_while_statement(p):
    """while_statement : while_keyword open_parenthesise condition close_parenthesise scope"""

    AST_while_statement = AST.AST_WhileLoopStatement(p[3], p[5])
    p[0] = AST_while_statement


def p_def_int(p):
    """def_int : int_32_keyword new_var_name
                 | int_32_keyword new_var_name equals_operator int_expression"""

    if len(p) == 3:
        AST_assignment = AST.AST_Assignment(p[2], AST.AST_Integer(0))
        AST_def_var = AST.AST_DefVar(p[2], AST_assignment)
    else:
        AST_assignment = AST.AST_Assignment(p[2], p[4])
        AST_def_var = AST.AST_DefVar(p[2], AST_assignment)

    p[0] = AST_def_var


def p_int_assignment(p):
    """int_assignment : var_name equals_operator expression"""

    AST_assignment = AST.AST_Assignment(p[1], p[3])
    p[0] = AST_assignment


def p_int_expression(p):
    """int_expression : int_value
                        | int_expression_in_parenthesise
                        | var_name
                        | add_expression
                        | sub_expression
                        | mul_expression
                        | dev_expression
                        | dev_rest_expression"""

    p[0] = p[1]


def p_expression(p):
    """expression : int_expression"""

    p[0] = p[1]


def p_int_expression_in_parenthesise(p):
    """int_expression_in_parenthesise : open_parenthesise int_expression close_parenthesise"""

    p[0] = p[2]


def p_add_expression(p):
    """add_expression : expression add_operator expression"""

    AST_AddExpression = AST.AST_Expression(p[1], AST.Add_Operator(), p[3])
    p[0] = AST_AddExpression


def p_sub_expression(p):
    """sub_expression : expression sub_operator expression"""

    AST_SubExpression = AST.AST_Expression(p[1], AST.Sub_Operator(), p[3])
    p[0] = AST_SubExpression


def p_mul_expression(p):
    """mul_expression : expression mul_operator expression"""

    AST_MulExpression = AST.AST_Expression(p[1], AST.Mul_Operator(), p[3])
    p[0] = AST_MulExpression


def p_dev_expression(p):
    """dev_expression : expression dev_operator expression"""

    AST_DevExpression = AST.AST_Expression(p[1], AST.Div_Operator(), p[3])
    p[0] = AST_DevExpression


def p_dev_rest_expression(p):
    """dev_rest_expression : expression dev_rest_operator expression"""

    AST_DevRestExpression = AST.AST_Expression(p[1], AST.Remainder_Operator(), p[3])
    p[0] = AST_DevRestExpression


def p_var_name(p):
    """var_name : name"""

    res = SymbolTable.Tables.get_instance().\
        get_current_table().var_accessible_in_scope(p[1])

    if not res:
        Utils.Utils.handle_compiler_error("Var " + p[1] + " dose not exist in current scope")
        return

    var_name = \
        SymbolTable.Tables.get_instance().get_current_table().get_var_name(p[1])

    AST_var = AST.AST_Variable(var_name)
    p[0] = AST_var


def p_new_var_name(p):
    """new_var_name : name"""

    res = SymbolTable.Tables.get_instance().\
        get_current_table().var_exist_in_scope(p[1])

    if res:
        Utils.Utils.handle_compiler_error("Var " + p[1] + " already exist in current scope")
        return

    var_name = \
        SymbolTable.Tables.get_instance().get_current_table().add_var(p[1])

    AST_new_var = AST.AST_NewVariable(var_name)
    p[0] = AST_new_var


def p_int_value(p):
    """int_value : number"""

    AST_Int = AST.AST_Integer(p[1])
    p[0] = AST_Int


def p_print_statement(p):
    """print_statement : print_var
                         | print_string"""

    p[0] = p[1]


def p_print_var(p):
    """print_var : print var_name"""

    p[0] = AST.AST_Print(p[2])


def p_print_string(p):
    """print_string : print string"""

    p[0] = AST.AST_PrintString(p[2])


def p_error(p):
    Utils.Utils.handle_compiler_error("Failed to parse tokens")

    p[0] = None


class Lex:
    __instance = None

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = Lex()

        return cls.__instance

    def __init__(self):
        self.__lex = lex.lex()
        self.__line_number = 0

    def parse_to_tokens(self, text):
        self.__lex.input(text)

    def inc_line_number(self, count):
        self.__line_number += count

    def get_current_line_number(self):
        return self.__line_number


class Yacc:
    __instance = None

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = Yacc()

        return cls.__instance

    def __init__(self):
        self.__parser = yacc.yacc()

    def pars(self, text):
        AST_code_block = self.__parser.parse(text)
        return AST_code_block
