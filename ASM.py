from abc import abstractmethod


class Context:
    def __init__(self):
        self.__string = ""

        # data for write methods
        self.__data_size = None

    def append_string(self, string):
        self.__string += string

    def poll_string(self):
        return self.__string

    def set_data_size(self, size):
        self.__data_size = size

    def get_data_size(self):
        return self.__data_size


class ASM_Generator:
    def write(self, ir_program):
        self.gen(ir_program)
        return self.__context.poll_string()

    @abstractmethod
    def gen(self, ir_program):
        pass
