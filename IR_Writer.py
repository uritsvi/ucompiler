import IR

from abc import abstractmethod

IR_Writer_methods = {}


def _qualname(obj):
    return obj.__module__ + '.' + obj.__qualname__


def _declaring_class(obj):
    name = _qualname(obj)
    return name[:name.rfind('.')]


def _visitor_impl(self, arg, arg_2):
    method = IR_Writer_methods[(_qualname(type(self)), type(arg))]
    return method(self, arg, arg_2)


def writer(arg_type):
    def decorator(fn):
        declaring_class = _declaring_class(fn)
        IR_Writer_methods[(declaring_class, arg_type)] = fn

        return _visitor_impl

    return decorator


class IR_Writer:

    @abstractmethod
    @writer(IR.IR_Label)
    def write(self, label, context):
        pass

    @abstractmethod
    @writer(IR.IR_Function_SymbolTabel)
    def write(self, symbol_table, context):
        pass

    @abstractmethod
    @writer(IR.FreeVariable)
    def write(self, free_variable, context):
        pass

    @abstractmethod
    @writer(IR.FreeInteger)
    def write(self, free_integer, context):
        pass

    @abstractmethod
    @writer(IR.FreeTemp)
    def write(self, free_temp, context):
        pass

    @abstractmethod
    @writer(IR.DefTemp)
    def write(self, def_temp, context):
        pass

    @abstractmethod
    @writer(IR.IR_Assignment)
    def write(self, assignment, context):
        pass

    @abstractmethod
    @writer(IR.IR_AssignTemp)
    def write(self, assign_temp, context):
        pass

    @abstractmethod
    @writer(IR.IR_Integer)
    def write(self, integer, context):
        pass

    @abstractmethod
    @writer(IR.IR_Variable)
    def write(self, variable, context):
        pass

    @abstractmethod
    @writer(IR.IR_TempValue)
    def write(self, temp_value, context):
        pass

    @abstractmethod
    @writer(IR.IR_AddOperation)
    def write(self, add_operation, context):
        pass

    @abstractmethod
    @writer(IR.IR_SUbOperation)
    def write(self, sub_operation, context):
        pass

    @abstractmethod
    @writer(IR.IR_MulOperation)
    def write(self, mul_operation, context):
        pass

    @abstractmethod
    @writer(IR.IR_DevOperation)
    def writ(self, dev_operation, context):
        pass

    @abstractmethod
    @writer(IR.IR_DevRestOperation)
    def write(self, dev_res_operation, context):
        pass

    @abstractmethod
    @writer(IR.IR_Condition)
    def write(self, condition, context):
        pass

    @abstractmethod
    @writer(IR.IR_IfStatement)
    def write(self, if_statement, context):
        pass

    @abstractmethod
    @writer(IR.JumpStatement)
    def write(self, jump_statement, context):
        pass

    @abstractmethod
    @writer(IR.JumpLess)
    def write(self, jump_less, context):
        pass

    @abstractmethod
    @writer(IR.JumpGreater)
    def write(self, jump_greater, context):
        pass

    @abstractmethod
    @writer(IR.JumpEquals)
    def write(self, jump_equals, context):
        pass

    @abstractmethod
    @writer(IR.JumpNotEquals)
    def write(self, jump_not_equals, context):
        pass

    @abstractmethod
    @writer(IR.IR_Function)
    def write(self, function, context):
        pass

    @abstractmethod
    @writer(IR.IR_BasicBlock)
    def write(self, basic_block, context):
        pass

    @abstractmethod
    @writer(IR.IR_Print)
    def write(self, print_statement, context):
        pass

    @abstractmethod
    @writer(IR.AST_PrintString)
    def write(self, print_string, context):
        pass
