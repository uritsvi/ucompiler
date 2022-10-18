from abc import abstractmethod
from AST import *

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
    @visitor(AST_CodeBlock)
    def visit(self, code_block, context):
        pass

    @abstractmethod
    @visitor(AST_Value)
    def visit(self, code_block, context):
        pass

    @abstractmethod
    @visitor(AST_Integer)
    def visit(self, integer, context):
        pass

    @abstractmethod
    @visitor(AST_Variable)
    def visit(self, variable, context):
        pass

    @abstractmethod
    @visitor(AST_NewVariable)
    def visit(self, new_variable, context):
        pass

    @abstractmethod
    @visitor(AST_Expression)
    def visit(self, expression, context):
        pass

    @abstractmethod
    @visitor(AST_DefVar)
    def visit(self, def_var, context):
        pass

    @abstractmethod
    @visitor(AST_Assignment)
    def visit(self, assignment, context):
        pass

    @abstractmethod
    @visitor(Add_Operator)
    def visit(self, add_operator, context):
        pass

    @abstractmethod
    @visitor(Sub_Operator)
    def visit(self, sub_operator, context):
        pass

    @abstractmethod
    @visitor(Mul_Operator)
    def visit(self, mul_operator, context):
        pass

    @abstractmethod
    @visitor(Div_Operator)
    def visit(self, dev_operator, context):
        pass

    @abstractmethod
    @visitor(Remainder_Operator)
    def visit(self, dev_res_operator, context):
        pass

    @abstractmethod
    @visitor(LessOperatorAST)
    def visit(self, less_operator, context):
        pass

    @abstractmethod
    @visitor(GreaterOperatorAST)
    def visit(self, greater_operator, context):
        pass

    @abstractmethod
    @visitor(LessOperatorAST)
    def visit(self, equality_operator, context):
        pass

    @abstractmethod
    @visitor(AndOperator)
    def visit(self, and_operator, context):
        pass

    @abstractmethod
    @visitor(AST_IfStatement)
    def visit(self, if_statement, context):
        pass

    @abstractmethod
    @visitor(AST_WhileLoopStatement)
    def visit(self, while_loop_statement, context):
        pass

    @abstractmethod
    @visitor(AST_ElseStatement)
    def visit(self, else_statement, context):
        pass

    @abstractmethod
    @visitor(AST_Condition)
    def visit(self, condition, context):
        pass

    @abstractmethod
    @visitor(AST_ComplexCondition)
    def visit(self, condition, context):
        pass

    @abstractmethod
    @visitor(AST_Print)
    def visit(self, print_statement, context):
        pass

    @abstractmethod
    @visitor(AST_PrintString)
    def visit(self, print_statement, context):
        pass

    @abstractmethod
    @visitor(AST_Exit)
    def visit(self, exit_statement, context):
        pass

