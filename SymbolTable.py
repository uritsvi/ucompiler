from abc import abstractmethod


class FunctionParameter:
    def __init__(self, name, data_type):
        self.__name = name
        self.__data_type = data_type

    def get_name(self):
        return self.__name

    def get_data_type(self):
        return self.__data_type


class FunctionParameters:
    def __init__(self):
        self.__parameters = {}

    def add_parameter(self, name, parameter):
        self.__parameters[name] = parameter

    def get_all_parameters(self):
        return list(self.__parameters.values())

    def get_parameter(self, name):
        return self.__parameters[name]


class FunctionCallParameters:
    def __init__(self):
        self.__parameters = []

    def add_parameter(self, parameter):
        self.__parameters.append(parameter)

    def is_matching_function_parameters_list(self, function_name):
        function_table_name = \
            FunctionsTabel.get_instance().get_function_tabel_name(function_name)

        function_prototype = \
            FunctionsTabel.get_instance().get_function(function_table_name).get_function_prototype()

        function_prototype_parameters = \
            function_prototype.get_parameters().get_all_parameters()

        if len(self.__parameters) != \
                len(function_prototype_parameters):
            return False

        for i in range(len(function_prototype_parameters)):
            if not function_prototype_parameters[i].get_data_type().\
                    is_compatible_with(self.__parameters[i].get_data_type()):
                return False

        return True

    def get_all_parameters(self):
        return self.__parameters


class SymbolTableFunctionPrototype:
    def __init__(self, name, return_value_type):
        self.__name = name
        self.__return_value_type = return_value_type
        self.__parameters = None
        self.__parameters_name = {}
        self.__args_count = 0

    def get_name(self):
        return self.__name

    def get_return_value_type(self):
        return self.__return_value_type

    def set_parameters(self, parameters):
        self.__parameters = parameters

    def get_parameters(self):
        return self.__parameters

    def get_parameter_name(self, name):
        return self.__parameters_name.get(name)

    def var_in_parameters(self, name):
        if name in self.__parameters_name.keys():
            return True

        return False

    def get_var(self, name):
        return self.__parameters.get_parameter(name)

    def __get_new_arg_name(self):
        string = \
            "arg" + "_" + str(self.__args_count)

        self.__args_count += 1

        return string

    def map_arg_name_to_table_name(self, name):
        table_name = self.__get_new_arg_name()

        self.__parameters_name[name] = \
            table_name

        return table_name


class SymbolTabelFunction:
    def __init__(self, name, prototype):
        self.__name = name
        self.__current_tabel = SymbolTable(None)
        self.__prototype = prototype

        self.__vars_count = 0

        self.__tables = []
        self.__tables.append(self.__current_tabel)

        # When pop the current tabel the tables don't pop of this list
        self.__all_tables = []
        self.__all_tables.append(self.__current_tabel)

        self.__has_body = False

    def set_has_body(self, b):
        self.__has_body = b

    def has_body(self):
        return self.__has_body

    def get_name(self):
        return self.__name

    def get_new_var_name(self):
        new_var_name = "var" + "_" + str(self.__vars_count)

        self.__vars_count += 1

        return new_var_name

    def push_table(self):
        self.__tables.append(SymbolTable(self.__current_tabel))
        self.__all_tables.append(SymbolTable(self.__current_tabel))

    def pop_table(self):
        self.__tables.pop()

    def get_current_tabel(self):
        return self.__current_tabel

    def get_all_tables(self):
        return self.__all_tables

    def get_function_prototype(self):
        return self.__prototype


class FunctionsTabel:
    __instance = None

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = FunctionsTabel()

        return cls.__instance

    def __init__(self):
        self.__functions = {}
        self.__names = {}

        self.__counter = 0

        self.___current_function = None

        self.__current_tabel = None
        self.__current_prototype = None

    def add_function(self, function):
        self.__functions[function.get_name()] = function
        self.___current_function = function

    def get_current_tabel(self):
        current_label = self.___current_function.get_current_tabel()
        return current_label

    def get_current_function(self):
        return self.___current_function

    def __get_new_function_name(self):
        string = "f" + "_" + str(self.__counter)

        self.__counter += 1

        return string

    def map_function_name_to_table_name(self, name):
        new_name = self.__get_new_function_name()
        self.__names[name] = new_name

        return new_name

    def get_function_tabel_name(self, name):
        tabel_name = self.__names[name]
        return tabel_name

    def get_function(self, name):
        function = self.__functions.get(name)
        return function

    def get_current_prototype(self):
        return self.__current_prototype

    def set_current_prototype(self, prototype):
        self.__current_prototype = prototype


class SymbolTabelVar:
    @abstractmethod
    def get_name(self):
        pass


class Var(SymbolTabelVar):
    def __init__(self, name, data_type):
        self.__name = name
        self.__data_type = data_type

    def get_name(self):
        return self.__name

    def set_data_type(self, data_type):
        self.__data_type = data_type

    def get_data_type(self):
        return self.__data_type


class Array(SymbolTabelVar):
    def __init__(self, name, data_type):
        self.__name = name
        self.__data_type = data_type

    def get_name(self):
        return self.__name

    def set_data(self, data_type):
        self.__data_type = data_type

    def get_data(self):
        return self.__data_type

    def get_data_type(self):
        return self.__data_type.get_data_type()

    def get_size(self):
        return self.__data_type.get_array_size()


class SymbolTable:
    def __init__(self, parent):
        self.__vars = {}
        self.__arrays = {}

        self.__old_names = {}

        self.__parent = parent

    def add_var(self, name, data_type):
        new_var = Var(name, data_type)
        self.__vars[name] = new_var

    def add_array(self, name, data):
        new_var = Array(name, data)

        self.__arrays[name] = new_var

        return name

    def set_array_data(self, name, data):
        self.__vars[name].set_data(data)

    def get_var_name(self, name):
        var_name = self.__old_names.get(name)

        if var_name is None:
            var_name = self.__get_var_name_from_parents(name)

        return var_name

    def get_array_name(self, name):
        array_name = self.__old_names.get(name)

        if array_name is None:
            array_name = self.__get_array_name_from_parents(name)

        return array_name

    def get_var(self, name):
        var = self.__vars.get(name)

        if var is None:
            var = self.__get_var_from_parent_Scope(name)

        return var

    def get_array(self, name):
        var = self.__arrays.get(name)

        if var is None:
            var = self.__get_array_from_parent_scope(name)

        return var

    def __get_var_from_parent_Scope(self, name):
        if self.__parent is not None:
            var = self.__parent.get_var(name)
        else:
            var = FunctionsTabel.get_instance().get_current_function().\
                get_function_prototype().get_parameters().get_parameter(name)

        return var

    def __get_array_from_parent_scope(self, name):
        if self.__parent is None:
            return None

        array = self.__parent.get_array(name)

        return array

    def __get_var_name_from_parents(self, name):
        if self.__parent is not None:
            var_name = \
                self.__parent.get_var_name(name)
        else:
            var_name = FunctionsTabel.get_instance().get_current_function().\
                get_function_prototype().get_parameter_name(name)

        return var_name

    def __get_array_name_from_parents(self, name):
        if self.__parent is None:
            return None

        array_name = \
            self.__parent.get_array_name(name)

        return array_name

    def __var_accessible_in_parent_scope(self, name):
        if self.__parent is None:
            if FunctionsTabel.get_instance().get_current_function().get_function_prototype().var_in_parameters(name):
                return True

            return False

        return \
            self.__parent.var_accessible_in_scope(name)

    def __array_accessible_in_parent_scope(self, name):
        if self.__parent is None:
            return None

        return \
            self.__parent.array_accessible_in_scope(name)

    def var_exist_in_scope(self, name):
        if name in self.__vars.keys() or \
                name in self.__arrays.keys():

            return True

        return False

    def var_accessible_in_scope(self, name):
        if self.__vars.get(self.get_var_name(name)) is not None:
            return True

        return \
            self.__var_accessible_in_parent_scope(name)

    def array_accessible_in_scope(self, name):
        if self.__arrays.get(self.get_array_name(name)) is not None:
            return True

        return \
            self.__array_accessible_in_parent_scope(name)

    def get_all_vars(self):
        return self.__vars.values()

    def get_all_arrays(self):
        return self.__arrays.values()

    def map_var_name_to_symbol_tabel_name(self, name):
        new_name = FunctionsTabel.get_instance().\
            get_current_function().get_new_var_name()

        self.__old_names[name] = new_name

        return new_name
