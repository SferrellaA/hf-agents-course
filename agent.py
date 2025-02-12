from openai import OpenAI
from calc_tool import multiply, secret
from random import choice

def message(role, content):
    if role not in ["system", "user", "assistant"]:
        raise ValueError(f"invalid role '{role}'")
    if type(content) is not str:
        content = str(content)
    return {"role": role, "content": content}
def sysm(content):
    return message("system", content)
def usrm(content):
    return message("user", content)
def astm(command, output):
    content = f'{command} -> "{output}"'
    return message("assistant", content)

def get_model(client: OpenAI)->str:
    try:
        return choice(client.models.list().data).id
    except:
        return ""

client = OpenAI(
    base_url="http://127.0.0.1:8080/v1",
    api_key="asdf"
)
#model = client.models.list().data[0].id
model = get_model(client)
print(f"Using model '{model}'")

tools = [secret]
tool_string = "\n\n".join([str(tool) for tool in tools])

messages = [
    sysm(f"""
You are a helpful assistant that answers user questions with all the tools available to you.

You have the following tools available to you:

{tool_string}

You should think step by step in order to fulfill the user's objective. You may call tools and see their responses repeatedly in order to find the final answer. If you would like to call an available tool, the last line of your response should be in format 'Tool: <tool_name> <args...>'; the output of that tool call will then be provided to you. If you would like to give the final answer to the user, the last line of your response should be in format 'Answer: <your answer>'. You should stop writing after you write your Tool or Answer line. Only one of Tool or Answer should be in your response; you should not include both in your response. If your response does not match either format it will be rejected. 

Example Part 1:
User message:
what's five times 2?

Your response:
I should call the multiply tool with the user's numbers.
Tool: multiply 5 2

Example Part 2:
Tool output:
10

Your response:
Answer: The answer is 10
    """)
]

def resolve(call):
    args = []
    if "(" in call and ")" in call:
        parts = call.split("(", 1)
        call = parts[0]
        args = parts[-1].rsplit(")", 1)[0]
        if ',' in args:
            args = args.replace(',', ' ')
        args = args.split()
    else:
        parts = call.split()
        call = parts[0]
        if len(parts) > 1:
            args += parts[1:]

    for tool in tools:
        if tool.name == call:
            return tool(*args)

user = input("> ")
messages.append(usrm(user))

while True:
    print(messages[-2])
    print(messages[-1])
    response = client.chat.completions.create(messages=messages, model=model)
    response = response.choices[0].message.content
    if "</think>" in response:
        response = response.split("</think>\n\n")[-1]
    if "Tool:" in response:
        response = response.split("Tool:")[-1]
        if "\n" in response:
            response = response.split("\n")[0]
        response = response.lstrip(' ').rstrip(' ')
        messages.append(usrm("Tool: " + response))
        messages.append(astm(response, resolve(response)))
    elif "Answer:" in response:
        response = "Answer: " + response.split("Answer:")[-1]
        messages.append(usrm(response))
        print("====================")
        print(response)
        break
    else:
        print("am I not catching this?")
        messages.append(usrm(response))

print("====================")
for message in messages:
    print(message)
