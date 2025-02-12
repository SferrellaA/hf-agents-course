from inspect import signature

class Tool:
    def __init__(
        self,
        name: str,
        description: str,
        func: callable,
    ):
        self.name = name
        self.description = description
        self.func = func

    def __call__(self, *args, **kwargs):
        try:
            return self.func(*args, **kwargs)
        except Exception as e:
            return f'Error: "{e}"'
    
    def __str__(self):
        help  = f"Tool Name: {self.name}\n"
        help += f"   Description: {self.description}\n"
        help += f"   Usage: {self.name}{signature(self.func)}"
        return help

    def help(self) -> str:
        return str(self)

'''
class Bin(Tool):
    the path to the binary to call
    bin -h for usage
    bool interactive
    bool sandboxed
    timeout
'''
