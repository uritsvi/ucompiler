from abc import abstractmethod

import SymbolTable


class AST_Node:
    pass


class AST_Program(AST_Node):
    def __init__(self):
        self.__functions = []

    def add_function(self, function):
        self.__functions.append(function)

    def get_functions(self):
        return self.__functions


class AST_CodeBlock(AST_Node):
    def __init__(self):
        self.__statements = []

    def add_statement(self, statement):
        self.__statements.append(statement)

    def get_all_statements(self):
        return self.__statements


class AST_Value(AST_Node):

    @abstractmethod
    def get_data_type(self):
        pass

    @abstractmethod
    def write(self):
        pass


class AST_FunctionCallReturnValue(AST_Value):
    def __init__(self, function_call, function_return_data_type):
        self.__function_call = function_call
        self.__function_return_data_type = function_return_data_type

    def get_data_type(self):
        return self.__function_return_data_type

    def get_function_call(self):
        return self.__function_call

    def write(self):
        string = self.__function_call.get_name()
        return string


class AST_Integer(AST_Value):
    def __init__(self, value, data_type):
        self.__value = value
        self.__data_type = data_type

    def get_value(self):
        return self.__value

    def get_data_type(self):
        return self.__data_type

    def write(self):
        string = str(self.__value)
        return string


class AST_Variable(AST_Value):
    def __init__(self, name, data_type):
        self.__name = name
        self.__data_type = data_type

    def get_name(self):
        return self.__name

    def get_data_type(self):
        return self.__data_type

    def write(self):
        string = SymbolTable.FunctionsTable.get_instance().get_current_table().get_old_name(self.__name)
        return string


class AST_Array:
    def __init__(self, name, data_type):
        self.__name = name
        self.__data_type = data_type

    def get_name(self):
        return self.__name

    def get_data_type(self):
        return self.__data_type.get_data_type()

    def get_size(self):
        return self.__data_type.get_size()


class AST_ArrayCell(AST_Value):
    def __init__(self, array_name, index):
        self.__array_name = array_name
        self.__index = index
        self.__data_type = self.__array_name.get_data_type()

    def get_data_type(self):
        return self.__data_type

    def get_array_name(self):
        return self.__array_name

    def get_index(self):
        return self.__index

    def get_name(self):
        return self.__array_name.get_name()

    def write(self):
        string = self.__array_name + "[" + str(self.__index) + "]"


class AST_Expression(AST_Value):
    def __init__(self, expression_1, operator, expression_2):
        self.__expression_1 = expression_1
        self.__operator = operator
        self.__expression_2 = expression_2
        self.__data_type = None

    def get_expression_1(self):
        return self.__expression_1

    def get_operator(self):
        return self.__operator

    def get_expression_2(self):
        return self.__expression_2

    def get_data_type(self):
        return self.__data_type

    def set_data_type(self, data_type):
        self.__data_type = data_type

    def write(self):
        string = self.__expression_1.write() + self.__operator.write() + self.__expression_2.write()
        return string


class AST_DefVar(AST_Node):
    def __init__(self, name, assignment):
        self.__name = name
        self.__assignment = assignment

    def get_name(self):
        return self.__name

    def get_assignment(self):
        return self.__assignment


class AST_Assignment(AST_Node):
    def __init__(self, dest, value):
        self.__dest = dest
        self.__value = value

    def get_dest(self):
        return self.__dest

    def get_value(self):
        return self.__value


class AST_IfStatement(AST_Node):
    def __init__(self, condition, then_part, else_statement):
        self.__condition = condition
        self.__then_part = then_part
        self.__else_part = else_statement

    def get_condition(self):
        return self.__condition

    def get_then_part(self):
        return self.__then_part

    def get_else_part(self):
        return self.__else_part


class AST_ElseStatement(AST_Node):
    def __init__(self, code_block):
        self.__code_block = code_block

    def get_code_block(self):
        return self.__code_block


class AST_WhileLoopStatement(AST_Node):
    def __init__(self, condition, repeat_part):
        self.__condition = condition
        self.__code_block = repeat_part

    def get_condition(self):
        return self.__condition

    def get_code_block(self):
        return self.__code_block


class AST_Condition(AST_Node):
    def __init__(self, left_expression, operator, right_expression):
        self.__left_expression = left_expression
        self.__right_expression = right_expression
        self.__operator = operator

    def get_expression_1(self):
        return self.__left_expression

    def get_operator(self):
        return self.__operator

    def get_expression_2(self):
        return self.__right_expression

    def write(self):
        string = self.__left_expression.write() + " " + self.__operator.write() + " " + self.__right_expression.write()

        return string


class AST_ComplexCondition(AST_Node):
    def __init__(self, left_condition, operator, right_condition):
        self.__left_condition = left_condition
        self.__right_condition = right_condition
        self.__operator = operator

    def get_condition_1(self):
        return self.__left_condition

    def get_condition_2(self):
        return self.__right_condition

    def get_operator(self):
        return self.__operator


class AST_Operator(AST_Node):
    @abstractmethod
    def write(self):
        pass


class AST_MathOperator(AST_Operator):
    @abstractmethod
    def write(self):
        pass


class AST_Add_Operator(AST_MathOperator):
    def write(self):
        string = "+"
        return string


class AST_Sub_Operator(AST_MathOperator):
    def write(self):
        string = "-"
        return string


class AST_Mul_Operator(AST_MathOperator):
    def write(self):
        string = "*"
        return string


class AST_Div_Operator(AST_MathOperator):
    def write(self):
        string = "/"
        return string


class AST_Remainder_Operator(AST_Operator):
    def write(self):
        string = "%"
        return string


class AST_ConditionOperator(AST_Operator):
    @abstractmethod
    def write(self):
        pass


class AST_LessOperator(AST_ConditionOperator):
    def write(self):
        string = "<"
        return string


class AST_GreaterOperator(AST_ConditionOperator):
    def write(self):
        string = ">"
        return string


class AST_EqualityOperator(AST_ConditionOperator):
    def write(self):
        string = "=="
        return string


class AST_NotEqualsOperator(AST_ConditionOperator):
    def write(self):
        string = "!="
        return string


class AST_AndOperator(AST_ConditionOperator):
    def write(self):
        string = "&&"
        return string


class AST_OrOperator(AST_ConditionOperator):
    def write(self):
        string = "||"
        return string


class AST_ReadLine(AST_Node):
    def __init__(self, array_name, num_of_chars):
        self.__array_name = array_name
        self.__num_of_chars = num_of_chars

    def get_array_name(self):
        return self.__array_name

    def get_num_of_chars(self):
        return self.__num_of_chars


class AST_Print(AST_Node):
    def __init__(self, print_format, value):
        self.__value = value
        self.__print_format = print_format

    def get_value(self):
        return self.__value

    def get_print_format(self):
        return self.__print_format


class AST_PrintArray(AST_Node):
    def __init__(self, array_name):
        self.__array_name = array_name

    def get_array_name(self):
        return self.__array_name


class AST_PrintString(AST_Node):
    def __init__(self, string):
        self.__string = string

    def get_string(self):
        return self.__string


class AST_Exit(AST_Node):
    def __init__(self, exit_code):
        self.__exit_code = exit_code

    def get_exit_code(self):
        return self.__exit_code


class AST_Function(AST_Node):
    def __init__(self, symbol_table_function, code_block):
        self.__code_block = code_block
        self.__symbol_table_function = symbol_table_function

    def get_code_block(self):
        return self.__code_block

    def get_name(self):
        return self.__symbol_table_function.get_name()

    def get_all_tables(self):
        return self.__symbol_table_function.get_all_tables()

    def get_prototype(self):
        return self.__symbol_table_function.get_function_prototype()


class AST_FunctionCall(AST_Node):
    def __init__(self, name, parameters):
        self.__name = name
        self.__parameters = parameters

    def get_name(self):
        return self.__name

    def get_parameters(self):
        return self.__parameters


class AST_ReturnStatement(AST_Node):
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return self.__value