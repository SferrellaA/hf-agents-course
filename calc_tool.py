import tool

def multiplyfunc(a:int, b:int) -> int:
    return a * b

multiply = tool.Tool(
    "multiply", 
    "multiply two integers together", 
    multiplyfunc,
)

def getsecret()->str:
    return "the secret was inside you all along!"
secret = tool.Tool(
    "secret",
    "returns the secret answer",
    getsecret,
)
