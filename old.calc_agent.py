from openai import OpenAI
import inspect

class Tool:
    def __init__(
        self,
        name: str,
        description: str,
        inputs: list,
        output: type,
        func: callable,
        example: str = None,
    ):
        self.name = name
        self.description = description
        self.inputs = inputs
        self.output = output
        self.func = func
        self.example = example

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
    
    def __str__(self):
        help  = f"Tool Name: {self.name}\n"
        help += f" Description: {self.description}\n"
        help += f" Arguments: {', '.join([str(arg) for arg in self.inputs])}\n"
        help += f" Output: {self.output}\n"
        if self.example:
            help += f" Ex: {self.example}\n"
        return help

def calculator(a:int, b:int) -> int:
    return a * b
calc = Tool(
    "calculator", 
    "multiple two integers together", 
    [int, int],
    int,
    calculator,
    "'calculator 5 2' --> 10"
)

client = OpenAI(
    base_url="http://127.0.0.1:8080/v1",
    api_key="asdf"
)
model = client.models.list().data[0].id
print(f"Going to use model '{model}'\n")

print(calc)
print(calc(5, 2))
