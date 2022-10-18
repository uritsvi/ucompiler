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
    dl = 7


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

    def get_free_register(self):
        return self.__free_registers.pop()

    def free_register(self, register):
        self.__free_registers.append(register)

    def get_register_class(self, register_type):
        return self.__all_full_registers[register_type]


class ASM_X86_Generator(ASM.ASM_Generator, IR_Writer):
    def __init__(self):

        super().__init__()

        self.__data_types = {1: "BYTE", 4: "DWORD"}
        self.__registers = Registers()
        self.__symbol_tabel = None

        """
        The div_temps will hold the values of the eax edx and ecx registers  
        because the idiv operation changes the values of these registers. 
        The result of the division will be stored in dev_res
        """

        self.__div_temp_1: Final[str] = "div_temp_1"
        self.__div_temp_2: Final[str] = "div_temp_2"
        self.__div_temp_3: Final[str] = "div_temp_3"
        self.__div_temp_RES: Final[str] = "div_temp_res"

    def __data_type_to_asm_data_type(self, size_in_bites):
        data_type = self.__data_types.get(size_in_bites)

        if data_type is None:
            Utils.Utils.handle_compiler_error("compiler error: data type for size " +
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
                         "call main\n" \
                         "main proc\n"

        after_program = "invoke ExitProcess, 0\n" \
                        "main endp\n" \
                        "end start\n"

        self.__symbol_tabel = ir_program.get_symbol_tabel()

        context = ASM.Context()

        context.append_string(before_program)

        self.write(self.__symbol_tabel, context)
        self.write(ir_program.get_main_function(), context)

        context.append_string(after_program)

        return context.poll_string()

    @classmethod
    def __write_xor(cls, dest, src):
        string = "xor" + " " + dest + "," + src
        return string

    @classmethod
    def __write_def_var(cls, name, data_type):
        string = "LOCAL" + " " + name + ":" + data_type
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
    def __write_idev(cls, src_register_name):
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
    def __write_print(cls, print_format, var_name):
        string = "printf" + "(" + print_format + "," + var_name + ")"
        return string

    @classmethod
    def __write_print_string(cls, string):
        string = "printf" + "(" + "\"" + string + "\"" + ")"
        return string

    @classmethod
    def __write_exit(cls, exit_code):
        string = "invoke ExitProcess" + "," + str(exit_code)
        return string

    @writer(IR.IR_Label)
    def write(self, label, context):
        string = \
            self.__write_label(label.get_name()) + "\n"

        context.append_string(string)

    @writer(IR.IR_Function_SymbolTabel)
    def write(self, symbol_table, context):
        string = ""

        vars = symbol_table.get_all_vars()

        vars[self.__div_temp_1] = (SymbolTable.Var(self.__div_temp_1, DataTypes.int_32()))
        vars[self.__div_temp_2] = (SymbolTable.Var(self.__div_temp_2, DataTypes.int_32()))
        vars[self.__div_temp_3] = (SymbolTable.Var(self.__div_temp_3, DataTypes.int_32()))
        vars[self.__div_temp_RES] = (SymbolTable.Var(self.__div_temp_RES, DataTypes.int_32()))

        for var in vars.values():
            string += self.__write_def_var(var.get_name(), self.__data_type_to_asm_data_type
                                          (var.get_data_type().get_size_in_bites())) + "\n"

        context.append_string(string)

    @writer(IR.FreeVariable)
    def write(self, free_variable, context):
        pass

    @writer(IR.FreeInteger)
    def write(self, free_integer, context):
        pass

    @writer(IR.FreeTemp)
    def write(self, free_temp, context):
        self.__registers.free_register(free_temp.get_temp().get_value())

    @writer(IR.DefTemp)
    def write(self, def_temp, context):
        register = self.__registers.get_free_register()
        def_temp.get_temp().set_value(register)

    @writer(IR.IR_Assignment)
    def write(self, assignment, context):
        context.set_data_size(self.__symbol_tabel.get_var(assignment.get_var_name()).
                              get_data_type().get_size_in_bites())

        string = \
            self.__write_assign_local_var(assignment.get_var_name(),
                                          self.write(assignment.get_value(), context)) + "\n"
        context.append_string(string)

    @writer(IR.IR_AssignTemp)
    def write(self, assign_temp, context):
        var_size_in_bites = assign_temp.get_value().get_data_type().get_size_in_bites()

        register_enum = assign_temp.get_temp().get_value()

        register = Registers.get_instance().get_register_class\
            (register_enum)\

        part_of_register = register.get_part_of_register(var_size_in_bites)

        string = ""

        if var_size_in_bites < register.get_size_in_bites():
            string += \
                self.__write_xor(register_enum.name, register_enum.name) + "\n"

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
        string =\
            self.__write_add(add_operation.get_dest_temp().get_value().name,
                             add_operation.get_src_temp().get_value().name) + "\n"

        context.append_string(string)

    @writer(IR.IR_SUbOperation)
    def write(self, sub_operation, context):
        string = \
            self.__write_sub(sub_operation.get_dest_temp().get_value().name,
                             sub_operation.get_src_temp().get_value().name) + "\n"

        context.append_string(string)

    @writer(IR.IR_MulOperation)
    def write(self, mul_operation, context):
        string = \
            self.__write_imul(mul_operation.get_dest_temp().get_value().name,
                              mul_operation.get_src_temp().get_value().name) + "\n"

        context.append_string(string)

    @abstractmethod
    @writer(IR.IR_DevRestOperation)
    def write(self, dev_rest_operation, context):
        eax_register = RegistersType.eax
        ecx_register = RegistersType.ecx
        edx_register = RegistersType.edx

        string = self.__write_assign_local_var(self.__div_temp_1,
                                               eax_register.name) + "\n"

        string += self.__write_assign_local_var(self.__div_temp_2,
                                                ecx_register.name) + "\n"

        string += self.__write_assign_local_var(self.__div_temp_3,
                                                edx_register.name) + "\n"

        string += self.__write_mov_to_register(eax_register.name,
                                               dev_rest_operation.get_dest_temp().get_value().name) + "\n"

        string += self.__write_mov_to_register(ecx_register.name,
                                               dev_rest_operation.get_src_temp().get_value().name) + "\n"

        string += self.__write_idev(ecx_register.name) + "\n"

        string += self.__write_assign_local_var(self.__div_temp_RES, edx_register.name) + "\n"

        string += self.__write_mov_to_register(eax_register.name,
                                               self.__div_temp_1) + "\n"

        string += self.__write_mov_to_register(ecx_register.name,
                                               self.__div_temp_2) + "\n"

        string += self.__write_mov_to_register(edx_register.name,
                                               self.__div_temp_3) + "\n"

        string += self.__write_mov_to_register(dev_rest_operation.get_dest_temp().get_value().name,
                                               self.__div_temp_RES) + "\n"

        context.append_string(string)

    @writer(IR.IR_DevOperation)
    def write(self, dev_operation, context):
        eax_register = RegistersType.eax
        ecx_register = RegistersType.ecx
        edx_register = RegistersType.edx

        string = self.__write_assign_local_var(self.__div_temp_1,
                                               eax_register.name) + "\n"

        string += self.__write_assign_local_var(self.__div_temp_2,
                                                ecx_register.name) + "\n"

        string += self.__write_assign_local_var(self.__div_temp_3,
                                                edx_register.name) + "\n"

        string += self.__write_mov_to_register(eax_register.name,
                                               dev_operation.get_dest_temp().get_value().name) + "\n"

        string += self.__write_mov_to_register(ecx_register.name,
                                               dev_operation.get_src_temp().get_value().name) + "\n"

        string += self.__write_idev(dev_operation.get_src_temp().get_value().name) + "\n"

        string += self.__write_assign_local_var(self.__div_temp_RES, eax_register.name) + "\n"

        string += self.__write_mov_to_register(eax_register.name,
                                               self.__div_temp_1) + "\n"

        string += self.__write_mov_to_register(ecx_register.name,
                                               self.__div_temp_2) + "\n"

        string += self.__write_mov_to_register(edx_register.name,
                                               self.__div_temp_3) + "\n"

        string += self.__write_mov_to_register(dev_operation.get_dest_temp().get_value().name,
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

    @writer(IR.Jump)
    def write(self, jump, context):
        string = \
            self.__write_jmp(jump.get_label().get_name()) + "\n"

        context.append_string(string)

    @writer(IR.JumpLess)
    def write(self, jump_less, context):
        string = \
            self.__write_jl(jump_less.get_label().get_name()) + "\n"

        context.append_string(string)

    @writer(IR.JumpGreater)
    def write(self, jump_greater, context):
        string = \
            self.__write_jg(jump_greater.get_label().get_name()) + "\n"

        context.append_string(string)

    @writer(IR.JumpEquals)
    def write(self, jump_equals, context):
        string = \
            self.__write_je(jump_equals.get_label().get_name()) + "\n"

        context.append_string(string)

    @writer(IR.JumpNotEquals)
    def write(self, jump_not_equals, context):
        string = \
            self.__write_jne(jump_not_equals.get_label().get_name()) + "\n"

        context.append_string(string)

    @writer(IR.IR_Function)
    def write(self, function, context):
        for basic_block in function.get_all_basic_blocks():
            self.write(basic_block, context)

    @writer(IR.IR_BasicBlock)
    def write(self, basic_block, context):

        self.write(basic_block.get_label(), context)

        for statement in basic_block.get_all_statements():
            self.write(statement, context)

        if basic_block.get_jump_block() is not None:
            self.write(basic_block.get_jump_block(), context)

    @writer(IR.IR_Print)
    def write(self, print_statement, context):

        string = \
            self.__write_print(print_statement.get_print_format(),
                               print_statement.get_var().get_name()) + "\n"

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
