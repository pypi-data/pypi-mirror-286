

from stacksim.Stack import Stack, StackFrame, StackCell 
from stacksim.function import Function, FunctionArgument
from stacksim.CallingConvention import CallingConvention, Register
from typing import List

from pwn import p32
import re

class CdeclConvention(CallingConvention):
    def __init__(self):
        super().__init__('cdecl')
        self.wordSize = 4
        self.endian = 'little'

        self.registers = {
            'eax': Register('eax', 4, 'Return Value'),
            'ecx': Register('ecx', 4, 'Arg 1'),
            'edx': Register('edx', 4, 'Arg 2'),
            'ebx': Register('ebx', 4, 'Arg 3'),
            'esp': Register('esp', 4, 'Stack Pointer'),
            'ebp': Register('ebp', 4, 'Base Pointer'),
            'esi': Register('esi', 4, 'Source Index'),
            'edi': Register('edi', 4, 'Destination Index'),
            'eip': Register('eip', 4, 'Instruction Pointer')
        }



    
    def call(self, function  : Function, args : List[FunctionArgument]):


        for arg in reversed(args):
            self.push(arg)

        # Push the return address
        self.stack.push(p32(self.registers['eip'].value), 'return Address')

        self.stack.pushFrame(StackFrame(function.name))



        