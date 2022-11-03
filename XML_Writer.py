from AST_Visitor import *

from xml.dom import minidom


class AST_XML_Program(AST_Visitor):

    __instance = None

    def __init__(self):
        self.__root = minidom.Document()

    def create_element(self, name):
        return self.__root.createElement(name)

    def write_xml(self, main_AST):
        code_block = self.visit(main_AST, None)

        self.__root.appendChild(code_block)

        string = self.__root.toprettyxml()
        return string

    @visitor(AST.AST_Program)
    def visit(self, program, context):
        xml_object = self.create_element("program")

        for function in program.get_functions():
            xml_object.appendChild(self.visit(function, None))

        return xml_object

    @visitor(AST.AST_Function)
    def visit(self, function, context):
        xml_object = self.create_element("function")
        xml_object.appendChild(self.create_element(function.get_name()))

        xml_object.appendChild(self.visit(function.get_code_block(), None))

        return xml_object

    @visitor(AST.AST_CodeBlock)
    def visit(self, code_block, context):
        statements = code_block.get_all_statements()
        xml_object = self.create_element("code block")

        for statement in statements:
            if statement is None:
                continue

            xml_object.appendChild(self.visit(statement, None))

        return xml_object

    @visitor(AST.AST_Integer)
    def visit(self, integer, context):
        xml_object = self.create_element("integer")
        integer_object = self.create_element("integer:" + str(integer.get_value()))

        xml_object.appendChild(integer_object)

        return xml_object

    @visitor(AST.AST_ArrayCell)
    def visit(self, get_value_from_array, context):
        xml_object = self.create_element("array cell")

        index = self.visit(get_value_from_array.get_index(), context)
        xml_object.appendChild(index)

        return xml_object

    @visitor(AST.AST_Variable)
    def visit(self, variable, context):
        xml_object = self.create_element("variable")
        name_object = self.create_element("name:" + variable.get_name())

        xml_object.appendChild(name_object)

        return xml_object

<<<<<<< HEAD
    @visitor(AST.AST_Expression)
=======
    @visitor(AST_NewVariable)
    def visit(self, new_variable, context):
        xml_object = self.create_element("new variable")
        name_object = self.create_element("name:" + new_variable.get_name())

        xml_object.appendChild(name_object)

        return xml_object

    @visitor(AST_Expression)
>>>>>>> parent of 475a605 (Added support for character type variables,)
    def visit(self, expression, context):
        xml_object = self.create_element("expression")

        xml_object.appendChild(self.visit(expression.get_expression_1(), None))
        xml_object.appendChild(self.visit(expression.get_operator(), None))
        xml_object.appendChild(self.visit(expression.get_expression_2(), None))

        return xml_object

    @visitor(AST.AST_DefVar)
    def visit(self, def_var, context):
        xml_object = self.create_element("def var")

        xml_object.appendChild(self.create_element(def_var.get_name()))
        xml_object.appendChild(self.visit(def_var.get_assignment(), None))

        return xml_object

    @visitor(AST.AST_Assignment)
    def visit(self, assignment, context):
        xml_object = self.create_element("assignment")

        xml_object.appendChild(self.visit(assignment.get_dest(), None))
        xml_object.appendChild(self.visit(assignment.get_value(), None))

        return xml_object

    @visitor(AST.AST_Add_Operator)
    def visit(self, add_operator, context):
        xml_object = self.create_element("add operator")
        return xml_object

    @visitor(AST.AST_Sub_Operator)
    def visit(self, sub_operator, context):
        xml_object = self.create_element("sub operator")
        return xml_object

    @visitor(AST.AST_Mul_Operator)
    def visit(self, mul_operator, context):
        xml_object = self.create_element("mul operator")
        return xml_object

    @visitor(AST.AST_Div_Operator)
    def visit(self, dev_operator, context):
        xml_object = self.create_element("dev operator")
        return xml_object

    @visitor(AST.AST_Remainder_Operator)
    def visit(self, dev_res_operator, context):
        xml_object = self.create_element("dev res operator")
        return xml_object

    @visitor(AST.AST_LessOperator)
    def visit(self, less_operator, context):
        xml_object = self.create_element("less operator")
        return xml_object

    @visitor(AST.AST_GreaterOperator)
    def visit(self, greater_operator, context):
        xml_object = self.create_element("greater operator")
        return xml_object

    @visitor(AST.AST_EqualityOperator)
    def visit(self, equality_operator, context):
        xml_object = self.create_element("equality operator")
        return xml_object

    @visitor(AST.AST_NotEqualsOperator)
    def visit(self, not_equals_operator, context):
        xml_object = self.create_element("not equals operator")
        return xml_object

    @visitor(AST.AST_AndOperator)
    def visit(self, and_operator, context):
        xml_object = self.create_element("and operator")
        return xml_object

    @visitor(AST.AST_OrOperator)
    def visit(self, and_operator, context):
        xml_object = self.create_element("or operator")
        return xml_object

    @visitor(AST.AST_IfStatement)
    def visit(self, if_statement, context):
        xml_object = self.create_element("if statement")

        xml_object.appendChild(self.visit(if_statement.get_condition(), None))
        xml_object.appendChild(self.visit(if_statement.get_then_part(), None))

        if if_statement.get_else_part() is not None:
            xml_object.appendChild(self.visit(if_statement.get_else_part(), None))

        return xml_object

    @visitor(AST.AST_WhileLoopStatement)
    def visit(self, while_loop_statement, context):
        xml_object = self.create_element("while loop statement")

        xml_object.appendChild(self.visit(while_loop_statement.get_condition(), None))
        xml_object.appendChild(self.visit(while_loop_statement.get_code_block(), None))

        return xml_object

    @visitor(AST.AST_ElseStatement)
    def visit(self, else_statement, context):
        xml_object = self.create_element("else statement")
        xml_object.appendChild(self.visit(else_statement.get_code_block(), None))

        return xml_object

    @visitor(AST.AST_Condition)
    def visit(self, condition, context):
        xml_object = self.create_element("condition")

        xml_object.appendChild(self.visit(condition.get_expression_1(), None))
        xml_object.appendChild(self.visit(condition.get_operator(), None))
        xml_object.appendChild(self.visit(condition.get_expression_2(), None))

        return xml_object

    @visitor(AST.AST_ComplexCondition)
    def visit(self, condition, context):
        xml_object = self.create_element("complex condition")

        xml_object.appendChild(self.visit(condition.get_condition_1(), None))
        xml_object.appendChild(self.visit(condition.get_operator(), None))
        xml_object.appendChild(self.visit(condition.get_condition_2(), None))

        return xml_object

    @abstractmethod
    @visitor(AST.AST_ReadLine)
    def visit(self, read_line_statement, context):
        xml_object = self.create_element("read line")

        return xml_object

    @visitor(AST.AST_Print)
    def visit(self, print_statement, context):
        xml_object = self.create_element("print")
        self.visit(print_statement.get_value(), None)

        return xml_object

    @visitor(AST.AST_PrintString)
    def visit(self, print_statement, context):
        xml_object = self.create_element("print string")

        return xml_object

    @visitor(AST.AST_PrintArray)
    def visit(self, print_array, context):
        xml_object = self.create_element("print array")

        return xml_object

    @visitor(AST.AST_Exit)
    def visit(self, exit_statement, context):
        xml_object = self.create_element("exit statement")

        xml_object.appendChild(self.visit(exit_statement.get_exit_code(), None))

        return xml_object

    @visitor(AST.AST_FunctionCall)
    def visit(self, function_call, context):
        xml_object = self.create_element("function call")

        xml_object.appendChild(self.create_element(function_call.get_name()))

        return xml_object

    @visitor(AST.AST_ReturnStatement)
    def visit(self, return_statement, context):
        xml_object = self.create_element("return")
        return xml_object

    @visitor(AST.AST_FunctionCallReturnValue)
    def visit(self, function_call_return_value, context):
        xml_object = self.create_element("function return value")
        return xml_object
