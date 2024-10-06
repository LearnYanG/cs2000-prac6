counter_equal = 0
counter_great = 0
counter_less_than = 0
counter_return = 0

class VMTranslator:

    def vm_push(segment, offset):
        '''Generate Hack Assembly code for a VM pop operation'''
        b_a = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
        }

        if segment == "constant":
            push = (
                f"@{offset}\n"
                "D=A\n"
                "@SP\n"
                "AM=M+1\n"
                "A=A-1\n"
                "M=D\n"
            )
        elif segment in b_a:
            push = (
                "@" + b_a[segment] + "\n"
                "D=M\n"
                "@" + str(offset) + "\n"
                "D=D+A\n"
                "A=D\n"
                "D=M\n"
                "@SP\n"
                "A=M\n"
                "M=D\n"
                "@SP\n"
                "M=M+1\n"
            )
        elif segment == "pointer" and offset == 0:
            push = (
                "@THIS\n"
                "D=M\n"
                "@SP\n"
                "AM=M+1\n"
                "A=A-1\n"
                "M=D\n"
            )
        elif segment == "pointer" and offset == 1:
            push = (
                "@THAT\n"
                "D=M\n"
                "@SP\n"
                "AM=M+1\n"
                "A=A-1\n"
                "M=D\n"
            )
        elif segment == "temp":
            push = (
                f"@{5+offset}\n"
                "D=M\n"
                "@SP\n"
                "A=M\n"
                "M=D\n"
                "@SP\n"
                "M=M+1\n"
            )
        elif segment == "static":
            push = (
                f"@{16+offset}\n"
                "D=M\n"
                "@SP\n"
                "A=M\n"
                "M=D\n"
                "@SP\n"
                "M=M+1\n"
            )

        return push


    def vm_pop(segment, offset):
        b_a = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
        }

        if segment in b_a:
            pop = (
                f"@{b_a[segment]}\n"
                "D=M\n"
                f"@{offset}\n"
                "D=D+A\n"
                "@R13\n"
                "M=D\n"
                "@SP\n"
                "AM=M-1\n"
                "D=M\n"
                "@R13\n"
                "A=M\n"
                "M=D\n"
            )
        elif segment == "pointer" and offset == 0:
            pop = (
                "@SP\n"
                "AM=M-1\n"
                "D=M\n"
                "@THIS\n"
                "M=D\n"
            )
        elif segment == "pointer" and offset == 1:
            pop = (
                "@SP\n"
                "AM=M-1\n"
                "D=M\n"
                "@THAT\n"
                "M=D\n"
            )
        elif segment == "temp":
            pop = (
                "@SP\n"
                "AM=M-1\n"
                "D=M\n"
                f"@{5+offset}\n"
                "M=D\n"
            )
        elif segment == "static":
            pop = (
                "@SP\n"
                "AM=M-1\n"
                "D=M\n"
                f"@{16+offset}\n"
                "M=D\n"
            )
        elif segment == "constant":
            pop = ""

        return pop

    def vm_add():
        addition = (
            "@SP\n"
            "AM=M-1\n"
            "D=M\n"
            "A=A-1\n"
            "M=D+M\n"
        )
        return addition


    def vm_sub():
        subtraction = (
            "@SP\n"
            "AM=M-1\n"
            "D=M\n"
            "A=A-1\n"
            "M=M-D\n"
        )
        return subtraction


    def vm_neg():
        negetive = (
            "@SP\n"
            "A=M-1\n"
            "M=-M\n"
        )
        return negetive


    def vm_eq():
        global counter_equal
        counter_equal += 1
        equal = (
            "@SP\n"
            "AM=M-1\n"
            "D=M\n"
            "A=A-1\n"
            "D=M-D\n"
            f"@TRUEEQ{counter_equal}\n"
            "D;JEQ\n"
            f"@FALSEEQ{counter_equal}\n"
            "0;JMP\n"
            f"(FALSEEQ{counter_equal})\n"
            "@SP\n"
            "A=M-1\n"
            "M=0\n"
            f"@END{counter_equal}\n"
            "0;JMP\n"
            f"(TRUEEQ{counter_equal})\n"
            "@SP\n"
            "A=M-1\n"
            "M=-1\n"
            f"@END{counter_equal}\n"
            "0;JMP\n"
            f"(END{counter_equal})"
        )
        return equal


    def vm_gt():
        global counter_great
        counter_great += 1
        great = (
            "@SP\n"
            "AM=M-1\n"
            "D=M\n"
            "A=A-1\n"
            "D=M-D\n"
            f"@TRUEGT{counter_great}\n"
            "D;JGT\n"
            f"@FALSEGT{counter_great}\n"
            "0;JMP\n"
            f"(FALSEGT{counter_great})\n"
            "@SP\n"
            "A=M-1\n"
            "M=0\n"
            f"@END{counter_great}\n"
            "0;JMP\n"
            f"(TRUEGT{counter_great})\n"
            "@SP\n"
            "A=M-1\n"
            "M=-1\n"
            f"@END{counter_great}\n"
            "0;JMP\n"
            f"(END{counter_great})"
        )
        return great


    def vm_lt():
        global counter_less_than
        counter_less_than += 1
        less_than = (
            "@SP\n"
            "AM=M-1\n"
            "D=M\n"
            "A=A-1\n"
            "D=M-D\n"
            f"@TRUELT{counter_less_than}\n"
            "D;JLT\n"
            f"@FALSELT{counter_less_than}\n"
            "0;JMP\n"
            f"(FALSELT{counter_less_than})\n"
            "@SP\n"
            "A=M-1\n"
            "M=0\n"
            f"@END{counter_less_than}\n"
            "0;JMP\n"
            f"(TRUELT{counter_less_than})\n"
            "@SP\n"
            "A=M-1\n"
            "M=-1\n"
            f"@END{counter_less_than}\n"
            "0;JMP\n"
            f"(END{counter_less_than})"
        )
        return less_than


    def vm_and():
        and_operation = (
            "@SP\n"
            "AM=M-1\n"
            "D=M\n"
            "A=A-1\n"
            "M=D&M\n"
        )
        return and_operation


    def vm_or():
        or_operation = (
            "@SP\n"
            "AM=M-1\n"
            "D=M\n"
            "A=A-1\n"
            "M=D|M\n"
        )
        return or_operation


    def vm_not():
        not_operation = (
            "@SP\n"
            "A=M-1\n"
            "M=!M\n"
        )
        return not_operation


    def vm_label(label):
        return f"({label})"


    def vm_goto(label):
        goto = f"@{label}\n0;JMP\n"
        return goto


    def vm_if(label):
        if_goto = (
            "@SP\n"
            "AM=M-1\n"
            "D=M\n"
            f"@{label}\n"
            "D;JNE\n"
        )
        return if_goto


    def vm_function(function_name, n_vars):
        n = f"({function_name})\n"
        function_code = ""
        for i in range(n_vars):
            function_code += (
                "@SP\n"
                "AM=M+1\n"
                "A=A-1\n"
                "M=0\n"
            )
        return n + function_code
    
    def vm_call(function_name, n_args):
        '''Generate Hack Assembly code for a VM call operation'''
        return ""

    def vm_return():
        '''Generate Hack Assembly code for a VM return operation'''
        return ""

# A quick-and-dirty parser when run as a standalone script.
if __name__ == "__main__":
    import sys
    if(len(sys.argv) > 1):
        with open(sys.argv[1], "r") as a_file:
            for line in a_file:
                tokens = line.strip().lower().split()
                if(len(tokens)==1):
                    if(tokens[0]=='add'):
                        print(VMTranslator.vm_add())
                    elif(tokens[0]=='sub'):
                        print(VMTranslator.vm_sub())
                    elif(tokens[0]=='neg'):
                        print(VMTranslator.vm_neg())
                    elif(tokens[0]=='eq'):
                        print(VMTranslator.vm_eq())
                    elif(tokens[0]=='gt'):
                        print(VMTranslator.vm_gt())
                    elif(tokens[0]=='lt'):
                        print(VMTranslator.vm_lt())
                    elif(tokens[0]=='and'):
                        print(VMTranslator.vm_and())
                    elif(tokens[0]=='or'):
                        print(VMTranslator.vm_or())
                    elif(tokens[0]=='not'):
                        print(VMTranslator.vm_not())
                    elif(tokens[0]=='return'):
                        print(VMTranslator.vm_return())
                elif(len(tokens)==2):
                    if(tokens[0]=='label'):
                        print(VMTranslator.vm_label(tokens[1]))
                    elif(tokens[0]=='goto'):
                        print(VMTranslator.vm_goto(tokens[1]))
                    elif(tokens[0]=='if-goto'):
                        print(VMTranslator.vm_if(tokens[1]))
                elif(len(tokens)==3):
                    if(tokens[0]=='push'):
                        print(VMTranslator.vm_push(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='pop'):
                        print(VMTranslator.vm_pop(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='function'):
                        print(VMTranslator.vm_function(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='call'):
                        print(VMTranslator.vm_call(tokens[1],int(tokens[2])))

        