from abc import abstractmethod


class Context:
    def __init__(self):
        self.__string = ""

    def append_string(self, string):
        self.__string += string

    def poll_string(self):
        return self.__string


class ASM_Generator:
    def __init__(self):
        self.__context = Context()

    def write(self, ir_program):
        self.gen(ir_program)
        return self.__context.poll_string()

    @abstractmethod
    def gen(self, ir_program):
        pass
