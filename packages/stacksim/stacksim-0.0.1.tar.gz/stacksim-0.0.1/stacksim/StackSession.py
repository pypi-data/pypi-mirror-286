
from stacksim.CdeclConvention import CdeclConvention
from stacksim.Stack import Stack, StackFrame, StackCell
from stacksim.function import Function, FunctionArgument
import re
import yaml
import json
import argparse



class StackSession():
    def __init__(self):
        self.conv = CdeclConvention()
        self.stack = self.conv.stack
        self.functions = {}
        self.parser = argparse.ArgumentParser(description='Stack Visualizer')
        self.init_args()

    def loadYaml(self, obj):


        if isinstance(obj, str):
            with open(obj) as f:
                obj = yaml.safe_load(f)


        order = 'normal'

        if 'stackBase' in obj:
            self.stack.baseAddress = obj['stackBase']
        
        if 'order' in obj:
            order = obj['order']

        if 'functions' in obj:
            for func in obj['functions']:
                self.addFunction(Function.fromString(func))
    

        if 'stack' in obj:

            nodes = []
            if order == 'normal':
                nodes = reversed(obj['stack'])
            else:
                nodes = obj['stack']

            for node in nodes:
                
               if isinstance(node, dict) and 'function' in node:
                   #Create a new frame 
                   frame = StackFrame.fromObj(node, order= order)
                   self.stack.pushFrame(frame)
                   self.stack.currentFrame = None
               else:
                    cell = StackCell.fromObj(node)
                    self.stack.push(cell)
        
        self.stack.applyAddresses()


    


    def addFunction(self, function):
        self.functions[function.name] = function

    def parseFrame(self,words):
        
        line = " ".join(words[1:])
        self.stack.pushFrame(StackFrame(line))

    def frameCmd(self, args):
        frame = StackFrame(args.name)
        if args.color:
            frame.color = args.color
        self.stack.pushFrame(frame)

    def popCmd(self, args):
        if args.count:
            self.stack.pop(args.count)
        else:
            self.stack.pop()

    def pushCmd(self, args):
        cell = StackCell()

        if args.value:

            line = " ".join(args.value)

            parts = line.split(":")

            if len(parts) > 1:
                cell.label = parts[0]

                words = parts[1].strip().split(",")
                words = [x.strip() for x in words]

                cell.setWords(words)
            else:
                words = parts[0].split(",")
                words = [x.strip() for x in words]
                cell.setWords(parts[0].split(","))


        if args.size:
            cell.size = args.size
        
        if args.label:
            cell.label = args.label

        if args.address:
            cell.address = args.address

        if args.note:
            cell.note = args.note



        self.stack.push(cell)


    def parseFunction(self, line):

        function = Function.fromString(line)
        self.addFunction(function)

    def parsePush(self, line):
        """
            Parse a push command 
        """
        words = line.split(" ")
        line = " ".join(words[1:])

        obj = yaml.safe_load(line)

        cell = StackCell.fromObj(obj)

        self.stack.push(cell)

        pass

    def parsePop(self, words):
        """
            Parse a pop command 
        """

        if len(words) > 1:
            if words[1] == "frame":
                self.stack.popFrame()
            else:
                if words[1].isnumeric():
                    self.stack.pop(int(words[1]))
                else:
                    print("Invalid pop command")
                    return
        else:
            self.stack.pop()
            

        pass

    def parseCall(self, line):
        """
            Parse a call command 
        """
        pass

        

    def parseCommand(self, line):
        """
            Handles a command 

            #Define a function
            function addTwo@0x454545(int a, int b)

            #Push to the stack
            push 0x00000001 # Push a single word 
            push [1,23,4,5] # Push multiple words 
            push "sting of data" Push a string  
            push 0x00*45  push 45 words of same value 
            push [1,2,3]*45 push 

            #Pop from the stack
            pop
            pop 4 # pop 4 words 
            pop frame # pop the current frame

            #Call a defined Function 
            call addTwo 4 5 

            #Call undefined function 
            call addThree[0x455677] int32:45 int32:34 int32:456
        """

        # words = line.split(" ")

        # if words[0] == "frame":
        #     self.parseFrame(words)
        # elif words[0] == "function":
        #     self.parseFunction(line)
        # elif words[0] == "push":
        #     self.parsePush(line)
        # elif words[0] == "pop":
        #     self.parsePop(words)
        # elif words[0] == "call":
        #     self.parseCall(line)
        # else:
        #     print("Unknown command")
        #     return
        # pass 

        args = self.parser.parse_args(line.split(" "))

        #print(args)
        args.func(args)



    # Initialize the argument parser
    def init_args(self):

        subparsers = self.parser.add_subparsers(dest='command', help='sub-command help')

        # pop command
        pop_parser = subparsers.add_parser('pop', help='pop help')

        pop_parser.add_argument('count', type=int, nargs='?', help='Number of elements to pop', default=1)
        pop_parser.set_defaults(func=self.popCmd)
        
        #push command
        push_parser = subparsers.add_parser('push', help='push help')
        push_parser.add_argument('value', nargs='*', help='Value to push', default='')
        push_parser.add_argument('--size', type=int, help='Type of value')
        push_parser.add_argument('--label','-l', help='Label for the value')
        push_parser.add_argument('--address','-a', help='Address for the value')
        push_parser.add_argument('--note','-n', help='Note for the value')
        push_parser.set_defaults(func=self.pushCmd)

        #frame command
        frame_parser = subparsers.add_parser('frame', help='frame help')
        frame_parser.add_argument('name', help='Name of the frame')
        frame_parser.add_argument('--color', help='Color of the frame', default='blue')
        frame_parser.set_defaults(func=self.frameCmd)