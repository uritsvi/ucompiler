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


class SymbolTable:
    def __init__(self, parent):
        self.__vars = {}
        self.__parent = parent

    def add_var(self, name):
        new_name = Tables.get_instance().get_new_var_name()
        self.__vars[name] = new_name

        return new_name

    def get_var_name(self, name):
        var_name = self.__vars.get(name)

        if var_name is None:
            var_name = self.__parent.get_var_name(name)

        return var_name

    def __var_exist_in_parent_scope(self, name):
        if self.__parent is None:
            return False

        if self.__parent.var_accessible_in_scope(name):
            return True

        return False

    def var_exist_in_scope(self, name):
        if name in self.__vars.keys():
            return True

        return False

    def var_accessible_in_scope(self, name):
        if self.__vars.get(name) is not None:
            return True

        elif self.__var_exist_in_parent_scope(name):
            return True

        return False

    def get_all_vars(self):
        return self.__vars.values()
