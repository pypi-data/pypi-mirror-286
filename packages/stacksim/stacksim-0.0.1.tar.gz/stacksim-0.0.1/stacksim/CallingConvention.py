
from stacksim.Stack import Stack, StackFrame, StackCell 
from stacksim.function import Function, FunctionArgument


class Register():
    def __init__(self, name, size, description):
        self.name = name
        self.size = size
        self.type = type
        self.value = None
        self.description = None


class CallingConvention():
    """
        Base Class for calling conventions
    """
    def __init__(self, name):
        self.name = name
        self.stack = Stack()
        self.wordSize = 4
        self.endian = 'little'
        self.registers = {}


    def pop(self):
       return self.stack.pop()

    def push(self,cell):
        self.stack.push(cell)
    
    def popFrame(self):
       return self.stack.popFrame()
    
    def pushFrame(self, frame):
        self.stack.pushFrame(frame)

    def call(self, function, args):

        self.stack.pushFrame(StackFrame(function.name))
        

