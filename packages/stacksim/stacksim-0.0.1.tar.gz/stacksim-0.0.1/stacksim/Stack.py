import os
from typing import List
from enum import Enum
from jinja2 import Environment, PackageLoader, select_autoescape

from termcolor import colored
from stacksim.term_to_rich import termcolor_to_rich_markup
import yaml
#enum of cell types 

from stacksim.function import Function, FunctionArgument

rich_color_map = {
    'grey': 'gray',
    'red': 'red',
    'green': 'green',
    'yellow': 'yellow',
    'blue': 'blue',
    'magenta': 'magenta',
    'cyan': 'cyan',
    'white': 'white',
    'dark_grey': 'grey53',
    'dark_red': 'maroon',
    'dark_green': 'dark green',
    'dark_yellow': 'olive',
    'dark_blue': 'navy',
    'dark_magenta': 'purple',
    'dark_cyan': 'teal',
    'dark_white': 'silver'
}

class StackCell():
    def __init__(self, label = "???", words = []):
        self.address = None
        self.frame = None
        self.words = words
        self.note = None 
        self.size = 1
        self.label = ""
        self.color = None

    def setWords(self,words):

        #if not a list, make it a list
        if not isinstance(words, list):
            self.words = [words]
        else:
            self.words = words

        #remove any empty strings
        self.words = [x for x in self.words if x != "" or x != " "]


        self.size = len(self.words)

    @classmethod
    def fromObj(cls, obj):

        ret = StackCell()

        if not isinstance(obj, dict):
            ret.setWords(obj)
        
        else:

            key = list(obj.keys())[0]
            value = obj[key]

            ret.label = key

            if not isinstance(value, dict):
                ret.setWords(value)

            else:

                if 'words' in value:
                    ret.setWords(value['words'])
                    ret.size = len(ret.words)
                else:
                    ret.words = []

                if 'color' in value:
                    ret.color = value['color']

                if 'note' in value:
                    ret.note = value['note']

                if 'size' in value:
                    ret.size = value['size']



        return ret
    
    def toAscii(self, width = 80, leftMargin = 20, color = "blue", showAddress = True, sof = False):

        out = ""

        lmargin = " "*leftMargin

        lAddress = colored(f"{lmargin}")

        if showAddress and self.address:
            lAddress = colored(f"{hex(self.address).rjust(leftMargin)}", color="dark_grey")
            pass

        if self.color:
            color = self.color

        top = f"├{'─'*(width-2)}┤"

        header = self.label

        if self.size > 1:
            header = f"{self.label} [{self.size}]"

        if header and header != "":
            

            top = f"├{header.center(width-2,'─')}┤"

            topParts = top.split(header)

            top = colored(topParts[0], color=color) + colored(header, color="dark_grey") + colored(topParts[1], color=color)

            if sof:
                top = f"┌{header.center(width-2,'─')}┐"
        
        else:
            if sof:
                top = f"┌{'─'*(width-2)}┐"
        

        out += colored(f"{lmargin}{top}\n", color=color)

        if self.size == 1:
            if len(self.words) > 0:
                val = str(self.words[0])
                out += lAddress + colored(f"│{val.ljust(width-2)}│", color=color)
            else:
                out += lAddress+ colored(f"│{' '.ljust(width-2)}│", color=color)

            if self.note:
                out += colored(f" <-- {self.note}", color="red")
            
            out += "\n"
        else:
            vals = [""]

            if len(self.words) > 0:
                vals = self.words

            for i,val in enumerate(vals):
                strVal = str(val)

                if i == 0:

                    out+=  lAddress + colored(f"│{strVal.ljust(width-2)}│", color=color)

                    if self.note:
                        out += colored(f" <-- {self.note}", color="red")
                else:
                    out+=  lmargin + colored(f"│{strVal.ljust(width-2)}│", color=color)

                out += "\n"

            if len(vals) < self.size:
                out+= colored(f"{lmargin}:{" "*(width-2)}:\n", color=color)

        return out


    def toRich(self, width=80, leftMargin=20, color="blue", showAddress=True, sof=False):
        out = ""
        lmargin = " " * leftMargin
        lAddress = f"[grey53]{lmargin}[/grey53]"

        if showAddress and self.address:
            lAddress = f"[grey53]{hex(self.address).rjust(leftMargin)}[/grey53]"
        if self.color:
            color = self.color

        color = rich_color_map.get(color, color)
        
        top = f"├{'─' * (width - 2)}┤"
        if self.label and self.label != "":

            header = self.label
            if self.size > 1:
                header = f"{self.label} [{self.size}]"
            top = f"├{header.center(width - 2, '─')}┤"
            topParts = top.split(header)
            top = f"[{color}]{topParts[0]}[/{color}][grey53]{header}[/grey53][{color}]{topParts[1]}[/{color}]"
            if sof:
                top = f"┌{header.center(width - 2, '─')}┐"
        else:
            if sof:
                top = f"┌{'─' * (width - 2)}┐"
        out += f"[{color}]{lmargin}{top}\n[/{color}]"
        if self.size == 1:
            if len(self.words) > 0:
                val = str(self.words[0])
                out += lAddress + f"[{color}]│{val.ljust(width - 2)}│[/{color}]"
            else:
                out += lAddress + f"[{color}]│{' '.ljust(width - 2)}│[/{color}]"
            if self.note:
                out += f"[red] <-- {self.note}[/red]"
            out += "\n"
        else:
            vals = [""]
            if len(self.words) > 0:
                vals = self.words
            for i, val in enumerate(vals):
                strVal = str(val)
                if i == 0:
                    out += lAddress + f"[{color}]│{strVal.ljust(width - 2)}│[/{color}]"
                    if self.note:
                        out += f"[red] <-- {self.note}[/red]"
                else:
                    out += f"{lmargin}[{color}]│{strVal.ljust(width - 2)}│[/{color}]"
                out += "\n"
            if len(vals) < self.size:
                out += f"[{color}]{lmargin}:{' ' * (width - 2)}:\n[/{color}]"
        return out





class StackFrame():
    def __init__(self, function = None):
        self.function = function
        self.cells: List[StackCell] = []
        self.color = None
        

    def length(self):
        return len(self.cells)

    def pop(self):

        if len(self.cells) == 0:
            return False
        
        cell = self.cells[-1]

        if cell.size == 1:
            self.cells.pop()
        else :
            if(len(cell.words) > 0):
                cell.words.pop()
            cell.size -= 1
        
        return True
        
    
    def push(self, cell):
        self.cells.append(cell)

    def applyAddresses(self, baseAddress = 0x07f00000):

        for cell in self.cells:
            baseAddress -= cell.size
            cell.address = baseAddress
        
        return baseAddress
            

    @classmethod
    def fromObj(cls, obj, order = 'normal'):
            
        ret = cls()

        if 'function' in obj:
            ret.function = obj['function']
            ret.color = "blue"
        
        if 'stack' in obj:
            cells = []
            if order == 'normal':
                cells = reversed(obj['stack'])
            else:
                cells = obj['stack']

            for cell in cells:
                ret.push(StackCell.fromObj(cell))

        if 'color' in obj:
            ret.color = obj['color']

        return ret
    
    def toAscii(self, width = 80, leftMargin = 20, color= "blue", showAddress = False):

        #           ╭─main──────────────────────────────╮
        #  0x070000 │         i = 0x014                 │
        #           ├─────────────buffer────────────────┤
        #  0x070000 :        ...                        :
        #           ├─────────────arg1──────────────────┤
        #  0x070000 │         32                        | 
        #           ├──────────────arg1─────────────────┤
        #  0x070000 │         14                        │
        #           ╰──────────────arg2─────────────────╯

        out = ""

        lmargin = " "*leftMargin
        fill = "─"*(width - 2)

        if not self.function:
            color = "dark_grey"

        if self.color:
            color = self.color


        if self.function:
            fill = "─"*(width - (len(self.function) + 3))
            out += colored(f"{lmargin}╭─{self.function}{fill}╮\n", color=color)
        # else: 
        #     out += colored(f"{lmargin}┌{fill}┐\n",color=color)
        
        for i,cell in enumerate( reversed(self.cells)):
           
           sof = False
           if i == 0 and not self.function:
                sof = True
           out += cell.toAscii(width, leftMargin, color, sof=sof,showAddress=showAddress)

        if self.function:
            fill = "─"*(width - 2)
            out += colored(f"{lmargin}╰{'─'*(width - 2)}╯\n", color=color)
        else:
            out += colored(f"{lmargin}└{fill}┘\n",color=color)

        return out
        

    def toRich(self, width=80, leftMargin=20, color="blue", showAddress=False):
        out = ""
        lmargin = " " * leftMargin
        fill = "─" * (width - 2)
        if not self.function:
            color = "dark_grey"
        if self.color:
            color = self.color

        color = rich_color_map.get(color, color)

        if self.function:
            fill = "─" * (width - (len(self.function) + 3))
            out += f"[{color}]{lmargin}╭─{self.function}{fill}╮\n[/{color}]"
        for i, cell in enumerate(reversed(self.cells)):
            sof = False
            if i == 0 and not self.function:
                sof = True
            out += cell.toRich(width, leftMargin, color, sof=sof, showAddress=showAddress)
        if self.function:
            fill = "─" * (width - 2)
            out += f"[{color}]{lmargin}╰{'─' * (width - 2)}╯\n[/{color}]"
        else:
            out += f"[{color}]{lmargin}└{fill}┘\n[/{color}]"
        return out

        



class Stack():
    def __init__(self, baseAddress = 0x07f00000):
        self.frames: List[StackFrame] = []
        self.currentFrame = None
        self.bits = 32
        self.baseAddress = baseAddress
        self.endian = 'little'
        self.pointer = self.baseAddress
        self.nextAddress = self.baseAddress

    
    def popFrame(self):
        
        if self.currentFrame:
            self.frames.pop()

            if len(self.frames ) > 0:
                self.currentFrame = self.frames[-1]
            else:
                self.currentFrame = None

    def pushFrame(self, frame):
        self.frames.append(frame)
        self.currentFrame = self.frames[-1]

    def pop(self, count = 1):

        while count > 0:
            if self.currentFrame:

                if self.currentFrame.pop():
                    self.nextAddress += 1
                    self.pointer += 1
                    count -= 1

            
            if self.currentFrame.length() == 0:
                self.popFrame()
                

    
    def push(self, cell):

        if not self.currentFrame:
            self.pushFrame(StackFrame())

        if not cell.address:
            cell.address = self.nextAddress

        self.currentFrame.push(cell)
        self.nextAddress -= cell.size

        
    def call(self, function , args):

        if isinstance(function, Function):
            self.frames.append(StackFrame(function.name))
        else:
            self.frames.append(StackFrame(function))

    def applyAddresses(self, baseAddress = None):

        if not baseAddress:
            baseAddress = self.baseAddress

        self.nextAddr = baseAddress
        for frame in self.frames:
            self.nextAddr = frame.applyAddresses(self.nextAddr)

        return self.nextAddr
    
    def loadYaml(self, obj):
        

        if isinstance(obj, str):
            with open(obj) as f:
                obj = yaml.safe_load(f)
        
        if 'stackBase' in obj:
            self.baseAddress = obj['stackBase']
        
        if 'order' in obj:
            order = obj['order']

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
                    self.pushFrame(frame)
                    self.currentFrame = None
                else:
                        cell = StackCell.fromObj(node)
                        self.push(cell)
        
        self.applyAddresses()


    
    def toAscii(self, width = 50, showAddress = False, leftMargin = 20):
     
        # Another style 
        #           ╭─vuln──────────────────────────────╮
        #  0x070000 │                                   │
        #           ├───────────────────────────────────┤
        #  0x070000 │                                   | 
        #           ├───────────────────────────────────┤
        #  0x070000 │   <main+054>                      │ <- return to main
        #           ╰───────────────────────────────────╯
        #           ╭─main──────────────────────────────╮
        #           ├───────────────i───────────────────┤
        #  0x070000 │ 0x014                             │
        #           ├─────────────buffer────────────────┤
        #           :                                   : 
        #  0x070000 :  ...                              : 
        #           ├───────────────arg1────────────────┤
        #  0x070000 │ 17                                | 
        #           ├───────────────arg2────────────────┤
        #  0x070000 │ 38                                │
        #           ╰───────────────────────────────────╯
        #           ┌───────────────────────────────────┐
        #  0x070000 │     . . .                         │
        #           └───────────────────────────────────┘

        out = ""
        for i,frame in enumerate(reversed(self.frames)):
            
            color = "blue"
            if frame == self.currentFrame:
                color = "green"

            out += frame.toAscii(width,color=color, showAddress=showAddress)

        #Add end of stack

        if showAddress:
            out+= colored(f"{hex(self.baseAddress).rjust(leftMargin)}", color="dark_grey")
        else:
            out += colored(f"{" "*(leftMargin)}", color="dark_grey")
        out += colored(f" {"End Of Stack".center((width-2), '─')}\n", color="dark_grey")

        return out


    
    def toRich(self, width=50, showAddress=False, leftMargin=20):
        out = ""
        for i, frame in enumerate(reversed(self.frames)):
            color = "blue"
            if frame == self.currentFrame:
                color = "green"

            out += frame.toRich(width, leftMargin=leftMargin, color=color, showAddress=showAddress)
        if showAddress:
            out += f"[grey53]{hex(self.baseAddress).rjust(leftMargin)}[/grey53]"
        else:
            out += f"[grey53]{' ' * leftMargin}[/grey53]"
        out += f"[grey53]{' End Of Stack '.center((width - 2), '─')}\n[/grey53]"
        return out
    
    
    def generateHTML(self, showAddress = True):
        env = Environment(
            loader=PackageLoader('stacksim', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template('stack.html')
        html_output = template.render(stack=self, showAddress = showAddress)
        return html_output
    
    def print(self, showAddress= True, leftMargin = 20):
        
        ascii = self.toAscii(showAddress=showAddress, leftMargin=leftMargin)
        print(ascii)
        
    
    def generateImage(self):

        pass
        
