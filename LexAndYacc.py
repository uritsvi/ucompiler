import ply.lex as lex
import ply.yacc as yacc

import Constance
import DataTypes
import Utils
import SymbolTable
import AST

tokens = ('int_32_keyword',
          'char_keyword',
          'void_keyword',

          'return',

          'if_keyword',
          'else_keyword',
          'while_keyword',

          'open_parenthesise',
          'close_parenthesise',

          'open_curly_brackets',
          'close_curly_brackets',

          'open_brackets',
          'close_brackets',

          'int_32_value',
          'char_value',
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
          'print_array',

          'read_line',

          'exit',

          'semicolon',
          'comma',

          'new_line')


def t_new_line(t):
    r"""\n+"""

    t.lexer.lineno += len(t.value)


def t_int_32_keyword(t):
    r"""int_32"""

    t.value = DataTypes.int_32()

    return t


def t_char_keyword(t):
    r"""char"""

    t.value = DataTypes.char()

    return t


def t_void_keyword(t):
    r"""void"""

    t.value = DataTypes.void()

    return t


def t_return(t):
    r"""return"""
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


def t_print_array(t):
    r"""@print_array"""
    return t


def t_print(t):
    r"""@print"""
    return t


def t_read_line(t):
    r"""@read_line"""
    return t


def t_exit(t):
    r"""@exit"""
    return t


t_open_parenthesise = r'\('
t_close_parenthesise = r'\)'

t_open_curly_brackets = r'\{'
t_close_curly_brackets = r'\}'

t_open_brackets = r'\['
t_close_brackets = r'\]'


def t_string(t):
    r"""\".+\""""

    t.value = t.value.split("\"", 2)[1]

    return t


def t_char_value(t):
    r"""'.'"""

    value = t.value.split("'", 2)
    value = value[1]

    AST_Integer = AST.AST_Integer(ord(value), DataTypes.char())
    t.value = AST_Integer

    return t


def t_int_32_value(t):
    r"""\d+"""

    AST_Integer = AST.AST_Integer(t.value, DataTypes.int_32())
    t.value = AST_Integer

    return t


t_name = r'\w+'

t_comma = r','
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
    """program : function_impl
                | program function_impl"""

    if len(p) == 2:
        program = AST.AST_Program()
        program.add_function(p[1])
        p[0] = program
    else:
        p[1].add_function(p[2])
        p[0] = p[1]


def p_return_statement(p):
    """return_statement : return return_value"""

    return_value = p[2]

    current_function =  \
        SymbolTable.FunctionsTabel.get_instance().get_current_function()

    current_function_prototype = \
        current_function.get_function_prototype()

    current_function_return_value_type = \
        current_function_prototype.get_return_value_type()

    res = \
        current_function_return_value_type.is_compatible_with(return_value)

    if not res:
        Utils.Utils.handle_compiler_error("Try's to return incompatible value from function" + " " +
                                          current_function_prototype.get_name() + " " + "in line" + " " +
                                          str(p.lexer.lineno))

    return_statement = AST.AST_ReturnStatement(return_value)

    p[0] = return_statement


def p_return_value(p):
    """return_value : value
                      | """

    if len(p) == 2:
        p[0] = p[1]
        return

    p[0] = None


def p_function_parameters(p):
    """function_impl_parameters :
                                  | data_type new_function_parameter_name
                                  | function_impl_parameters comma data_type new_function_parameter_name"""
    if len(p) == 1:
        parameters = SymbolTable.FunctionParameters()

    elif len(p) == 3:
        parameters = SymbolTable.FunctionParameters()

        new_parameter = \
            SymbolTable.FunctionParameter(p[2], p[1])

        parameters.add_parameter(new_parameter.get_name(), new_parameter)

    else:
        parameters = p[1]

        new_parameter = \
            SymbolTable.FunctionParameter(p[4], p[3])

        parameters.add_parameter(new_parameter.get_name(), new_parameter)

    p[0] = parameters


def p_function_prototype_start(p):
    """function_prototype_start : function_ret_type function_name"""

    function_prototype = \
        SymbolTable.SymbolTableFunctionPrototype(p[2], p[1])

    SymbolTable.FunctionsTabel.get_instance().\
        set_current_prototype(function_prototype)

    p[0] = function_prototype


def p_function_prototype(p):
    """function_prototype : function_prototype_start open_parenthesise function_impl_parameters close_parenthesise """

    function_prototype = p[1]
    function_name = function_prototype.get_name()

    function_prototype.set_parameters(p[3])

    function_table_name = \
        SymbolTable.FunctionsTabel.get_instance().map_function_name_to_table_name(function_name)

    symbol_table_function = \
        SymbolTable.SymbolTabelFunction(function_table_name, function_prototype)

    SymbolTable.FunctionsTabel.get_instance().add_function(symbol_table_function)

    p[0] = symbol_table_function


def p_function_call_parameters(p):
    """function_call_parameters :
                                | value
                                | function_call_parameters comma value"""

    if len(p) == 1:
        parameters = SymbolTable.FunctionCallParameters()
        p[0] = parameters
    elif len(p) == 2:
        parameters = SymbolTable.FunctionCallParameters()

        parameters.add_parameter(p[1])

        p[0] = parameters
    else:
        parameters = p[1]

        parameters.add_parameter(p[3])

        p[0] = parameters


def p_function_call(p):
    """function_call : function_name open_parenthesise function_call_parameters close_parenthesise"""

    function_name = p[1]
    parameters = p[3]

    if not parameters.is_matching_function_parameters_list(function_name):
        Utils.Utils.handle_compiler_error("function call dose not match parameters list in line" + " " + str(p.lexer.lineno))
        return

    function_table_name = \
        SymbolTable.FunctionsTabel.get_instance().get_function_tabel_name(function_name)

    function_call = \
        AST.AST_FunctionCall(function_table_name, parameters)

    p[0] = function_call


def p_function_impl(p):
    """function_impl :  function_prototype open_curly_brackets code_block close_curly_brackets"""

    function = p[1]
    code_block = p[3]

    ast_function = \
        AST.AST_Function(function, code_block)

    p[0] = ast_function


def p_function_ret_type(p):
    """function_ret_type : data_type
                           | void_keyword"""

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
    """statement : basic_block_command semicolon
                   | block"""

    p[0] = p[1]


def p_basic_block_command(p):
    """basic_block_command : def_var
                             | def_array
                             | int_assignment
                             | print_statement
                             | read_line_statement
                             | exit_statement
                             | function_call
                             | return_statement"""

    p[0] = p[1]


def p_block(p):
    """block : if_statement
               | while_statement"""

    p[0] = p[1]


def p_scope_start(p):
    """scope_start : open_curly_brackets"""

    SymbolTable.FunctionsTabel.get_instance().\
        get_current_function().push_table()

    p[0] = p[1]


def p_scope_end(p):
    """scope_end : close_curly_brackets"""

    SymbolTable.FunctionsTabel.get_instance(). \
        get_current_function().pop_table()

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

    AST_condition = AST.AST_ComplexCondition(p[1], AST.AST_OrOperator(), p[3])
    p[0] = AST_condition


def p_and_condition(p):
    """and_condition : condition and_operator simple_condition"""

    AST_condition = AST.AST_ComplexCondition(p[1], AST.AST_AndOperator(), p[3])
    p[0] = AST_condition


def p_condition_in_parenthesise(p):
    """condition_in_parenthesise : open_parenthesise condition close_parenthesise"""

    p[0] = p[2]


def p_les_condition(p):
    """les_condition : expression less_operator expression"""

    AST_Condition = AST.AST_Condition(p[1], AST.AST_LessOperator(), p[3])
    p[0] = AST_Condition


def p_greater_condition(p):
    """grater_condition : expression greater_operator expression"""

    AST_Condition = AST.AST_Condition(p[1], AST.AST_GreaterOperator(), p[3])
    p[0] = AST_Condition


def p_equality_condition(p):
    """equality_condition : expression equality_operator expression"""

    AST_Condition = AST.AST_Condition(p[1], AST.AST_EqualityOperator(), p[3])
    p[0] = AST_Condition


def p_not_equals_condition(p):
    """not_equals_condition : expression not_equals_operator expression"""
    AST_Condition = AST.AST_Condition(p[1], AST.AST_NotEqualsOperator(), p[3])
    p[0] = AST_Condition


def p_if_statement(p):
    """if_statement : if_keyword open_parenthesise condition close_parenthesise scope else_statement
                      | if_keyword open_parenthesise condition close_parenthesise scope"""

    if len(p) == 7:
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


def p_data_type(p):
    """data_type : int_32_keyword
                   | char_keyword"""

    p[0] = p[1]


def p_def_var(p):
    """def_var : data_type new_var_name
                 | data_type new_var_name equals_operator value"""

    data_type = p[1]
    var = AST.AST_Variable(p[2], data_type)

    SymbolTable.FunctionsTabel.get_instance().get_current_tabel().\
        add_var(var.get_name(), data_type)

    if len(p) == 3:
        AST_assignment = AST.AST_Assignment(var, AST.AST_Integer(0, data_type))
        AST_def_var = AST.AST_DefVar(p[2], AST_assignment)
    else:
        AST_assignment = AST.AST_Assignment(var, p[4])
        AST_def_var = AST.AST_DefVar(p[2], AST_assignment)

    p[0] = AST_def_var


def p_def_array(p):
    """def_array : data_type new_var_name open_brackets simple_int_value close_brackets"""

    array_len = p[4]

    if int(array_len.get_value()) > Constance.MAX_ARRAY_SIZE:
        Utils.Utils.handle_compiler_error("Try's to define an array of size greater than" + " " +
                                          str(Constance.MAX_ARRAY_SIZE) + " " + "in line" + " " + str(p.lexer.lineno))
        return

    data_type = p[1]
    new_var = p[2]

    data_type = DataTypes.Array(data_type, array_len)

    SymbolTable.FunctionsTabel.get_instance().get_current_tabel().\
        add_array(new_var, data_type)


def p_array_cell(p):
    """array_cell : array_name open_brackets value close_brackets"""

    array_name = p[1]
    index = p[3]

    AST_ArrayCell = \
        AST.AST_ArrayCell(array_name, index)

    p[0] = AST_ArrayCell


def p_int_assignment(p):
    """int_assignment : dest_var equals_operator value"""

    AST_assignment = AST.AST_Assignment(p[1], p[3])
    p[0] = AST_assignment


def p_simple_int_value(p):
    """simple_int_value : int_32_value
                          | char_value"""

    p[0] = p[1]


def p_int_value(p):
    """int_value : int_expression"""

    p[0] = p[1]


def p_dest_var(p):
    """dest_var : var_name
                  | array_cell"""

    p[0] = p[1]


def p_value(p):
    """value : int_value"""

    p[0] = p[1]


def p_function_call_value(p):
    """function_call_value : function_call"""

    function_call = p[1]
    function_name = function_call.get_name()

    function_data_type = SymbolTable.FunctionsTabel.get_instance().\
        get_function(function_name).get_function_prototype().get_return_value_type()

    AST_function_call_return_value = \
        AST.AST_FunctionCallReturnValue(function_call, function_data_type)

    p[0] = AST_function_call_return_value


def p_int_expression(p):
    """int_expression :  simple_int_value
                        | function_call_value
                        | array_cell
                        | int_expression_in_parenthesise
                        | var_name
                        | add_expression
                        | sub_expression
                        | mul_expression
                        | dev_expression
                        | dev_rest_expression"""

    value = p[1]

    res = value.get_data_type().\
        is_compatible_with(DataTypes.int_32())

    if not res:
        Utils.Utils.handle_compiler_error("Values are not compatible at line" + " " + str(p.lexer.lineno))

    p[0] = p[1]


def p_expression(p):
    """expression : int_expression"""

    p[0] = p[1]


def p_int_expression_in_parenthesise(p):
    """int_expression_in_parenthesise : open_parenthesise int_expression close_parenthesise"""

    p[0] = p[2]


def p_add_expression(p):
    """add_expression : expression add_operator expression"""

    AST_AddExpression = AST.AST_Expression(p[1], AST.AST_Add_Operator(), p[3])
    p[0] = AST_AddExpression

    p[0].set_data_type(p[1].get_data_type())


def p_sub_expression(p):
    """sub_expression : expression sub_operator expression"""

    AST_SubExpression = AST.AST_Expression(p[1], AST.AST_Sub_Operator(), p[3])
    p[0] = AST_SubExpression

    p[0].set_data_type(p[1].get_data_type())


def p_mul_expression(p):
    """mul_expression : expression mul_operator expression"""

    AST_MulExpression = AST.AST_Expression(p[1], AST.AST_Mul_Operator(), p[3])
    p[0] = AST_MulExpression

    p[0].set_data_type(p[1].get_data_type())


def p_dev_expression(p):
    """dev_expression : expression dev_operator expression"""

    AST_DevExpression = AST.AST_Expression(p[1], AST.AST_Div_Operator(), p[3])
    p[0] = AST_DevExpression

    p[0].set_data_type(p[1].get_data_type())


def p_dev_rest_expression(p):
    """dev_rest_expression : expression dev_rest_operator expression"""

    AST_DevRestExpression = AST.AST_Expression(p[1], AST.AST_Remainder_Operator(), p[3])
    p[0] = AST_DevRestExpression

    p[0].set_data_type(p[1].get_data_type())


def p_var_name(p):
    """var_name : name"""

    current_tabel =\
        SymbolTable.FunctionsTabel.get_instance().get_current_tabel()

    res = \
        current_tabel.var_accessible_in_scope(p[1])

    if not res:
        Utils.Utils.handle_compiler_error("Var " + p[1] + " dose not exist in current scope")
        return
    else:
        var_name = \
            current_tabel.get_var_name(p[1])

        var_data_type = \
            current_tabel.get_var(var_name)

    AST_var = AST.AST_Variable(var_name, var_data_type.get_data_type())
    p[0] = AST_var


def p_array_name(p):
    """array_name : name"""

    current_tabel =\
        SymbolTable.FunctionsTabel.get_instance().get_current_tabel()

    res = current_tabel\
        .array_accessible_in_scope(p[1])

    if not res:
        Utils.Utils.handle_compiler_error("Array " + p[1] + " dose not exist in current scope")
        return

    else:
        var_name = \
            current_tabel.get_var_name(p[1])

        var_data_type = \
            current_tabel.get_array(var_name)

    AST_var = AST.AST_Array(var_name, var_data_type)
    p[0] = AST_var


def p_new_function_parameter_name(p):
    """new_function_parameter_name : name"""

    new_name = p[1]

    table_name = SymbolTable.FunctionsTabel.get_instance().get_current_prototype().\
        map_arg_name_to_table_name(new_name)

    p[0] = table_name


def p_new_var_name(p):
    """new_var_name : name"""

    current_tabel =\
        SymbolTable.FunctionsTabel.get_instance().get_current_tabel()

    res = \
        current_tabel.var_exist_in_scope(p[1])

    if res:
        Utils.Utils.handle_compiler_error("Var " + p[1] + " already exist in current scope")
        return

    var_name = \
        current_tabel.map_var_name_to_symbol_tabel_name(p[1])

    p[0] = var_name


def p_function_name(p):
    """function_name : name"""

    p[0] = p[1]


def p_exit(p):
    """exit_statement : exit int_expression"""

    AST_ExitStatement = AST.AST_Exit(p[2])
    p[0] = AST_ExitStatement


def p_read_line_statement(p):
    """read_line_statement : read_line array_name comma simple_int_value"""

    p[0] = AST.AST_ReadLine(p[2].get_name(), p[4])


def p_print_statement(p):
    """print_statement : print_value_statement
                         | print_string_statement
                         | print_array_statement"""

    p[0] = p[1]


def p_print_array(p):
    """print_array_statement : print_array array_name"""

    p[0] = AST.AST_PrintArray(p[2].get_name())


def p_print_value(p):
    """print_value_statement : print value"""

    p[0] = AST.AST_Print(p[2].get_data_type().get_print_format(), p[2])


def p_print_string(p):
    """print_string_statement : print string"""

    p[0] = AST.AST_PrintString(p[2])


def p_error(p):
    Utils.Utils.handle_compiler_error("Failed to parse tokens in line" + " " +
                                      str(p.lineno) + " " + "token" + " " + "\"" + str(p.value) + "\"")

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
