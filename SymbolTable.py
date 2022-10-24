from abc import abstractmethod


class Tables:
    __instance = None

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = Tables()

        return cls.__instance

    def __init__(self):
        first_table = SymbolTable(None)

        self.__tables = []
        self.__tables.append(first_table)

        self.__all_tables = []
        self.__all_tables.append(first_table)

        self.__vars_count = 0

    def get_current_table(self):
        return self.__tables[-1]

    def push_table(self):
        new_table = SymbolTable(self.get_current_table())

        self.__tables.append(new_table)
        self.__all_tables.append(new_table)

    def pop_top_table(self):
        self.__tables.pop()

    def get_all_tables(self):
        return self.__all_tables

    def get_new_var_name(self):
        string = "var_" + str(self.__vars_count)

        self.__vars_count += 1

        return string


class SymbolTabelVar:
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def is_pointer(self):
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

    def is_pointer(self):
        return False


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

    def is_pointer(self):
        return True


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
        if self.__parent is None:
            return None

        var = self.__parent.get_var(name)

        return var

    def __get_array_from_parent_scope(self, name):
        if self.__parent is None:
            return None

        array = self.__parent.get_array(name)

        return array

    def __get_var_name_from_parents(self, name):
        if self.__parent is None:
            return None

        var_name = \
            self.__parent.get_var_name(name)

        return var_name

    def __get_array_name_from_parents(self, name):
        if self.__parent is None:
            return None

        array_name = \
            self.__parent.get_array_name(name)

        return array_name

    def __var_accessible_in_parent_scope(self, name):
        if self.__parent is None:
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
        new_name = Tables.get_instance().get_new_var_name()
        self.__old_names[name] = new_name

        return new_name
