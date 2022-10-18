from abc import abstractmethod


class DataType:
    @abstractmethod
    def get_size_in_bites(self):
        pass

    @abstractmethod
    def write_name(self):
        pass

    @abstractmethod
    def get_print_format(self):
        pass


class int_32(DataType):
    def __init__(self):
        self.__size_in_bites = 4
        self.__name = "int_32"

    def get_size_in_bites(self):
        return self.__size_in_bites

    def write_name(self):
        return self.__name

    def get_print_format(self):
        return "\"%d\\n\""


class char(DataType):
    def __init__(self):
        self.__size_in_bites = 1
        self.__name = "char"

    def get_size_in_bites(self):
        return self.__size_in_bites

    def write_name(self):
        return self.__name

    def get_print_format(self):
        return "\"%c\\n\""
