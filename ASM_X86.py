import ASM

from enum import Enum
from typing import Final

import DataTypes
import Utils
from IR_Writer import *
import IR
import SymbolTable


class RegistersType(Enum):
    eax = 0
    ebx = 1
    ecx = 2
    edx = 3

    al = 4,
    bl = 5,
    cl = 6,
    dl = 7,

    esi = 8,
    edi = 9


class Register:

    def __init__(self):
        self.__size_in_bites = 4

    def get_part_of_register(self, size_in_bites):
        if size_in_bites == 1:
            return self._get_one_bite_part_of_register()
        else:
            return self._get_full_register_type()

    @abstractmethod
    def _get_one_bite_part_of_register(self):
        pass

    @abstractmethod
    def _get_full_register_type(self):
        pass

    def get_size_in_bites(self):
        return self.__size_in_bites


class eax_Register(Register):

    def _get_full_register_type(self):
        return RegistersType.eax

    def _get_one_bite_part_of_register(self):
        return RegistersType.al


class ebx_Register(Register):

    def _get_full_register_type(self):
        return RegistersType.ebx

    def _get_one_bite_part_of_register(self):
        return RegistersType.bl


class ecx_Register(Register):

    def _get_full_register_type(self):
        return RegistersType.ecx

    def _get_one_bite_part_of_register(self):
        return RegistersType.cl


class edx_Register(Register):

    def _get_full_register_type(self):
        return RegistersType.edx

    def _get_one_bite_part_of_register(self):
        return RegistersType.dl


class Registers:
    __instance = None

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = Registers()

        return cls.__instance

    def __init__(self):
        self.__free_registers = [RegistersType.eax,
                                 RegistersType.ebx,
                                 RegistersType.ecx,
                                 RegistersType.edx]

        self.__all_full_registers = {RegistersType.eax: eax_Register(),
                                     RegistersType.ebx: ebx_Register(),
                                     RegistersType.ecx: ecx_Register(),
                                     RegistersType.edx: edx_Register()}

        self.__all_equired_registers = []

    def get_free_register(self):
        if len(self.__free_registers) == 0:
            Utils.Utils.handle_compiler_error("Compiler error: empty registers list" + "\n")
            return

        register = self.__free_registers.pop()

        self.__all_equired_registers.append(register)

        return register

    def free_register(self, register):
        if register in self.__free_registers:
            return

        self.__free_registers.append(register)
        self.__all_equired_registers.remove(register)

    def get_register_class(self, register_type):
        return self.__all_full_registers[register_type]

    def get_all_equired_registers(self):
        return self.__all_equired_registers


class ASM_X86_Generator(ASM.ASM_Generator, IR_Writer):
    __data_types = {1: "BYTE", 4: "DWORD"}

    def __init__(self):

        super().__init__()

        self.__registers = Registers()

        """
        The div_temps will hold the values of the eax edx and ecx registers  
        because the idiv operation changes the values of these registers. 
        The result of the division will be stored in div_res
        """

        self.__div_temp_RES: Final[str] = "div_temp_res"

    @classmethod
    def __data_type_to_asm_data_type(cls, size_in_bites):
        data_type = cls.__data_types.get(size_in_bites)

        if data_type is None:
            Utils.Utils.handle_compiler_error("Compiler error: data type for size " +
                                              size_in_bites + " " + "is undefined")
            return None

        return data_type

    def gen(self, ir_program):
        before_program = ".386\n" \
                         ".model flat,stdcall\n" \
                         "option casemap:none\n" \
                         "includelib \masm32\lib\kernel32.lib\n" \
                         "includelib C:\masm32\lib\masm32.lib\n" \
                         "include C:\masm32\include\masm32rt.inc\n" \
                         ".code\n" \
                         "start:\n" \

        after_program = "end start\n"

        context = ASM.Context()

        context.push_string()

        context.append_string(before_program)

        context.append_string(self.__write_call_to_main() + "\n")
        context.append_string(self.__write_exit(0) + "\n")

        self.write(ir_program, context)

        context.append_string(after_program)

        return context.pop_string()

    @classmethod
    def __write_call_to_main(cls):
        main_function_name = \
            SymbolTable.FunctionsTabel.get_instance().get_function_tabel_name("main")

        if main_function_name is None:
            Utils.Utils.handle_compiler_error("Every program needs to contains a main function entry")

        call_to_main = \
            cls.__write_call(main_function_name)

        return call_to_main

    @classmethod
    def __write_parameters(cls, parameters):
        string = ""

        for parameter in parameters:
            string += ","
            string += parameter.get_name() + ":" + cls.__data_type_to_asm_data_type(parameter.get_data_type().
                                                                                    get_size_in_bites())

        return string

    @classmethod
    def __write_call(cls, proc_name):
        string = "call" + " " + proc_name
        return string

    @classmethod
    def __write_invoke(cls, proc_name):
        string = "invoke" + " " + proc_name
        return string

    @classmethod
    def __write_proc(cls, name, parameters, code):
        string = name + " " + "proc" + " " + cls.__write_parameters(parameters) + "\n" + code + "ret" + "\n" + \
                 name + " " + "endp" + "\n"
        return string

    @classmethod
    def __write_xor(cls, dest, src):
        string = "xor" + " " + dest + "," + src
        return string

    @classmethod
    def __write_def_var(cls, name, data_type):
        string = "LOCAL" + " " + name + ":" + data_type
        return string

    @classmethod
    def __write_def_array(cls, name, data_type, size):
        string = "LOCAL" + " " + name + "[" + str(size) + "]" + ":" + data_type
        return string

    @classmethod
    def __write_var_name(cls, name):
        return name

    @classmethod
    def __write_assign_local_var(cls, name, value):
        string = cls.__write_mov(name, value)
        return string

    @classmethod
    def __write_mov_to_register(cls, register_name, value):
        string = cls.__write_mov(register_name, value)
        return string

    @classmethod
    def __write_mov(cls, dest, source):
        string = "mov" + " " + dest + "," + source
        return string

    @classmethod
    def __write_add(cls, dest_register_name, src_register_name):
        string = "add" + " " + dest_register_name + "," + src_register_name
        return string

    @classmethod
    def __write_sub(cls, dest_register_name, src_register_name):
        string = "sub" + " " + dest_register_name + "," + src_register_name
        return string

    @classmethod
    def __write_imul(cls, dest_register_name, src_register_name):
        string = "imul" + " " + dest_register_name + "," + src_register_name
        return string

    @classmethod
    def __write_idiv(cls, src_register_name):
        string = "cdq" + "\n" + \
                 "idiv" + " " + src_register_name
        return string

    @classmethod
    def __write_cmp(cls, register_1_name, register_2_name):
        string = "cmp" + " " + register_1_name + "," + register_2_name
        return string

    @classmethod
    def __write_label(cls, label_name):
        string = label_name + ":"
        return string

    @classmethod
    def __write_jmp(cls, label_name):
        string = "jmp" + " " + label_name
        return string

    @classmethod
    def __write_je(cls, label_name):
        string = "je" + " " + label_name
        return string

    @classmethod
    def __write_jne(cls, label_name):
        string = "jne" + " " + label_name
        return string

    @classmethod
    def __write_jl(cls, label_name):
        string = "jl" + " " + label_name
        return string

    @classmethod
    def __write_jg(cls, label_name):
        string = "jg" + " " + label_name
        return string

    @classmethod
    def __write_read_line(cls, array_name, num_of_chars):
        string = "invoke StdIn" + "," + " " + "addr" + " " + array_name + "," + str(num_of_chars)
        return string

    @classmethod
    def __write_print(cls, print_format, var_name):
        string = "printf" + "(" + print_format + "," + var_name + ")"
        return string

    @classmethod
    def __write_print_array(cls, array_name):
        string = "printf" + "(" + "\"%s\\n\"" + "," + "addr" + " " + array_name + ")"
        return string

    @classmethod
    def __write_print_string(cls, string):
        string = "printf" + "(" + "\"" + string + "\"" + ")"
        return string

    @classmethod
    def __write_exit(cls, exit_code):
        string = "invoke ExitProcess" + "," + str(exit_code)
        return string

    @classmethod
    def __write_array_cell(cls, array_name, index):
        string = \
            array_name + "[" + str(index) + "]"

        return string

    @classmethod
    def __write_push_to_stack(cls, src):
        string = \
            "push" + " " + src

        return string

    @classmethod
    def __write_pop(cls, dest):
        string = \
            "pop" + " " + dest

        return string

    @classmethod
    def __write_ret(cls):
        string = \
            "ret"

        return string

    @classmethod
    def __write_pass_parameter_to_proc(cls, value):

        string = \
            cls.__write_push_to_stack(value)

        return string

    def __write_push_state(self):
        equired_registers = \
            self.__registers.get_all_equired_registers()

        string = ""

        for register in equired_registers:
            string += \
                self.__write_push_to_stack(register.name) + "\n"

        return string

    def __write_pop_state(self):
        equired_registers = \
            self.__registers.get_all_equired_registers()

        equired_registers.reverse()

        string = ""

        for register in equired_registers:
            string += \
                self.__write_pop(register.name) +"\n"

        return string

    @writer(IR.IR_Program)
    def write(self, program, context):
        all_functions = program.get_all_functions()

        for function in all_functions:
            self.write(function, context)

    @writer(IR.IR_Function)
    def write(self, function, context):
        context.push_string()

        symbol_table = function.get_symbol_table()
        all_basic_blocks = function.get_all_basic_blocks()

        self.write(symbol_table, context)

        for basic_block in all_basic_blocks:
            self.write(basic_block, context)

        code = context.pop_string()

        function_prototype = \
            function.get_function_prototype()

        string = self.__write_proc(function.get_name(),
                                   function_prototype.get_parameters().get_all_parameters(),
                                   code)

        context.append_string(string)

        return string

    @writer(IR.IR_Label)
    def write(self, label, context):
        string = \
            self.__write_label(label.get_name()) + "\n"

        context.append_string(string)

    @writer(IR.IR_SymbolTabel)
    def write(self, symbol_table, context):
        string = ""

        symbol_tabel_vars = symbol_table.get_all_vars()

        symbol_tabel_vars[self.__div_temp_RES] = \
            (SymbolTable.Var(self.__div_temp_RES, DataTypes.int_32()))

        arrays = symbol_table.get_all_arrays()

        for var in symbol_tabel_vars.values():
            string += self.__write_def_var(var.get_name(),
                                           self.__data_type_to_asm_data_type
                                           (var.get_data_type().get_size_in_bites())) + "\n"

        for array in arrays.values():
            string += self.__write_def_array(array.get_name(),
                                             self.__data_type_to_asm_data_type
                                             (array.get_data_type().get_size_in_bites()),
                                             str(self.write(array.get_size(), context))) + "\n"

        context.append_string(string)

    @writer(IR.IR_FreeVariable)
    def write(self, free_variable, context):
        pass

    @writer(IR.IR_ArrayCell)
    def write(self, get_value_from_array, context):
        context.set_data_size(get_value_from_array.get_index().get_data_type().get_size_in_bites())

        string = \
            self.__write_array_cell(get_value_from_array.get_ir_array().get_name(),
                                    self.write(get_value_from_array.get_index(), context))

        return string

    @writer(IR.IR_FreeInteger)
    def write(self, free_integer, context):
        pass

    @writer(IR.IR_FreeTemp)
    def write(self, free_temp, context):
        self.__registers.free_register(free_temp.get_temp().get_value())

    @writer(IR.IR_DefTemp)
    def write(self, def_temp, context):
        register = self.__registers.get_free_register()
        def_temp.get_temp().set_value(register)

    @writer(IR.IR_DefReturnFromFunctionValueTemp)
    def write(self, def_return_from_value_function_temp, context):
        register = RegistersType.eax
        def_return_from_value_function_temp.get_temp().set_value(register)

    @writer(IR.IR_Assignment)
    def write(self, assignment, context):

        dest = self.write(assignment.get_dest(), context)

        var = assignment.get_dest()
        context.set_data_size(var.get_data_type().get_size_in_bites())

        src = self.write(assignment.get_value(), context)

        string = \
            self.__write_assign_local_var(dest,
                                          src) + "\n"
        context.append_string(string)

    @writer(IR.IR_AssignTemp)
    def write(self, assign_temp, context):
        var_size_in_bites = assign_temp.get_value().get_data_type().get_size_in_bites()

        register_enum = assign_temp.get_temp().get_value()

        register = Registers.get_instance().get_register_class(register_enum)

        part_of_register = register.get_part_of_register(var_size_in_bites)

        string = ""

        if var_size_in_bites < register.get_size_in_bites():
            string += \
                self.__write_xor(register_enum.name, register_enum.name) + "\n"

        context.set_data_size(var_size_in_bites)

        string += \
            self.__write_mov_to_register(part_of_register.name,
                                         self.write(assign_temp.get_value(), context)) + "\n"

        context.append_string(string)

    @writer(IR.IR_Integer)
    def write(self, integer, context):
        return str(integer.get_value())

    @writer(IR.IR_Variable)
    def write(self, variable, context):
        return variable.get_value()

    @writer(IR.IR_TempValue)
    def write(self, temp_value, context):
        return Registers.get_instance().get_register_class(temp_value.get_value()).\
            get_part_of_register(context.get_data_size()).name

    @writer(IR.IR_AddOperation)
    def write(self, add_operation, context):
        context.set_data_size(add_operation.get_src_temp().get_data_type().get_size_in_bites())

        string =\
            self.__write_add(self.write(add_operation.get_dest_temp(), context),
                             self.write(add_operation.get_src_temp(), context)) + "\n"

        context.append_string(string)

    @writer(IR.IR_SUbOperation)
    def write(self, sub_operation, context):
        context.set_data_size(sub_operation.get_src_temp().get_data_type().get_size_in_bites())

        string = \
            self.__write_sub(self.write(sub_operation.get_dest_temp(), context),
                             self.write(sub_operation.get_src_temp(), context)) + "\n"

        context.append_string(string)

    @writer(IR.IR_MulOperation)
    def write(self, mul_operation, context):
        context.set_data_size(mul_operation.get_dest_temp().get_data_type().get_size_in_bites())

        string = \
            self.__write_imul(self.write(mul_operation.get_dest_temp(), context),
                              self.write(mul_operation.get_src_temp(), context)) + "\n"

        context.append_string(string)

    @writer(IR.IR_DivRestOperation)
    def write(self, div_rest_operation, context):
        eax_register = RegistersType.eax
        ebx_register = RegistersType.ebx
        edx_register = RegistersType.edx
        string = ""

        string += \
            self.__write_push_state()

        string += \
            self.__write_mov_to_register(eax_register.name,
                                         div_rest_operation.get_dest_temp().get_value().name) + "\n"

        string += \
            self.__write_mov_to_register(ebx_register.name,
                                         self.write(div_rest_operation.get_src_temp(), context)) + "\n"

        string += \
            self.__write_idiv(ebx_register.name) + "\n"

        string += \
            self.__write_assign_local_var(self.__div_temp_RES, edx_register.name) + "\n"

        string += \
            self.__write_pop_state()

        string += self.__write_mov_to_register(div_rest_operation.get_dest_temp().get_value().name,
                                               self.__div_temp_RES) + "\n"

        context.append_string(string)

    @writer(IR.IR_DivOperation)
    def writ(self, div_operation, context):
        eax_register = RegistersType.eax
        ebx_register = RegistersType.ebx

        string = ""

        string += \
            self.__write_push_state()

        string += \
            self.__write_mov_to_register(eax_register.name,
                                         div_operation.get_dest_temp().get_value().name) + "\n"

        string += \
            self.__write_mov_to_register(ebx_register.name,
                                         self.write(div_operation.get_src_temp(), context)) + "\n"

        string += \
            self.__write_idiv(ebx_register.name) + "\n"

        string += \
            self.__write_assign_local_var(self.__div_temp_RES, eax_register.name) + "\n"

        string += \
            self.__write_pop_state()

        string += self.__write_mov_to_register(div_operation.get_dest_temp().get_value().name,
                                               self.__div_temp_RES) + "\n"

        context.append_string(string)

    @writer(IR.IR_Condition)
    def write(self, condition, context):
        string = \
            self.__write_cmp(condition.get_expression_1().get_value().name,
                             condition.get_expression_2().get_value().name) + "\n"

        context.append_string(string)

    @writer(IR.IR_IfStatement)
    def write(self, if_statement, context):

        condition = if_statement.get_condition()
        self.write(condition, context)

        self.write(if_statement.get_jump_to_than_part(), context)
        self.write(if_statement.get_jump_to_else_part(), context)

    @writer(IR.IR_Jump)
    def write(self, jump, context):
        string = \
            self.__write_jmp(jump.get_label().get_name()) + "\n"

        context.append_string(string)

    @writer(IR.IR_JumpLess)
    def write(self, jump_less, context):
        string = \
            self.__write_jl(jump_less.get_label().get_name()) + "\n"

        context.append_string(string)

    @writer(IR.IR_JumpGreater)
    def write(self, jump_greater, context):
        string = \
            self.__write_jg(jump_greater.get_label().get_name()) + "\n"

        context.append_string(string)

    @writer(IR.IR_JumpEquals)
    def write(self, jump_equals, context):
        string = \
            self.__write_je(jump_equals.get_label().get_name()) + "\n"

        context.append_string(string)

    @writer(IR.IR_JumpNotEquals)
    def write(self, jump_not_equals, context):
        string = \
            self.__write_jne(jump_not_equals.get_label().get_name()) + "\n"

        context.append_string(string)

    @writer(IR.IR_BasicBlock)
    def write(self, basic_block, context):

        self.write(basic_block.get_label(), context)

        for statement in basic_block.get_all_statements():
            self.write(statement, context)

        if basic_block.get_jump_block() is not None:
            self.write(basic_block.get_jump_block(), context)

    @writer(IR.IR_ReadLine)
    def write(self, ir_read_line, context):

        string = \
            self.__write_read_line(ir_read_line.get_array_name(),
                                   self.write(ir_read_line.get_num_of_chars(), context)) + "\n"

        context.append_string(string)

    @writer(IR.IR_Print)
    def write(self, print_statement, context):

        string = \
            self.__write_print(print_statement.get_print_format(),
                               self.write(print_statement.get_var(), context)) + "\n"

        context.append_string(string)

    @writer(IR.IR_PrintArray)
    def write(self, print_array, context):

        string = \
            self.__write_print_array(print_array.get_array_name()) + "\n"

        context.append_string(string)

    @writer(IR.IR_PrintString)
    def write(self, print_string, context):

        string = \
            self.__write_print_string(print_string.get_string()) + "\n"

        context.append_string(string)

    @writer(IR.IR_Exit)
    def write(self, exit_statement, context):

        string = \
            self.__write_exit(self.write(exit_statement.get_exit_code(), context)) + "\n"

        context.append_string(string)

    @writer(IR.IR_FunctionCall)
    def write(self, function_call, context):

        string = \
            self.__write_call(function_call.get_name()) + "\n"

        context.append_string(string)

    @writer(IR.IR_ReturnFromFunction)
    def write(self, return_from_function, context):

        string = \
            self.__write_ret() + "\n"

        context.append_string(string)

    @writer(IR.IR_ReturnFromFunctionValueTemp)
    def write(self, return_from_function_value_temp, context):
        register = RegistersType.eax
        return register.name

    @writer(IR.IR_PassParameterToFunction)
    def write(self, function_call_parameters, context):

        string = \
            self.__write_pass_parameter_to_proc(self.write
                                                (function_call_parameters.get_value(), context)) + "\n"

        context.append_string(string)

    @writer(IR.IR_ReturnFromFunctionValue)
    def write(self, ir_return_from_function_value, context):
        temp = ir_return_from_function_value.get_dest_temp()
        return self.write(temp, context)

    @writer(IR.IR_PushState)
    def write(self, ir_push_state, context):
        string = \
            self.__write_push_state()

        context.append_string(string)

    @writer(IR.IR_PopState)
    def write(self, ir_pop_state, context):
        string = \
            self.__write_pop_state()

        context.append_string(string)
