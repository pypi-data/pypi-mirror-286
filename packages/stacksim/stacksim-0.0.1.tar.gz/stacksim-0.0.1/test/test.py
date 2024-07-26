from stacksim.StackSession import StackSession
from stacksim.Stack import Stack
import yaml

from rich import console

from rich.console import Console
from rich.text import Text


console = Console()

def test_StackSession():



    stack = Stack()


    stack.loadYaml("test/test1.stack.yml")

    #ascii = stack.toAscii(showAddress=True)
    rich = stack.toRich(showAddress=True)

    start = Text("Stack: ", style="bold blue")
    #stack.print()
    #print(ascii)

    console.print(rich)

    # print(rich)
    # print(start)
    

    html = stack.generateHTML()

    with open("test.html", "w") as f:
        f.write(html)




def main():
    test_StackSession()

if __name__ == "__main__":
    main()