
import re

class FunctionArgument():
    def __init__(self, type, name):
        self.name = name
        self.type = type

class Function():
    def __init__(self, name, address = "???", args= [], type = 'void'):
        self.name = name
        self.address = address
        self.args = args 
        self.type = type

    @classmethod
    def fromString(cls, line):
        
        #0x0040100 <int main(int, char**)>
        #int main(int argc, char **argv)
        #void doSomething(int a, int b)

        functionAddress = None

        regex = re.compile(r"(0x[0-9A-F]+)\S*?<(.*?)>")
        match = regex.match(line)

        if match:
            functionAddress = int(match.group(1), 16)
            line = match.group(2)
        

        #Parse the function definition
        regex = re.compile(r"(.*?[[*]?)(\w+)\((.*?)\)")
        match = regex.match(line)

        if match:
            returnType = match.group(1).replace(" ","")
            functionName = match.group(2)
            args = match.group(3).split(',')

            functionArgs = []
            for arg in args:

                arg = arg.strip()

                if arg and arg != "...":
                    argParts = arg.split(' ')

                    if 'const' in argParts:
                        argParts.remove('const')

                    argType = argParts[0]
                    argName = None

                    if len(argParts) > 1:
                        argName = argParts[1]

                        while argName[0] == '*':
                            argType += '*'
                            argName = argName[1:]

                    functionArgs.append(FunctionArgument(argType, argName))
            
            ret = cls(functionName, functionAddress, functionArgs, returnType)
        
            return ret 

        else : 
            
            print(f"No match: {line}")