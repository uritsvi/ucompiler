import DataTypes
import Utils

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
        self.__current_function = None
        self.__current_function_table = None

    def set_if_statement_labels(self, if_statements_labels):
        self.__if_statement_labels = if_statements_labels

    def get_if_statement_labels(self):
        return self.__if_statement_labels

    def set_condition(self, condition):
        self.__condition = condition

    def get_condition(self):
        return self.__condition

    def set_current_function(self, function):
        self.__current_function = function

    def get_current_function(self):
        return self.__current_function


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
    __instance = None

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = IR_Labels()

        return cls.__instance

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


class IR_Parameter(IR_Value):

    def __init__(self, name, data_type):
        self.__name = name
        self.__data_type = data_type

    def get_value(self):
        return self.__name

    def get_name(self):
        return self.__name

    def get_data_type(self):
        return self.__data_type

    def add_free_operation(self, basic_block):
        pass


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


# this class is a shield for a temp
class IR_TempValue(IR_Value):

    def __init__(self):
        self.__value = None
        self.__data_type = DataTypes.int_32()

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
    def __init__(self):
        self.__temp = IR_TempValue()

    def get_temp(self):
        return self.__temp

    def add_free_operation(self, current_basic_block):
        pass


class IR_DefReturnFromFunctionValueTemp(IR_DefTemp):
    pass


class IR_ReturnFromFunctionValueTemp(IR_TempValue):
    pass


class IR_ReturnFromFunctionValue(IR_TempValue):
    def __init__(self, dest_temp, function_call, data_type):
        super().__init__()

        self.__dest_temp = dest_temp
        self.__function_call = function_call
        self.__data_type = data_type

    def add_free_operation(self, current_basic_block):
        self.__dest_temp.add_free_operation(current_basic_block)

    def get_dest_temp(self):
        return self.__dest_temp


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


class IR_DivOperation(IR_ValueOperation):
    pass


class IR_DivRestOperation(IR_ValueOperation):
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
    def __init__(self, name, symbol_table, function_prototype):
        self.__basic_blocks = []
        self.__current_basic_block = []
        self.__function_prototype = function_prototype

        self.__symbol_table = symbol_table
        self.__name = name

        basic_block = IR_BasicBlock(IR_Label(IR_Labels.get_instance().get_new_label_name()), None)

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

    def get_symbol_table(self):
        return self.__symbol_table

    def get_name(self):
        return self.__name

    def get_function_prototype(self):
        return self.__function_prototype


class IR_BasicBlock(IR_Interface):
    def __init__(self, label, jump_block):

        if label is None:
            Utils.Utils.handle_compiler_error("compiler error: basic block does not contain a label")

        self.__label = label
        self.__jump_block = jump_block
        self.__statements = []

    def add_statement(self, statement):
        if type(statement) == IR_DefTemp:
            print()

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
    def __init__(self):
        self.__functions = []

    def add_function(self, function):
        self.__functions.append(function)

    def get_all_functions(self):
        return self.__functions


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


class IR_SymbolTable:
    def __init__(self):
        self.__vars = {}
        self.__arrays = {}
        self.__parameters = {}

    def get_all_vars(self):
        return self.__vars

    def get_all_arrays(self):
        return self.__arrays

    def add_var(self, var):
        self.__vars[var.get_name()] = \
            IR_Variable(var.get_name(), var.get_data_type())

    def add_array(self, array, size):
        self.__arrays[array.get_name()] = \
            IR_Array(array.get_name(), array.get_data_type(), size)

    def add_parameter(self, parameter):
        self.__parameters[parameter.get_name()] = \
            IR_Parameter(parameter.get_name(), parameter.get_data_type())


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


class IR_PassParameterToFunction(IR_Interface):
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

    def add_free_operation(self, current_basic_block):
        self.__value.add_free_operation(current_basic_block)


class IR_FunctionCall(IR_Interface):
    def __init__(self, name, parameters):
        self.__name = name
        self.__parameters = parameters

    def get_name(self):
        return self.__name

    def add_free_operation(self, current_basic_block):
        self.__parameters.add_free_operation(current_basic_block)


class IR_ReturnFromFunction(IR_Interface):
    def add_free_operation(self, current_basic_block):
        pass


class IR_PushState(IR_Interface):
    def add_free_operation(self, current_basic_block):
        pass


class IR_PopState(IR_Interface):
    def add_free_operation(self, current_basic_block):
        pass


class IR_Generator(AST_Visitor):
    def __init__(self):
        self.__program = IR_Program()

    def gen(self, main_AST):
        self.visit(main_AST, Context())
        return self.__program

    # creates an ir symbol table from a symbol table(class implemented in file SymbolTable.py)
    def __create_ir_symbol_table(self, symbol_tables, context):
        ir_table = IR_SymbolTable()

        for table in symbol_tables:
            for var in table.get_all_vars():
                ir_table.add_var(var)

        for table in symbol_tables:
            for array in table.get_all_arrays():
                ir_table.add_array(array, self.visit(array.get_size(), context))

        return ir_table

    @visitor(AST.AST_Program)
    def visit(self, program, context):
        for function in program.get_functions():
            self.visit(function, context)

    @visitor(AST.AST_Function)
    def visit(self, function, context):
        function_name = function.get_name()
        symbol_table = self.__create_ir_symbol_table(function.get_all_tables(), context)
        
        ir_function = IR_Function(function_name, symbol_table, function.get_prototype())
        
        context.set_current_function(ir_function)

        self.visit(function.get_code_block(), context)
        
        self.__program.add_function(ir_function)

    @visitor(AST.AST_CodeBlock)
    def visit(self, code_block, context):
        for statement in code_block.get_all_statements():
            if statement is None:
                continue

            self.visit(statement, context)

    @visitor(AST.AST_Integer)
    def visit(self, integer, context):
        integer = IR_Integer(integer.get_value(), integer.get_data_type())

        return integer

    @visitor(AST.AST_ArrayCell)
    def visit(self, get_value_from_array, context):

        array = self.visit(get_value_from_array.get_array_name(), context)
        index = self.visit(get_value_from_array.get_index(), context)

        data_type_size_in_bites = \
            IR_Integer(get_value_from_array.get_data_type().get_size_in_bites(),
                       get_value_from_array.get_data_type)

        def_index_temp = \
            IR_DefTemp()

        index_temp = def_index_temp.get_temp()

        assign_index_temp = IR_AssignTemp(index_temp, index)

        current_function = \
            context.get_current_function()

        current_function.get_current_basic_block().add_statement(def_index_temp)
        current_function.get_current_basic_block().add_statement(assign_index_temp)

        # to get to the array cell you need to mul the index you want to
        # access in the array by the size in bites of the array data type
        mul_operation = IR_MulOperation()
        mul_operation.set_temps(index_temp, data_type_size_in_bites)

        assign_index_temp.add_free_operation(current_function.get_current_basic_block())

        current_function.get_current_basic_block().add_statement(mul_operation)
        mul_operation.add_free_operation(current_function.get_current_basic_block())

        array_cell = \
            IR_ArrayCell(array, index_temp)

        return array_cell

    @visitor(AST.AST_Variable)
    def visit(self, variable, context):
        variable = IR_Variable(variable.get_name(), variable.get_data_type())

        return variable

    @visitor(AST.AST_Array)
    def visit(self, array, context):
        array = IR_Array(array.get_name(), array.get_data_type(), self.visit(array.get_size(), context))

        return array

    @visitor(AST.AST_Expression)
    def visit(self, expression, context):
        expression_1 = self.visit(expression.get_expression_1(), context)
        expression_2 = self.visit(expression.get_expression_2(), context)

        def_dest_temp = IR_DefTemp()
        #def_src_temp = IR_DefTemp()

        dest_temp = def_dest_temp.get_temp()
        #src_temp = def_src_temp.get_temp()

        current_function = \
            context.get_current_function()

        current_function.get_current_basic_block().add_statement(def_dest_temp)
        assign_dest_temp = IR_AssignTemp(dest_temp, expression_1)
        current_function.get_current_basic_block().add_statement(assign_dest_temp)

        """
        assign_src_temp = IR_AssignTemp(src_temp, expression_2)
        current_function.get_current_basic_block().add_statement(def_src_temp)
        assign_src_temp.add_free_operation(current_function.get_current_basic_block())
        """

        operation = \
            self.visit(expression.get_operator(), context)

        operation.set_temps(dest_temp, expression_2)

        #current_function.get_current_basic_block().add_statement(assign_src_temp)
        assign_dest_temp.add_free_operation(current_function.get_current_basic_block())

        current_function.get_current_basic_block().add_statement(operation)

        #src_temp.add_free_operation(current_function.get_current_basic_block())
        #operation.add_free_operation(current_function.get_current_basic_block())

        return dest_temp

    @visitor(AST.AST_DefVar)
    def visit(self, def_var, context):
        self.visit(def_var.get_assignment(), context)

    @visitor(AST.AST_Assignment)
    def visit(self, assignment, context):
        value = self.visit(assignment.get_value(), context)
        dest = self.visit(assignment.get_dest(), context)

        def_temp = IR_DefTemp()
        temp = def_temp.get_temp()

        assign_temp = IR_AssignTemp(temp, value)

        ir_assignment = IR_Assignment(dest, temp)

        current_function = \
            context.get_current_function()

        current_function.get_current_basic_block().add_statement(def_temp)
        current_function.get_current_basic_block().add_statement(assign_temp)
        current_function.get_current_basic_block().add_statement(ir_assignment)

        temp.add_free_operation(current_function.get_current_basic_block())
        value.add_free_operation(current_function.get_current_basic_block())
        dest.add_free_operation(current_function.get_current_basic_block())

    @visitor(AST.AST_Add_Operator)
    def visit(self, add_operator, context):
        return IR_AddOperation()

    @visitor(AST.AST_Sub_Operator)
    def visit(self, sub_operator, context):
        return IR_SUbOperation()

    @visitor(AST.AST_Mul_Operator)
    def visit(self, mul_operator, context):
        return IR_MulOperation()

    @visitor(AST.AST_Div_Operator)
    def visit(self, dev_operator, context):
        return IR_DivOperation()

    @visitor(AST.AST_Remainder_Operator)
    def visit(self, dev_res_operator, context):
        return IR_DivRestOperation()

    @visitor(AST.AST_LessOperator)
    def visit(self, less_operator, context):
        return IR_JumpLess()

    @visitor(AST.AST_GreaterOperator)
    def visit(self, greater_operator, context):
        return IR_JumpGreater()

    @visitor(AST.AST_EqualityOperator)
    def visit(self, equality_operator, context):
        return IR_JumpEquals()

    @visitor(AST.AST_NotEqualsOperator)
    def visit(self, not_equals_operator, context):
        return IR_JumpNotEquals()

    @visitor(AST.AST_AndOperator)
    def visit(self, and_operator, context):

        condition = context.get_condition()

        new_basic_block_label = IR_Label(IR_Labels.get_instance().get_new_label_name())

        current_function = \
            context.get_current_function()

        new_basic_block = IR_BasicBlock(new_basic_block_label,
                                        current_function.get_current_basic_block().get_jump_block())

        jump_to_else_part = IR_Jump()

        jump_to_else_part.set_label(context.get_if_statement_labels().get_else_part_label())

        jump_to_than_part = \
            condition.get_operator()

        jump_to_than_part.set_label(new_basic_block_label)

        condition.add_free_operation(current_function.get_current_basic_block())

        ir_if = IR_IfStatement(condition,
                               jump_to_than_part,
                               jump_to_else_part)

        current_function.get_current_basic_block().set_jump_block(ir_if)

        current_function.add_basic_block(new_basic_block)
        current_function.push_current_basic_block(new_basic_block)

    @visitor(AST.AST_OrOperator)
    def visit(self, or_condition, context):

        condition = context.get_condition()

        new_basic_block_label = IR_Label(IR_Labels.get_instance().get_new_label_name())

        current_function = \
            context.get_current_function()

        new_basic_block = IR_BasicBlock(new_basic_block_label,
                                        current_function.get_current_basic_block().get_jump_block())

        jump_to_else_part = IR_Jump()
        jump_to_else_part.set_label(new_basic_block_label)

        jump_to_than_part = \
            condition.get_operator()

        jump_to_than_part.set_label(context.get_if_statement_labels().get_than_part_label())

        condition.add_free_operation(current_function.get_current_basic_block())

        ir_if = IR_IfStatement(condition,
                               jump_to_than_part,
                               jump_to_else_part)

        current_function.get_current_basic_block().set_jump_block(ir_if)

        current_function.add_basic_block(new_basic_block)
        current_function.push_current_basic_block(new_basic_block)

    @visitor(AST.AST_IfStatement)
    def visit(self, if_statement, context):

        contains_else_part = False
        if if_statement.get_else_part() is not None:
            contains_else_part = True

        current_function = \
            context.get_current_function()

        last_jump_block = \
            current_function.get_current_basic_block().get_jump_block()

        # this label can be for the else part or the merge block
        else_part_label = IR_Label(IR_Labels.get_instance().get_new_label_name())
        than_part_label = IR_Label(IR_Labels.get_instance().get_new_label_name())

        context.set_if_statement_labels(IR_IfStatementLabels(than_part_label, else_part_label))
        condition = self.visit(if_statement.get_condition(), context)

        jump_to_than_part = condition.get_operator()
        jump_to_than_part.set_label(than_part_label)

        jump_to_else_part = IR_Jump()
        jump_to_else_part.set_label(else_part_label)

        if contains_else_part:
            merge_block_label = IR_Label(IR_Labels.get_instance().get_new_label_name())
        else:
            merge_block_label = else_part_label

        jump_to_merge_block = IR_Jump()
        jump_to_merge_block.set_label(merge_block_label)

        than_part = IR_BasicBlock(than_part_label, jump_to_merge_block)

        ir_if_statement = \
            IR_IfStatement(condition,
                           jump_to_than_part,
                           jump_to_else_part)

        current_function.get_current_basic_block().set_jump_block(ir_if_statement)

        # gen the then part code
        current_function.push_current_basic_block(than_part)
        current_function.add_basic_block(than_part)

        condition.add_free_operation(current_function.get_current_basic_block())

        self.visit(if_statement.get_then_part(), context)

        if contains_else_part:
            # gen else part code
            else_part = IR_BasicBlock(else_part_label, jump_to_merge_block)
            current_function.push_current_basic_block(else_part)
            current_function.add_basic_block(else_part)

            condition.add_free_operation(current_function.get_current_basic_block())

            self.visit(if_statement.get_else_part(), context)

            current_function.pop_current_basic_block()

        merge_block = IR_BasicBlock(merge_block_label, last_jump_block)

        # set the merge block as the new current block
        current_function.add_basic_block(merge_block)
        current_function.push_current_basic_block(merge_block)

    @visitor(AST.AST_ElseStatement)
    def visit(self, else_statement, context):
        self.visit(else_statement.get_code_block(), context)

    @visitor(AST.AST_WhileLoopStatement)
    def visit(self, while_loop_statement, context):
        current_function = \
            context.get_current_function()

        last_jump_block = \
            current_function.get_current_basic_block().get_jump_block()

        cmp_block_label = IR_Label(IR_Labels.get_instance().get_new_label_name())
        cmp_block = IR_BasicBlock(cmp_block_label, None)

        jump_to_cmp_block = IR_Jump()
        jump_to_cmp_block.set_label(cmp_block_label)

        current_function.get_current_basic_block().set_jump_block(jump_to_cmp_block)

        current_function.add_basic_block(cmp_block)
        current_function.push_current_basic_block(cmp_block)

        merge_block_label = IR_Label(IR_Labels.get_instance().get_new_label_name())

        than_part_label = IR_Label(IR_Labels.get_instance().get_new_label_name())

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

        cmp_block.set_jump_block(ir_if_statement)

        # gen the then part code
        current_function.push_current_basic_block(than_part)
        current_function.add_basic_block(than_part)

        condition.add_free_operation(current_function.get_current_basic_block())

        self.visit(while_loop_statement.get_code_block(), context)

        current_function.pop_current_basic_block()

        merge_block = \
            IR_BasicBlock(merge_block_label, last_jump_block)

        # set the merge block as the new current block
        current_function.add_basic_block(merge_block)
        current_function.push_current_basic_block(merge_block)

    @visitor(AST.AST_Condition)
    def visit(self, condition, context):
        def_temp = IR_DefTemp()
        temp_1 = def_temp.get_temp()

        expression_1 = self.visit(condition.get_expression_1(), context)

        assign_temp = IR_AssignTemp(temp_1, expression_1)

        current_function = \
            context.get_current_function()

        current_function.get_current_basic_block().add_statement(def_temp)
        current_function.get_current_basic_block().add_statement(assign_temp)

        expression_1.add_free_operation(current_function.get_current_basic_block())

        def_temp = IR_DefTemp()
        temp_2 = def_temp.get_temp()

        expression_2 = self.visit(condition.get_expression_2(), context)

        assign_temp = IR_AssignTemp(temp_2, expression_2)

        current_function.get_current_basic_block().add_statement(def_temp)
        current_function.get_current_basic_block().add_statement(assign_temp)

        expression_2.add_free_operation(current_function.get_current_basic_block())

        operator = self.visit(condition.get_operator(), context)

        ir_condition = \
            IR_Condition(temp_1, operator, temp_2)

        return ir_condition

    @visitor(AST.AST_ComplexCondition)
    def visit(self, condition, context):
        condition_1 = self.visit(condition.get_condition_1(), context)

        context.set_condition(condition_1)

        self.visit(condition.get_operator(), context)

        condition_2 = self.visit(condition.get_condition_2(), context)
        return condition_2

    @visitor(AST.AST_ReadLine)
    def visit(self, read_line_statement, context):
        ir_read_line = \
            IR_ReadLine(read_line_statement.get_array_name(),
                        self.visit(read_line_statement.get_num_of_chars(), context))

        context.get_current_function().\
            get_current_basic_block().add_statement(ir_read_line)

    @visitor(AST.AST_Print)
    def visit(self, print_statement, context):
        value = self.visit(print_statement.get_value(), context)

        ir_print = IR_Print(print_statement.get_print_format(),
                            value)

        current_basic_block = context.get_current_function().\
            get_current_basic_block()

        current_basic_block.\
            add_statement(ir_print)

        value.add_free_operation(current_basic_block)

    @visitor(AST.AST_PrintArray)
    def visit(self, print_array, context):
        ir_print = \
            IR_PrintArray(print_array.get_array_name())

        context.get_current_function().\
            get_current_basic_block().add_statement(ir_print)

    @visitor(AST.AST_PrintString)
    def visit(self, print_statement, context):
        ir_print = \
            IR_PrintString(print_statement.get_string())

        context.get_current_function().\
            get_current_basic_block().add_statement(ir_print)

    @visitor(AST.AST_Exit)
    def visit(self, exit_statement, context):
        ir_exit_statement = \
            IR_Exit(self.visit(exit_statement.get_exit_code(), context))

        context.get_current_function().\
            get_current_basic_block().add_statement(ir_exit_statement)

    @visitor(AST.AST_FunctionCall)
    def visit(self, function_call, context):

        current_basic_block = context.get_current_function().\
            get_current_basic_block()

        ir_push_state = IR_PushState()
        current_basic_block.add_statement(ir_push_state)

        ir_function_call = \
            IR_FunctionCall(function_call.get_name(), function_call.get_parameters())

        call_parameters = \
            function_call.get_parameters().get_all_parameters()

        # the calling convention is stdcall so i
        # need to pass the parameters from the end to the start
        call_parameters.reverse()

        for parameter in call_parameters:

            ir_parameter = \
                self.visit(parameter, context)

            ir_pass_parameter_to_function = \
                IR_PassParameterToFunction(ir_parameter)

            current_basic_block.add_statement(ir_pass_parameter_to_function)
            ir_pass_parameter_to_function.add_free_operation(current_basic_block)

        ir_pop_state = IR_PopState()

        current_basic_block.add_statement(ir_function_call)
        current_basic_block.add_statement(ir_pop_state)

    @visitor(AST.AST_ReturnStatement)
    def visit(self, return_statement, context):
        ir_return_statement = \
            IR_ReturnFromFunction()

        current_basic_block = \
            context.get_current_function().get_current_basic_block()

        return_value = \
            return_statement.get_value()

        if return_value is not None:

            return_value = \
                self.visit(return_value, context)

            def_return_from_function_value_temp = \
                IR_DefReturnFromFunctionValueTemp()

            temp = \
                def_return_from_function_value_temp.get_temp()

            fill_return_value_temp = \
                IR_AssignTemp(temp, return_value)

            current_basic_block.\
                add_statement(def_return_from_function_value_temp)

            current_basic_block.\
                add_statement(fill_return_value_temp)

            fill_return_value_temp. \
                add_free_operation(current_basic_block)

            current_basic_block. \
                add_statement(ir_return_statement)

            temp.\
                add_free_operation(current_basic_block)
        else:
            current_basic_block. \
                add_statement(ir_return_statement)

    @visitor(AST.AST_FunctionCallReturnValue)
    def visit(self, function_call_return_value, context):

        current_basic_block = \
            context.get_current_function().get_current_basic_block()

        self.visit(function_call_return_value.get_function_call(), context)

        data_type = \
            function_call_return_value.get_data_type()

        def_dest_temp = \
            IR_DefTemp()

        context.get_current_function().get_current_basic_block().\
            add_statement(def_dest_temp)

        dest_temp = \
            def_dest_temp.get_temp()

        assign_dest_temp = \
            IR_AssignTemp(dest_temp, IR_ReturnFromFunctionValueTemp())


        current_basic_block.\
            add_statement(assign_dest_temp)

        ir_return = \
            IR_ReturnFromFunctionValue(dest_temp,
                                       function_call_return_value.get_function_call(),
                                       data_type)

        return ir_return
