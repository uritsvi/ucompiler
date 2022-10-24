import DataTypes
import Utils
import SymbolTable

from AST_Visitor import *


class IR_IfStatementLabels:
    def __init__(self, than_part_label, else_part_label):
        self.__than_part_label = than_part_label
        self.__else_part_label = else_part_label

    def get_than_part_label(self):
        return self.__than_part_label

    def get_else_part_label(self):
        return self.__else_part_label


class Context:
    def __init__(self):
        self.__if_statement_labels = None
        self.__condition = None

    def set_if_statement_labels(self, if_statements_labels):
        self.__if_statement_labels = if_statements_labels

    def get_if_statement_labels(self):
        return self.__if_statement_labels

    def set_condition(self, condition):
        self.__condition = condition

    def get_condition(self):
        return self.__condition


class IR_Interface:
    @abstractmethod
    def add_free_operation(self, current_basic_block):
        pass


class IR_FreeValue(IR_Interface):
    def add_free_operation(self, current_basic_block):
        pass


class IR_FreeVariable(IR_FreeValue):
    def __init__(self, name):
        self.__name = name


class IR_FreeTemp(IR_FreeValue):
    def __init__(self, temp_value):
        self.__temp_value = temp_value

    def get_temp(self):
        return self.__temp_value


class IR_FreeInteger(IR_FreeValue):
    def __init__(self, integer):
        self.__integer = integer


class IR_Labels:
    def __init__(self):
        self.__count = 0

    def get_new_label_name(self):
        string = "L" + str(self.__count)

        self.__count += 1

        return string


class IR_Assignment(IR_Interface):
    def __init__(self, name, value):
        self.__name = name
        self.__value = value

    def get_dest(self):
        return self.__name

    def get_value(self):
        return self.__value

    def add_free_operation(self, current_basic_block):
        pass


class IR_AssignTemp(IR_Interface):
    def __init__(self, temp, value):
        self.__temp = temp
        self.__value = value

    def get_temp(self):
        return self.__temp

    def get_value(self):
        return self.__value

    def add_free_operation(self, current_basic_block):
        self.__value.add_free_operation(current_basic_block)


class IR_Operator(IR_Interface):
    def __init__(self):
        self.__operation = None

    @abstractmethod
    def _get_operation(self):
        pass

    def get_operation(self):
        if self.__operation is None:
            self.__operation = self._get_operation()

        return self.__operation

    def add_free_operation(self, current_basic_block):
        pass


class IR_Value(IR_Interface):

    @abstractmethod
    def get_value(self):
        pass

    @abstractmethod
    def add_free_operation(self, basic_block):
        pass

    @abstractmethod
    def get_data_type(self):
        pass


class IR_Integer(IR_Value):

    def __init__(self, value, data_type):
        self.__value = value
        self.__data_type = data_type

    def get_value(self):
        return self.__value

    def add_free_operation(self, current_basic_block):
        current_basic_block.add_statement(IR_FreeInteger(self.__value))

    def get_data_type(self):
        return self.__data_type


class IR_Variable(IR_Value):

    def __init__(self, name, data_type):
        self.__name = name
        self.__data_type = data_type

    def get_name(self):
        return self.__name

    def get_value(self):
        return self.__name

    def add_free_operation(self, current_basic_block):
        current_basic_block.add_statement(IR_FreeVariable(self.__name))

    def get_data_type(self):
        return self.__data_type


class IR_TempValue(IR_Value):

    def __init__(self, data_type):
        self.__value = None
        self.__data_type = data_type

    # set the temp
    def set_value(self, data):
        self.__value = data

    # returns the temp
    def get_value(self):
        return self.__value

    def add_free_operation(self, current_basic_block):
        current_basic_block.add_statement(IR_FreeTemp(self))

    def get_data_type(self):
        return self.__data_type


class IR_DefTemp(IR_Interface):
    def __init__(self, data_type):
        self.__temp = IR_TempValue(data_type)

    def get_temp(self):
        return self.__temp

    def add_free_operation(self, current_basic_block):
        pass


class IR_ValueOperation(IR_Interface):

    # the object is created on the operator visit so,
    # I can't pass the temps in the constructor

    def __init__(self):
        self._dest_temp = None
        self._src_temp = None

    def set_temps(self, dest_temp, src_temp):
        self._dest_temp = dest_temp
        self._src_temp = src_temp

    def get_dest_temp(self):
        return self._dest_temp

    def get_src_temp(self):
        return self._src_temp

    def add_free_operation(self, current_basic_block):
        pass


class IR_AddOperation(IR_ValueOperation):
    pass


class IR_SUbOperation(IR_ValueOperation):
    pass


class IR_MulOperation(IR_ValueOperation):
    pass


class IR_DevOperation(IR_ValueOperation):
    pass


class IR_DevRestOperation(IR_ValueOperation):
    pass


class IR_Condition(IR_Interface):
    def __init__(self, expression_1, operator, expression_2):
        self.__expression_1 = expression_1
        self.__expression_2 = expression_2
        self.__operator = operator

    def get_operator(self):
        return self.__operator

    def get_expression_1(self):
        return self.__expression_1

    def get_expression_2(self):
        return self.__expression_2

    def add_free_operation(self, current_basic_block):
        self.__expression_1.add_free_operation(current_basic_block)
        self.__expression_2.add_free_operation(current_basic_block)

        self.__operator.add_free_operation(current_basic_block)


class IR_JumpBlock(IR_Interface):

    def __init__(self):
        self._label = None

    def set_label(self, label):
        self._label = label

    @abstractmethod
    def on_use(self, context):
        pass


class IR_IfStatement(IR_Interface):
    def __init__(self, condition, jump_to_than_part, jump_to_else_part):
        self.__condition = condition
        self.__jump_to_than_part = jump_to_than_part
        self.__jump_to_else_part = jump_to_else_part

    def add_free_operation(self, current_basic_block):
        pass

    def get_condition(self):
        return self.__condition

    def get_jump_to_than_part(self):
        return self.__jump_to_than_part

    def get_jump_to_else_part(self):
        return self.__jump_to_else_part


class IR_JumpStatement(IR_Interface):
    def __init__(self):
        self.__label = None

    def add_free_operation(self, current_basic_block):
        pass

    def get_label(self):
        return self.__label

    def set_label(self, label):
        self.__label = label


class IR_Jump(IR_JumpStatement):
    pass


class IR_JumpEquals(IR_JumpStatement):
    pass


class IR_JumpNotEquals(IR_JumpStatement):
    pass


class IR_JumpLess(IR_JumpStatement):
    pass


class IR_JumpGreater(IR_JumpStatement):
    pass


class IR_Function(IR_Interface):
    def __init__(self):
        self.__basic_blocks = []
        self.__current_basic_block = []

        basic_block = IR_BasicBlock(IR_Label("program"), None)

        self.__current_basic_block.append(basic_block)
        self.__basic_blocks.append(basic_block)

    def pop_current_basic_block(self):
        return self.__current_basic_block.pop()

    def push_current_basic_block(self, basic_block):
        self.__current_basic_block.append(basic_block)

    def get_current_basic_block(self):
        return self.__current_basic_block[-1]

    def add_basic_block(self, basic_block):
        self.__basic_blocks.append(basic_block)

    def write_basic_blocks(self):
        string = ""

        for basic_block in self.__basic_blocks:
            string += "label: " + str(basic_block.get_label()) + "\n"

            for statement in basic_block.get_statements():
                string += str(statement) + "\n"

            if basic_block.get_jump_block() is not None:
                string += "goto block: " + str(basic_block.get_jump_block()) + "\n"

        return string

    def add_free_operation(self, current_basic_block):
        pass

    def get_all_basic_blocks(self):
        return self.__basic_blocks


class IR_BasicBlock(IR_Interface):
    def __init__(self, label, jump_block):

        if label is None:
            Utils.Utils.handle_compiler_error("compiler error: basic block does not contain a label")

        self.__label = label
        self.__jump_block = jump_block
        self.__statements = []

    def add_statement(self, statement):
        self.__statements.append(statement)

    def set_jump_block(self, jump_block):
        self.__jump_block = jump_block

    def get_statements(self):
        return self.__statements

    def get_jump_block(self):
        return self.__jump_block

    def get_label(self):
        return self.__label

    def add_free_operation(self, current_basic_block):
        pass

    def get_all_statements(self):
        return self.__statements


class IR_Label(IR_Interface):
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def add_free_operation(self, current_basic_block):
        pass


class IR_Program:
    def __init__(self, main_function, symbol_tabel):
        self.__main_function = main_function
        self.__symbol_tabel = symbol_tabel

    def get_main_function(self):
        return self.__main_function

    def get_symbol_tabel(self):
        return self.__symbol_tabel


class IR_Array:
    def __init__(self, name, data_type, size):
        self.__name = name
        self.__data_type = data_type
        self.__size = size

    def get_name(self):
        return self.__name

    def get_data_type(self):
        return self.__data_type

    def get_size(self):
        return self.__size


class IR_ArrayCell(IR_Value):
    def __init__(self, ir_array, index):
        self.__ir_array = ir_array
        self.__index = index

    def get_ir_array(self):
        return self.__ir_array

    def get_index(self):
        return self.__index

    def add_free_operation(self, current_basic_block):
        self.__index.add_free_operation(current_basic_block)

    def get_value(self):
        pass

    def get_data_type(self):
        return self.__ir_array.get_data_type()


class IR_Function_SymbolTabel:

    def __init__(self):
        self.__vars = {}
        self.__arrays = {}

    def get_all_vars(self):

        for tabel in SymbolTable.Tables.get_instance().get_all_tables():
            for var in tabel.get_all_vars():
                self.__vars[var.get_name()] = (IR_Variable(var.get_name(), var.get_data_type()))

        return self.__vars

    def get_all_arrays(self):
        for tabel in SymbolTable.Tables.get_instance().get_all_tables():
            for symbol_Tabel_array in tabel.get_all_arrays():
                self.__arrays[symbol_Tabel_array.get_name()] = (IR_Array(symbol_Tabel_array.get_name(),
                                                                         symbol_Tabel_array.get_data_type(),
                                                                         symbol_Tabel_array.get_size().get_value()))

        return self.__arrays

    def get_var_or_array(self, var_name):
        var = self.__vars.get(var_name)

        if var is None:
            return self.__arrays.get(var_name)

        return var


class IR_ReadLine(IR_Interface):
    def __init__(self, array_name, num_of_chars):
        self.__array_name = array_name
        self.__num_of_chars = num_of_chars

    def get_array_name(self):
        return self.__array_name

    def get_num_of_chars(self):
        return self.__num_of_chars

    def add_free_operation(self, current_basic_block):
        pass


class IR_Print(IR_Interface):
    def __init__(self, print_format, var_name):
        self.__var_name = var_name
        self.__print_format = print_format

    def get_var(self):
        return self.__var_name

    def get_print_format(self):
        return self.__print_format

    def add_free_operation(self, current_basic_block):
        pass


class IR_PrintArray(IR_Interface):
    def __init__(self, array):
        self.__array = array

    def get_array_name(self):
        return self.__array

    def add_free_operation(self, current_basic_block):
        pass


class IR_PrintString(IR_Interface):
    def __init__(self, string):
        self.__string = string

    def get_string(self):
        return self.__string

    def add_free_operation(self, current_basic_block):
        pass


class IR_Exit(IR_Interface):
    def __init__(self, exit_code):
        self.__exit_code = exit_code

    def get_exit_code(self):
        return self.__exit_code

    def add_free_operation(self, current_basic_block):
        pass


class IR_Generator(AST_Visitor):
    def __init__(self):
        self.__main_function = IR_Function()
        self.__labels = IR_Labels()

    def gen(self, main_AST):
        self.visit(main_AST, Context())
        symbol_tale = IR_Function_SymbolTabel()

        program = IR_Program(self.__main_function, symbol_tale)
        return program

    @visitor(AST_CodeBlock)
    def visit(self, code_block, context):
        for statement in code_block.get_all_statements():
            if statement is None:
                continue

            self.visit(statement, context)

    @visitor(AST_Integer)
    def visit(self, integer, context):
        integer = IR_Integer(integer.get_value(), integer.get_data_type())

        return integer

    @visitor(AST_ArrayCell)
    def visit(self, get_value_from_array, context):

        array = self.visit(get_value_from_array.get_array_name(), context)
        index = self.visit(get_value_from_array.get_index(), context)

        data_type_size_in_bites = \
            IR_Integer(get_value_from_array.get_data_type().get_size_in_bites(),
                       get_value_from_array.get_data_type)

        def_index_temp = \
            IR_DefTemp(DataTypes.int_32())

        index_temp = def_index_temp.get_temp()

        assign_index_temp = IR_AssignTemp(index_temp, index)

        self.__main_function.get_current_basic_block().add_statement(def_index_temp)
        self.__main_function.get_current_basic_block().add_statement(assign_index_temp)

        # to get to the array cell you need to mul the index you want to
        # access in the array by the size in bites of the array data type
        mul_operation = IR_MulOperation()
        mul_operation.set_temps(index_temp, data_type_size_in_bites)

        assign_index_temp.add_free_operation(self.__main_function.get_current_basic_block())

        self.__main_function.get_current_basic_block().add_statement(mul_operation)
        mul_operation.add_free_operation(self.__main_function.get_current_basic_block())

        array_cell = \
            IR_ArrayCell(array, index_temp)

        return array_cell

    @visitor(AST_Variable)
    def visit(self, variable, context):

        variable = IR_Variable(variable.get_name(), variable.get_data_type())

        return variable

    @visitor(AST_Array)
    def visit(self, array, context):
        array = IR_Array(array.get_name(), array.get_data_type(), array.get_size())

        return array

    @visitor(AST_NewVariable)
    def visit(self, new_variable, context):
        return IR_Variable(new_variable.get_name(),
                           SymbolTable.Tables.get_instance().get_current_table().
                           get_var(new_variable.get_name()).get_data_type())

    @visitor(AST_Expression)
    def visit(self, expression, context):
        def_dest_temp = IR_DefTemp(expression.get_data_type())
        def_src_temp = IR_DefTemp(expression.get_data_type())

        dest_temp = def_dest_temp.get_temp()
        src_temp = def_src_temp.get_temp()

        assign_dest_temp = IR_AssignTemp(dest_temp, self.visit(expression.get_expression_1(), context))
        assign_src_temp = IR_AssignTemp(src_temp, self.visit(expression.get_expression_2(), context))

        operation = self.visit(expression.get_operator(), context)
        operation.set_temps(dest_temp, src_temp)

        self.__main_function.get_current_basic_block().add_statement(def_dest_temp)
        self.__main_function.get_current_basic_block().add_statement(def_src_temp)

        self.__main_function.get_current_basic_block().add_statement(assign_dest_temp)
        assign_src_temp.add_free_operation(self.__main_function.get_current_basic_block())

        self.__main_function.get_current_basic_block().add_statement(assign_src_temp)
        assign_dest_temp.add_free_operation(self.__main_function.get_current_basic_block())

        self.__main_function.get_current_basic_block().add_statement(operation)

        src_temp.add_free_operation(self.__main_function.get_current_basic_block())
        operation.add_free_operation(self.__main_function.get_current_basic_block())

        return dest_temp

    @visitor(AST_DefVar)
    def visit(self, def_var, context):
        self.visit(def_var.get_assignment(), context)

    @visitor(AST_Assignment)
    def visit(self, assignment, context):
        value = self.visit(assignment.get_value(), context)
        dest = self.visit(assignment.get_dest(), context)

        def_temp = IR_DefTemp(value.get_data_type())
        temp = def_temp.get_temp()

        assign_temp = IR_AssignTemp(temp, value)

        ir_assignment = IR_Assignment(dest, temp)

        self.__main_function.get_current_basic_block().add_statement(def_temp)
        self.__main_function.get_current_basic_block().add_statement(assign_temp)
        self.__main_function.get_current_basic_block().add_statement(ir_assignment)

        temp.add_free_operation(self.__main_function.get_current_basic_block())
        value.add_free_operation(self.__main_function.get_current_basic_block())
        dest.add_free_operation(self.__main_function.get_current_basic_block())

    @visitor(AST_Add_Operator)
    def visit(self, add_operator, context):
        return IR_AddOperation()

    @visitor(AST_Sub_Operator)
    def visit(self, sub_operator, context):
        return IR_SUbOperation()

    @visitor(AST_Mul_Operator)
    def visit(self, mul_operator, context):
        return IR_MulOperation()

    @visitor(AST_Div_Operator)
    def visit(self, dev_operator, context):
        return IR_DevOperation()

    @visitor(AST_Remainder_Operator)
    def visit(self, dev_res_operator, context):
        return IR_DevRestOperation()

    @visitor(AST_LessOperatorAST)
    def visit(self, less_operator, context):
        return IR_JumpLess()

    @visitor(AST_GreaterOperatorAST)
    def visit(self, greater_operator, context):
        return IR_JumpGreater()

    @visitor(AST_EqualityOperatorAST)
    def visit(self, equality_operator, context):
        return IR_JumpEquals()

    @visitor(AST_NotEqualsOperatorAST)
    def visit(self, not_equals_operator, context):
        return IR_JumpNotEquals()

    @visitor(AST_AndOperator)
    def visit(self, and_operator, context):

        condition = context.get_condition()

        new_basic_block_label = IR_Label(self.__labels.get_new_label_name())

        new_basic_block = IR_BasicBlock(new_basic_block_label,
                                        self.__main_function.get_current_basic_block().get_jump_block())

        jump_to_else_part = IR_Jump()

        jump_to_else_part.set_label(context.get_if_statement_labels().get_else_part_label())

        jump_to_than_part = \
            condition.get_operator()

        jump_to_than_part.set_label(new_basic_block_label)

        condition.add_free_operation(self.__main_function.get_current_basic_block())

        ir_if = IR_IfStatement(condition,
                               jump_to_than_part,
                               jump_to_else_part)

        self.__main_function.get_current_basic_block().set_jump_block(ir_if)

        self.__main_function.add_basic_block(new_basic_block)
        self.__main_function.push_current_basic_block(new_basic_block)

    @visitor(AST_OrOperatorAST)
    def visit(self, or_condition, context):

        condition = context.get_condition()

        new_basic_block_label = IR_Label(self.__labels.get_new_label_name())

        new_basic_block = IR_BasicBlock(new_basic_block_label,
                                        self.__main_function.get_current_basic_block().get_jump_block())

        jump_to_else_part = IR_Jump()
        jump_to_else_part.set_label(new_basic_block_label)

        jump_to_than_part = \
            condition.get_operator()

        jump_to_than_part.set_label(context.get_if_statement_labels().get_than_part_label())

        condition.add_free_operation(self.__main_function.get_current_basic_block())

        ir_if = IR_IfStatement(condition,
                               jump_to_than_part,
                               jump_to_else_part)

        self.__main_function.get_current_basic_block().set_jump_block(ir_if)

        self.__main_function.add_basic_block(new_basic_block)
        self.__main_function.push_current_basic_block(new_basic_block)

    @visitor(AST_IfStatement)
    def visit(self, if_statement, context):

        contains_else_part = False
        if if_statement.get_else_part() is not None:
            contains_else_part = True

        last_jump_block = \
            self.__main_function.get_current_basic_block().get_jump_block()

        # this label can be for the else part or the merge block
        else_part_label = IR_Label(self.__labels.get_new_label_name())
        than_part_label = IR_Label(self.__labels.get_new_label_name())

        context.set_if_statement_labels(IR_IfStatementLabels(than_part_label, else_part_label))
        condition = self.visit(if_statement.get_condition(), context)

        jump_to_than_part = condition.get_operator()
        jump_to_than_part.set_label(than_part_label)

        jump_to_else_part = IR_Jump()
        jump_to_else_part.set_label(else_part_label)

        if contains_else_part:
            merge_block_label = IR_Label(self.__labels.get_new_label_name())
        else:
            merge_block_label = else_part_label

        jump_to_merge_block = IR_Jump()
        jump_to_merge_block.set_label(merge_block_label)

        than_part = IR_BasicBlock(than_part_label, jump_to_merge_block)

        ir_if_statement = \
            IR_IfStatement(condition,
                           jump_to_than_part,
                           jump_to_else_part)

        self.__main_function.get_current_basic_block().set_jump_block(ir_if_statement)

        # gen the then part code
        self.__main_function.push_current_basic_block(than_part)
        self.__main_function.add_basic_block(than_part)

        condition.add_free_operation(self.__main_function.get_current_basic_block())

        self.visit(if_statement.get_then_part(), context)

        if contains_else_part:
            # gen else part code
            else_part = IR_BasicBlock(else_part_label, jump_to_merge_block)
            self.__main_function.push_current_basic_block(else_part)
            self.__main_function.add_basic_block(else_part)

            condition.add_free_operation(self.__main_function.get_current_basic_block())

            self.visit(if_statement.get_else_part(), context)

            self.__main_function.pop_current_basic_block()

        merge_block = IR_BasicBlock(merge_block_label, last_jump_block)

        # set the merge block as the new current block
        self.__main_function.add_basic_block(merge_block)
        self.__main_function.push_current_basic_block(merge_block)

    @visitor(AST_ElseStatement)
    def visit(self, else_statement, context):
        self.visit(else_statement.get_code_block(), context)

    @visitor(AST_WhileLoopStatement)
    def visit(self, while_loop_statement, context):
        last_jump_block = \
            self.__main_function.get_current_basic_block().get_jump_block()

        cmp_block_label = IR_Label(self.__labels.get_new_label_name())
        cmp_block = IR_BasicBlock(cmp_block_label, last_jump_block)

        jump_to_cmp_block = IR_Jump()
        jump_to_cmp_block.set_label(cmp_block_label)

        self.__main_function.get_current_basic_block().set_jump_block(jump_to_cmp_block)

        self.__main_function.add_basic_block(cmp_block)
        self.__main_function.push_current_basic_block(cmp_block)

        merge_block_label = IR_Label(self.__labels.get_new_label_name())

        than_part_label = IR_Label(self.__labels.get_new_label_name())

        context.set_if_statement_labels(IR_IfStatementLabels(than_part_label, merge_block_label))
        condition = self.visit(while_loop_statement.get_condition(), context)

        jump_to_than_part = condition.get_operator()
        jump_to_than_part.set_label(than_part_label)

        jump_to_merge_block = IR_Jump()
        jump_to_merge_block.set_label(merge_block_label)

        than_part = IR_BasicBlock(than_part_label, jump_to_cmp_block)

        ir_if_statement = \
            IR_IfStatement(condition,
                           jump_to_than_part,
                           jump_to_merge_block)

        self.__main_function.get_current_basic_block().set_jump_block(ir_if_statement)

        # gen the then part code
        self.__main_function.push_current_basic_block(than_part)
        self.__main_function.add_basic_block(than_part)

        condition.add_free_operation(self.__main_function.get_current_basic_block())

        self.visit(while_loop_statement.get_code_block(), context)

        self.__main_function.pop_current_basic_block()

        merge_block = IR_BasicBlock(merge_block_label, last_jump_block)

        # set the merge block as the new current block
        self.__main_function.add_basic_block(merge_block)
        self.__main_function.push_current_basic_block(merge_block)

    @visitor(AST_Condition)
    def visit(self, condition, context):
        def_temp = IR_DefTemp(condition.get_expression_1().get_data_type())
        temp_1 = def_temp.get_temp()

        expression_1 = self.visit(condition.get_expression_1(), context)

        assign_temp = IR_AssignTemp(temp_1, expression_1)

        self.__main_function.get_current_basic_block().add_statement(def_temp)
        self.__main_function.get_current_basic_block().add_statement(assign_temp)

        expression_1.add_free_operation(self.__main_function.get_current_basic_block())

        def_temp = IR_DefTemp(condition.get_expression_1().get_data_type())
        temp_2 = def_temp.get_temp()

        expression_2 = self.visit(condition.get_expression_2(), context)

        assign_temp = IR_AssignTemp(temp_2, expression_2)

        self.__main_function.get_current_basic_block().add_statement(def_temp)
        self.__main_function.get_current_basic_block().add_statement(assign_temp)

        expression_2.add_free_operation(self.__main_function.get_current_basic_block())

        operator = self.visit(condition.get_operator(), context)

        ir_condition = \
            IR_Condition(temp_1, operator, temp_2)

        return ir_condition

    @visitor(AST_ComplexCondition)
    def visit(self, condition, context):
        condition_1 = self.visit(condition.get_condition_1(), context)

        context.set_condition(condition_1)

        self.visit(condition.get_operator(), context)

        condition_2 = self.visit(condition.get_condition_2(), context)
        return condition_2

    @visitor(AST_ReadLine)
    def visit(self, read_line_statement, context):
        ir_read_line = \
            IR_ReadLine(read_line_statement.get_array_name(),
                        self.visit(read_line_statement.get_num_of_chars(), context))

        self.__main_function.get_current_basic_block().add_statement(ir_read_line)

    @visitor(AST_Print)
    def visit(self, print_statement, context):
        ir_print = IR_Print(print_statement.get_print_format(),
                            self.visit(print_statement.get_value(), context))

        self.__main_function.get_current_basic_block().add_statement(ir_print)

    @visitor(AST_PrintArray)
    def visit(self, print_array, context):
        ir_print = \
            IR_PrintArray(print_array.get_array_name())

        self.__main_function.get_current_basic_block().add_statement(ir_print)

    @visitor(AST_PrintString)
    def visit(self, print_statement, context):
        ir_print = IR_PrintString(print_statement.get_string())
        self.__main_function.get_current_basic_block().add_statement(ir_print)

    @visitor(AST_Exit)
    def visit(self, exit_statement, context):
        ir_exit_statement = IR_Exit(self.visit(exit_statement.get_exit_code(), context))
        self.__main_function.get_current_basic_block().add_statement(ir_exit_statement)
