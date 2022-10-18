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


class Var:
    def __init__(self, name, data_type):
        self.__name = name
        self.__data_type = data_type

    def get_name(self):
        return self.__name

    def set_data_type(self, data_type):
        self.__data_type = data_type

    def get_data_type(self):
        return self.__data_type


class SymbolTable:
    def __init__(self, parent):
        self.__vars_old_names = {}
        self.__vars_new_names = {}

        self.__parent = parent

    def add_var(self, name):
        new_name = Tables.get_instance().get_new_var_name()

        new_var = Var(new_name, None)

        self.__vars_old_names[name] = new_var
        self.__vars_new_names[new_name] = new_var

        return new_name

    def set_var_data_type(self, name, type):
        self.__vars_new_names[name].set_data_type(type)

    def get_var_name(self, name):
        var_name = self.__vars_old_names.get(name)

        if var_name is not None:
            var_name = var_name.get_name()
        else:
            var_name = self.__parent.get_var_name(name)

        return var_name

    def get_var(self, name):
        var = self.__vars_new_names.get(name)

        if var is None:
            var = self.__parent.get_var(name)

        return var

    def __var_exist_in_parent_scope(self, name):
        if self.__parent is None:
            return False

        if self.__parent.var_accessible_in_scope(name):
            return True

        return False

    def var_exist_in_scope(self, name):
        if name in self.__vars_old_names.keys():
            return True

        return False

    def var_accessible_in_scope(self, name):
        if self.__vars_old_names.get(name) is not None:
            return True

        elif self.__var_exist_in_parent_scope(name):
            return True

        return False

    def get_all_vars(self):
        return self.__vars_old_names.values()
