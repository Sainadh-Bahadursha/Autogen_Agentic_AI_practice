import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")


model_client=OpenAIChatCompletionClient(model='gpt-4o',api_key=api_key)

def reverse_string(text: str) -> str:
    '''
    Reverse the given text

    input:str

    output:str

    The reverse string is returned.
    '''
    return text[::-1]

reverse_tool = FunctionTool(reverse_string,description='A tool to reverse a string')



agent = AssistantAgent(
    name="ReverseStringAgent",
    model_client= model_client,
    system_message='You are a helpful assistant that can reverse string using reverse_string tool. Give the result with summary',
    tools=[reverse_tool],
    reflect_on_tool_use=True
)

async def main(): 
    result = await agent.run(task = 'Reverse the string "Hello, World!"')

    print(result.messages)

if (__name__ == "__main__"):
    asyncio.run(main())

    print(reverse_string("Hello, World!"))


# [TextMessage(id='8a16b184-abe7-4c0d-be6a-9a2f15b64326', 
# source='user', 
# models_usage=None,
#  metadata={}, 
# created_at=datetime.datetime(2025, 7, 29, 15, 53, 32, 364338, 
# tzinfo=datetime.timezone.utc), 
# content='Reverse the string "Hello, World!"', 
# type='TextMessage'),
# 
#  ToolCallRequestEvent(id='06450edb-8fb5-4ab3-bb24-26c2aa173045', 
# source='ReverseStringAgent',
#  models_usage=RequestUsage(prompt_tokens=79, completion_tokens=17),
#  metadata={}, 
# created_at=datetime.datetime(2025, 7, 29, 15, 53, 34, 918809, tzinfo=datetime.timezone.utc), 
# content=[FunctionCall(id='call_SfniGLDZJvIgzMWjaUeou2P2',
#  arguments='{"text":"Hello, World!"}', 
# name='reverse_string')], 
# type='ToolCallRequestEvent'), 
# 
# ToolCallExecutionEvent(id='7112f277-7dc9-4e8c-99c7-237b63938863',
#  source='ReverseStringAgent', 
# models_usage=None, 
# metadata={}, 
# created_at=datetime.datetime(2025, 7, 29, 15, 53, 34, 920859, 
# tzinfo=datetime.timezone.utc),
#  content=[FunctionExecutionResult(content='!dlroW ,olleH', name='reverse_string', call_id='call_SfniGLDZJvIgzMWjaUeou2P2', is_error=False)], type='ToolCallExecutionEvent'),
# 
#  TextMessage(id='5ce2fea2-3259-4d5e-9028-a2e9a22e70ad', 
# source='ReverseStringAgent', 
# models_usage=RequestUsage(prompt_tokens=71, 
# completion_tokens=19), metadata={}, 
# created_at=datetime.datetime(2025, 7, 29, 15, 53, 35, 943994,
#  tzinfo=datetime.timezone.utc), 
# content='The reverse of the string "Hello, World!" is "!dlroW ,olleH".',
#  type='TextMessage')]
# !dlroW ,olleH