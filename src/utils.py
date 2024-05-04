# %%
import anthropic
import os
from dataclasses import dataclass
from enum import Enum


# %%
API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=API_KEY)

class MODELS(Enum):
    opus = "claude-3-opus-20240229"
    sonnet = "claude-3-sonnet-20240229"
    haiku = "claude-3-haiku-20240307"

DEFAULT_MAX_TOKENS = 4096
# %%
@dataclass
class Tool:
    name: str
    description: str
    input_schema: dict # JSON schema
    callback: callable

    def __call__(self, **kwargs):
        return self.callback(**kwargs)
    
    def get_api_representation(self):
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema
        }

# %%
terminal_tool = Tool(
    name="terminal",
    description="Run a command in a UNIX terminal",
    input_schema={
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The command to run in the terminal",
            }
        },
        "required": ["command"],
    },
    callback=lambda command: os.popen(command["command"]).read()
)

# %%
query_tool = Tool(
    name="query",
    description="Query a database. The database has the following schema: ...", # TODO: add schema
    input_schema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The SQL query to run",
            }
        },
        "required": ["query"],
    },
    callback=lambda query: os.popen(f"sqlite3 /path/to/database.db '{query['query']}'").read()
)

# %%
# def ask_ai(prompt):
#     response = client.messages.create(
#         model=opus,
#         max_tokens=max_tokens,
#         messages=[
#             {"role": "user", "content": prompt}
#         ]
#     )
#     return response.content[0].text

# %%
def ask_ai(prompt: str, tools: list[Tool] = [], model = MODELS.haiku, max_tokens = DEFAULT_MAX_TOKENS) -> str:
    tool_inputs = [tool.get_api_representation() for tool in tools]

    messages = [{"role": "user", "content": prompt}]

    while True:
        response = client.beta.tools.messages.create(
            model=model,
            max_tokens=max_tokens,
            tools=tool_inputs,
            messages=messages
        )

        stop_reason = response.stop_reason

        if stop_reason == "tool_use":
            # find the content blocks of type "tool_use"
            tool_use_messages = [message for message in response.content if message.type == "tool_use"]

            for tool_use_message in tool_use_messages:
                tool_error = False
                tool_name = tool_use_message.name
                tool_id = tool_use_message.id
                tool_input = tool_use_message.input

                # find the tool that was used
                tool = next(tool for tool in tools if tool.name == tool_name)

                # run the tool
                try:
                    tool_output = tool(**tool_input)
                except Exception as e:
                    tool_output = str(e)
                    tool_error = True

                messages.append({
                    "role": "assistant",
                    "content": response.content,
                })

                messages.append({
                    "role": "user",
                    "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_id,
                                "content": tool_output,
                                "is_error": tool_error,
                            }
                        ],
                })

                

        else:
            response_text = [message for message in response.content if message.type == "text"][0].text

            return response_text

# # %%

# response = client.beta.tools.messages.create(
#     model="claude-3-opus-20240229",
#     max_tokens=1024,
#     tools=[
#         {
#             "name": "get_weather",
#             "description": "Get the current weather in a given location",
#             "input_schema": {
#                 "type": "object",
#                 "properties": {
#                     "location": {
#                         "type": "string",
#                         "description": "The city and state, e.g. San Francisco, CA",
#                     }
#                 },
#                 "required": ["location"],
#             },
#         }
#     ],
#     messages=[{"role": "user", "content": "What's the weather like in San Francisco?"}],
# )
# print(response)

# %%
print(ask_ai("what is the meaning of life?"))

# %%
print(ask_ai("Can you run and test a terminal command to find the median file in my directory by timestamp?", [terminal_tool]))

# %%
'''''''''

'''










# %%
