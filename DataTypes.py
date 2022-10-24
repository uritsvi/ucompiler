from abc import abstractmethod
from typing import Final

# constants

INT_32_SIZE_IN_BITES: Final[int] = 4

CHAR_SIZE_IN_BITES: Final[int] = 1

VOID_SIZE_IN_BITES: Final[int] = 1

INT_32_PRINT_FORMAT: Final[str] = "\"%d\\n\""
CHAR_PRINT_FORMAT: Final[str] = "\"%c\\n\""
ARRAY_PRINT_FORMAT: Final[str] = "\"%s\\n\""


class DataType:
    @abstractmethod
    def get_size_in_bites(self):
        pass

    @abstractmethod
    def get_print_format(self):
        pass


class int_32(DataType):
    def __init__(self):
        self.__size_in_bites = INT_32_SIZE_IN_BITES

    def get_size_in_bites(self):
        return self.__size_in_bites

    def get_print_format(self):
        return INT_32_PRINT_FORMAT


class char(DataType):
    def __init__(self):
        self.__size_in_bites = CHAR_SIZE_IN_BITES

    def get_size_in_bites(self):
        return self.__size_in_bites

    def get_print_format(self):
        return CHAR_PRINT_FORMAT


class Array(DataType):
    def __init__(self, data_type, size):
        self.__data_type = data_type
        self.__size = size

    def get_size_in_bites(self):
        return self.__data_type.get_size_in_bites()

    def get_data_type(self):
        return self.__data_type

    def get_array_size(self):
        return self.__size

    def get_print_format(self):
        return ARRAY_PRINT_FORMAT
