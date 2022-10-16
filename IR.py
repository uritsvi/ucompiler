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


class FreeValue(IR_Interface):
    def add_free_operation(self, current_basic_block):
        pass


class FreeVariable(FreeValue):
    def __init__(self, name):
        self.__name = name


class FreeTemp(FreeValue):
    def __init__(self, temp_value):
        self.__temp_value = temp_value

    def get_temp(self):
        return self.__temp_value


class FreeInteger(FreeValue):
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

    def get_var_name(self):
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
        pass


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


class IR_Integer(IR_Value):
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

    def add_free_operation(self, current_basic_block):
        current_basic_block.add_statement(FreeInteger(self.__value))


class IR_Variable(IR_Value):
    def __init__(self, name):
        self.__name = name

    def get_value(self):
        return self.__name

    def add_free_operation(self, current_basic_block):
        current_basic_block.add_statement(FreeVariable(self.__name))


class IR_TempValue(IR_Value):

    def __init__(self):
        self.__value = None

    # set the temp
    def set_value(self, data):
        self.__value = data

    # returns the temp
    def get_value(self):
        return self.__value

    def add_free_operation(self, current_basic_block):
        current_basic_block.add_statement(FreeTemp(self))


class DefTemp(IR_Interface):
    def __init__(self):
        self.__temp = IR_TempValue()

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
        self._dest_temp.add_free_operation(current_basic_block)
        self._src_temp.add_free_operation(current_basic_block)


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


class JumpBlock(IR_Interface):

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


class JumpStatement(IR_Interface):
    def __init__(self):
        self.__label = None

    def add_free_operation(self, current_basic_block):
        pass

    def get_label(self):
        return self.__label

    def set_label(self, label):
        self.__label = label


class Jump(JumpStatement):
    pass


class JumpEquals(JumpStatement):
    pass


class JumpNotEquals(JumpStatement):
    pass


class JumpLess(JumpStatement):
    pass


class JumpGreater(JumpStatement):
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


class IR_Function_SymbolTabel(IR_Interface):

    def __init__(self):
        self.__vars = []

    def get_all_vars(self):

        for tabel in SymbolTable.Tables.get_instance().get_all_tables():
            for var_name in tabel.get_all_vars():
                self.__vars.append(var_name)

        return self.__vars

    def add_free_operation(self, current_basic_block):
        pass


class IR_Print(IR_Interface):
    def __init__(self, var_name):
        self.__var_name = var_name

    def get_var(self):
        return self.__var_name

    def add_free_operation(self, current_basic_block):
        pass


class IR_PrintString(IR_Interface):
    def __init__(self, string):
        self.__string = string

    def get_string(self):
        return self.__string

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
            self.visit(statement, context)

    @visitor(AST_Integer)
    def visit(self, integer, context):
        def_temp = DefTemp()
        temp = def_temp.get_temp()

        integer = IR_Integer(integer.get_value())
        set_temp = IR_AssignTemp(temp, integer)

        self.__main_function.get_current_basic_block().add_statement(def_temp)
        self.__main_function.get_current_basic_block().add_statement(set_temp)

        integer.add_free_operation(self.__main_function.get_current_basic_block())

        return temp

    @visitor(AST_Variable)
    def visit(self, variable, context):
        def_temp = DefTemp()
        temp = def_temp.get_temp()

        variable = IR_Variable(variable.get_name())
        set_temp = IR_AssignTemp(temp, variable)

        self.__main_function.get_current_basic_block().add_statement(def_temp)
        self.__main_function.get_current_basic_block().add_statement(set_temp)

        variable.add_free_operation(self.__main_function.get_current_basic_block())

        return temp

    @visitor(AST_NewVariable)
    def visit(self, new_variable, context):
        return new_variable.get_name()

    @visitor(AST_Expression)
    def visit(self, expression, context):
        dest_temp = self.visit(expression.get_expression_1(), context)
        src_temp = self.visit(expression.get_expression_2(), context)

        operation = self.visit(expression.get_operator(), context)
        operation.set_temps(dest_temp, src_temp)

        self.__main_function.get_current_basic_block().add_statement(operation)

        src_temp.add_free_operation(self.__main_function.get_current_basic_block())

        return dest_temp

    @visitor(AST_DefVar)
    def visit(self, def_var, context):
        self.visit(def_var.get_assignment(), context)

    @visitor(AST_Assignment)
    def visit(self, assignment, context):

        value = self.visit(assignment.get_value(), context)

        ir_assignment = IR_Assignment(assignment.get_name().get_name(), value)

        self.__main_function.get_current_basic_block().\
            add_statement(ir_assignment)

        value.add_free_operation(self.__main_function.get_current_basic_block())

    @visitor(Add_Operator)
    def visit(self, add_operator, context):
        return IR_AddOperation()

    @visitor(Sub_Operator)
    def visit(self, sub_operator, context):
        return IR_SUbOperation()

    @visitor(Mul_Operator)
    def visit(self, mul_operator, context):
        return IR_MulOperation()

    @visitor(Div_Operator)
    def visit(self, dev_operator, context):
        return IR_DevOperation()

    @visitor(Remainder_Operator)
    def visit(self, dev_res_operator, context):
        return IR_DevRestOperation()

    @visitor(LessOperatorAST)
    def visit(self, less_operator, context):
        return JumpLess()

    @visitor(GreaterOperatorAST)
    def visit(self, greater_operator, context):
        return JumpGreater()

    @visitor(EqualityOperatorAST)
    def visit(self, equality_operator, context):
        return JumpEquals()

    @visitor(NotEqualsOperatorAST)
    def visit(self, not_equals_operator, context):
        return JumpNotEquals()

    @visitor(AndOperator)
    def visit(self, and_operator, context):

        condition = context.get_condition()

        new_basic_block_label = IR_Label(self.__labels.get_new_label_name())

        new_basic_block = IR_BasicBlock(new_basic_block_label,
                                        self.__main_function.get_current_basic_block().get_jump_block())

        jump_to_else_part = Jump()

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

    @visitor(OrOperatorAST)
    def visit(self, or_condition, context):

        condition = context.get_condition()

        new_basic_block_label = IR_Label(self.__labels.get_new_label_name())

        new_basic_block = IR_BasicBlock(new_basic_block_label,
                                        self.__main_function.get_current_basic_block().get_jump_block())

        jump_to_else_part = Jump()
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

        jump_to_else_part = Jump()
        jump_to_else_part.set_label(else_part_label)

        if contains_else_part:
            merge_block_label = IR_Label(self.__labels.get_new_label_name())
        else:
            merge_block_label = else_part_label

        jump_to_merge_block = Jump()
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

        jump_to_cmp_block = Jump()
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

        jump_to_merge_block = Jump()
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
        expression_1 = self.visit(condition.get_expression_1(), context)
        expression_2 = self.visit(condition.get_expression_2(), context)

        operator = self.visit(condition.get_operator(), context)

        ir_condition = \
            IR_Condition(expression_1, operator, expression_2)

        return ir_condition

    @visitor(AST_ComplexCondition)
    def visit(self, condition, context):
        condition_1 = self.visit(condition.get_condition_1(), context)

        context.set_condition(condition_1)

        self.visit(condition.get_operator(), context)

        condition_2 = self.visit(condition.get_condition_2(), context)
        return condition_2

    @visitor(AST_Print)
    def visit(self, print_statement, context):
        ir_print = IR_Print(print_statement.get_var_name())
        self.__main_function.get_current_basic_block().add_statement(ir_print)

    @visitor(AST_PrintString)
    def visit(self, print_statement, context):
        ir_print = IR_PrintString(print_statement.get_string())
        self.__main_function.get_current_basic_block().add_statement(ir_print)
