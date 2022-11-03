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
    @writer(IR.IR_Program)
    def write(self, program, context):
        pass

    @abstractmethod
    @writer(IR.IR_Function)
    def write(self, function, context):
        pass

    @abstractmethod
    @writer(IR.IR_Label)
    def write(self, label, context):
        pass

    @abstractmethod
    @writer(IR.IR_SymbolTabel)
    def write(self, symbol_table, context):
        pass

    @abstractmethod
    @writer(IR.IR_FreeVariable)
    def write(self, free_variable, context):
        pass

    @abstractmethod
    @writer(IR.IR_FreeInteger)
    def write(self, free_integer, context):
        pass

    @abstractmethod
    @writer(IR.IR_FreeTemp)
    def write(self, free_temp, context):
        pass

    @abstractmethod
    @writer(IR.IR_DefTemp)
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
    @writer(IR.IR_ArrayCell)
    def write(self, get_value_from_array, context):
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
    @writer(IR.IR_DivOperation)
    def writ(self, dev_operation, context):
        pass

    @abstractmethod
    @writer(IR.IR_DivRestOperation)
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
    @writer(IR.IR_JumpStatement)
    def write(self, jump_statement, context):
        pass

    @abstractmethod
    @writer(IR.IR_JumpLess)
    def write(self, jump_less, context):
        pass

    @abstractmethod
    @writer(IR.IR_JumpGreater)
    def write(self, jump_greater, context):
        pass

    @abstractmethod
    @writer(IR.IR_JumpEquals)
    def write(self, jump_equals, context):
        pass

    @abstractmethod
    @writer(IR.IR_JumpNotEquals)
    def write(self, jump_not_equals, context):
        pass

    @abstractmethod
    @writer(IR.IR_BasicBlock)
    def write(self, basic_block, context):
        pass

    @abstractmethod
    @writer(IR.IR_ReadLine)
    def write(self, ir_read_line, context):
        pass

    @abstractmethod
    @writer(IR.IR_Print)
    def write(self, print_statement, context):
        pass

    @abstractmethod
    @writer(IR.IR_PrintArray)
    def write(self, print_array, context):
        pass

    @abstractmethod
    @writer(IR.IR_PrintString)
    def write(self, print_string, context):
        pass

    @abstractmethod
    @writer(IR.IR_Exit)
    def write(self, exit_statement, context):
        pass

    @abstractmethod
    @writer(IR.IR_FunctionCall)
    def write(self, function_call, context):
        pass

    @abstractmethod
    @writer(IR.IR_ReturnFromFunction)
    def write(self, return_from_function, context):
        pass

    @abstractmethod
    @writer(IR.IR_DefReturnFromFunctionValueTemp)
    def write(self, def_return_from_value_function_temp, context):
        pass

    @abstractmethod
    @writer(IR.IR_ReturnFromFunctionValueTemp)
    def write(self, return_from_function_value_temp):
        pass

    @abstractmethod
    @writer(IR.IR_PassParameterToFunction)
    def write(self, function_call_parameters, context):
        pass

    @abstractmethod
    @writer(IR.IR_ReturnFromFunctionValue)
    def write(self, ir_return_from_function_value, context):
        pass

    @abstractmethod
    @writer(IR.IR_PushState)
    def write(self, ir_push_state, context):
        pass

    @abstractmethod
    @writer(IR.IR_PopState)
    def write(self, ir_pop_state, context):
        pass
