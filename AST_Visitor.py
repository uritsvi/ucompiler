from abc import abstractmethod
import AST

AST_visitor_methods = {}


def _qualname(obj):
    return obj.__module__ + '.' + obj.__qualname__


def _declaring_class(obj):
    name = _qualname(obj)
    return name[:name.rfind('.')]


def _visitor_impl(self, arg, arg2):
    method = AST_visitor_methods[(_qualname(type(self)), type(arg))]
    return method(self, arg, arg2)


def visitor(arg_type):
    def decorator(fn):
        declaring_class = _declaring_class(fn)
        AST_visitor_methods[(declaring_class, arg_type)] = fn

        return _visitor_impl

    return decorator


class AST_Visitor:
    @abstractmethod
    @visitor(AST.AST_Program)
    def visit(self, program, context):
        pass

    @abstractmethod
    @visitor(AST.AST_Function)
    def visit(self, function, context):
        pass

    @abstractmethod
    @visitor(AST.AST_CodeBlock)
    def visit(self, code_block, context):
        pass

    @abstractmethod
    @visitor(AST.AST_Value)
    def visit(self, code_block, context):
        pass

    @abstractmethod
    @visitor(AST.AST_Integer)
    def visit(self, integer, context):
        pass

    @abstractmethod
    @visitor(AST.AST_ArrayCell)
    def visit(self, get_value_from_array, context):
        pass

    @abstractmethod
    @visitor(AST.AST_Variable)
    def visit(self, variable, context):
        pass

    @abstractmethod
    @visitor(AST.AST_Array)
    def visit(self, array, context):
        pass

    @abstractmethod
    @visitor(AST.AST_Expression)
    def visit(self, expression, context):
        pass

    @abstractmethod
    @visitor(AST.AST_DefVar)
    def visit(self, def_var, context):
        pass

    @abstractmethod
    @visitor(AST.AST_Assignment)
    def visit(self, assignment, context):
        pass

    @abstractmethod
    @visitor(AST.AST_Add_Operator)
    def visit(self, add_operator, context):
        pass

    @abstractmethod
    @visitor(AST.AST_Sub_Operator)
    def visit(self, sub_operator, context):
        pass

    @abstractmethod
    @visitor(AST.AST_Mul_Operator)
    def visit(self, mul_operator, context):
        pass

    @abstractmethod
    @visitor(AST.AST_Div_Operator)
    def visit(self, dev_operator, context):
        pass

    @abstractmethod
    @visitor(AST.AST_Remainder_Operator)
    def visit(self, dev_res_operator, context):
        pass

    @abstractmethod
    @visitor(AST.AST_LessOperator)
    def visit(self, less_operator, context):
        pass

    @abstractmethod
    @visitor(AST.AST_GreaterOperator)
    def visit(self, greater_operator, context):
        pass

    @abstractmethod
    @visitor(AST.AST_LessOperator)
    def visit(self, equality_operator, context):
        pass

    @abstractmethod
    @visitor(AST.AST_AndOperator)
    def visit(self, and_operator, context):
        pass

    @abstractmethod
    @visitor(AST.AST_IfStatement)
    def visit(self, if_statement, context):
        pass

    @abstractmethod
    @visitor(AST.AST_WhileLoopStatement)
    def visit(self, while_loop_statement, context):
        pass

    @abstractmethod
    @visitor(AST.AST_ElseStatement)
    def visit(self, else_statement, context):
        pass

    @abstractmethod
    @visitor(AST.AST_Condition)
    def visit(self, condition, context):
        pass

    @abstractmethod
    @visitor(AST.AST_ComplexCondition)
    def visit(self, condition, context):
        pass

    @abstractmethod
    @visitor(AST.AST_ReadLine)
    def visit(self, read_line_statement, context):
        pass

    @abstractmethod
    @visitor(AST.AST_Print)
    def visit(self, print_statement, context):
        pass

    @abstractmethod
    @visitor(AST.AST_PrintArray)
    def visit(self, print_array, context):
        pass

    @abstractmethod
    @visitor(AST.AST_PrintString)
    def visit(self, print_statement, context):
        pass

    @abstractmethod
    @visitor(AST.AST_Exit)
    def visit(self, exit_statement, context):
        pass

    @abstractmethod
    @visitor(AST.AST_FunctionCall)
    def visit(self, function_call, context):
        pass

    @abstractmethod
    @visitor(AST.AST_ReturnStatement)
    def visit(self, return_statement, context):
        pass

    @abstractmethod
    @visitor(AST.AST_FunctionCallReturnValue)
    def visit(self, function_call_return_value, context):
        pass
