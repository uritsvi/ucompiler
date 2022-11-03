import os

import LexAndYacc
import ASM_X86
import IR
import XML_Writer


class Compiler:
    def __init__(self, src_file):

        with open(src_file, "r") as source_file:
            code = source_file.read()

        LexAndYacc.Lex.get_instance().parse_to_tokens(code)
        main_AST = LexAndYacc.Yacc.get_instance().pars(code)

        program_in_xml = XML_Writer.AST_XML_Program()

        ast_text = program_in_xml.write_xml(main_AST)
        print(ast_text)

        ir_gen = IR.IR_Generator()
        ir_program = ir_gen.gen(main_AST)

        all_function = ir_program.get_all_functions()

        bb_text = ""

        for function in all_function:
            bb_text += function.write_basic_blocks() + "\n"

        print(bb_text)

        asm = ASM_X86.ASM_X86_Generator()
        asm_code = asm.gen(ir_program)
        print(asm_code)

        file_name = os.path.join(os.getcwd(), src_file.rsplit('.', maxsplit=1)[0] + ".asm")
        os.chdir(os.path.dirname(src_file))
        with open(file_name, "w") as file:
            file.write(asm_code)

        ret = os.system("C:\\masm32\\bin\\ml /coff" + " " + file_name + " " + "-link /subsystem:console")

        if ret != 0:
            exit(-1)
