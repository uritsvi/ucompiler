from abc import abstractmethod


class Context:
    def __init__(self):
        self.__strings = []
        self.__strings.append(None)

        # data for write methods
        self.__data_size = None

    def push_string(self):
        string = ""
        self.__strings.append(string)

    def pop_string(self):
        last_string = self.__strings.pop()
        return last_string

    def append_string(self, string):
        self.__strings[-1] += string

    def set_data_size(self, size):
        self.__data_size = size

    def get_data_size(self):
        return self.__data_size


class ASM_Generator:
    @abstractmethod
    def gen(self, ir_program):
        pass
