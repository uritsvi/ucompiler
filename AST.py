from abc import abstractmethod


class AST_Node:
    pass


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


class AST_Integer(AST_Value):
    def __init__(self, value, data_type):
        self.__value = value
        self.__data_type = data_type

    def get_value(self):
        return self.__value

    def set_data_type(self, data_type):
        self.__data_type = data_type

    def get_data_type(self):
        return self.__data_type


class AST_Variable(AST_Value):
    def __init__(self, name, data_type):
        self.__name = name
        self.__data_type = data_type

    def get_name(self):
        return self.__name

    def get_data_type(self):
        return self.__data_type


class AST_NewVariable(AST_Node):
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name


class AST_Expression(AST_Value):
    def __init__(self, expression_1, operator, expression_2):
        self.__expression_1 = expression_1
        self.__operator = operator
        self.__expression_2 = expression_2

    def get_expression_1(self):
        return self.__expression_1

    def get_operator(self):
        return self.__operator

    def get_expression_2(self):
        return self.__expression_2

    def get_data_type(self):
        pass


class AST_DefVar(AST_Node):
    def __init__(self, name, assignment):
        self.__name = name
        self.__assignment = assignment

    def get_name(self):
        return self.__name

    def get_assignment(self):
        return self.__assignment


class AST_Assignment(AST_Node):
    def __init__(self, name, value):
        self.__name = name
        self.__value = value

    def get_name(self):
        return self.__name

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
    pass


class AST_MathOperator(AST_Operator):
    pass


class Add_Operator(AST_MathOperator):
    pass


class Sub_Operator(AST_MathOperator):
    pass


class Mul_Operator(AST_MathOperator):
    pass


class Div_Operator(AST_MathOperator):
    pass


class Remainder_Operator(AST_Operator):
    pass


class AST_ConditionOperator(AST_Operator):
    pass


class LessOperatorAST(AST_ConditionOperator):
    pass


class GreaterOperatorAST(AST_ConditionOperator):
    pass


class EqualityOperatorAST(AST_ConditionOperator):
    pass


class NotEqualsOperatorAST(AST_ConditionOperator):
    pass


class AndOperator(AST_ConditionOperator):
    pass


class OrOperatorAST(AST_ConditionOperator):
    pass


class AST_Print(AST_Node):
    def __init__(self, print_format, var_name):
        self.__var_name = var_name
        self.__print_format = print_format

    def get_var_name(self):
        return self.__var_name

    def get_print_format(self):
        return self.__print_format


class AST_PrintString(AST_Node):
    def __init__(self, string):
        self.__string = string

    def get_string(self):
        return self.__string
