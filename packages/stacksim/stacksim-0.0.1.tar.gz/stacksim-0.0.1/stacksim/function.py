
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
            regex = re.compile(r"(\w+)\s+(\w+)\((.*?)\)")
            match = regex.match(line)

            if match:
                returnType = match.group(1)
                functionName = match.group(2)
                args = match.group(3).split(',')

                functionArgs = []
                for arg in args:
                    arg = arg.strip()
                    if arg:
                        argParts = arg.split(' ')
                        argType = argParts[0]
                        argName = None

                        if len(argParts) > 1:
                            argName = argParts[1]

                            while argName[0] == '*':
                                argType += '*'
                                argName = argName[1:]

                        functionArgs.append(FunctionArgument(argType, argName))
                
                ret = cls(functionName, functionAddress, functionArgs, returnType)

        else:
            ret = cls(line)
            

        return ret