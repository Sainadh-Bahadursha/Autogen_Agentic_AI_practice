# Using inbuilt HTTP Tool

import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool
import os
from autogen_core.tools import FunctionTool
from dotenv import load_dotenv, dotenv_values

from autogen_ext.tools.http import HttpTool

# Load environment variables
# load_dotenv()
env_vars = dotenv_values(".env")
api_key = env_vars.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

model_client=OpenAIChatCompletionClient(model='gpt-4o-mini',api_key=api_key)


'''
{
  "fact": "Cats with long, lean bodies are more likely to be outgoing, and more protective and vocal than those with a stocky build.",
  "length": 121
}
'''

schema = {
        "type": "object",
        "properties": {
            "fact": {
                "type": "string",
                "description": "A random cat fact"
            },
            "length": {
                "type": "integer",
                "description": "Length of the cat fact"
            }
        },
        "required": ["fact", "length"],
    }


http_tool = HttpTool(
    name="cat_facts_api",
    description="get a cool cat fact",
    scheme="https",
    host="catfact.ninja",
    port=443,
    path="/fact",
    method="GET",
    return_type="json",
    json_schema= schema
)

agent = AssistantAgent(
    name="CatFactsAgent",
    model_client=model_client,
    system_message='You are a helpful assistant that can provide cat facts using the cat_facts_api tool. Give the result with summary',
    tools=[http_tool],
    reflect_on_tool_use=True
)



async def main(): 
    result = await agent.run(task = 'Give me a random cat fact')

    print(result.messages)

if (__name__ == "__main__"):
    asyncio.run(main())

# [TextMessage(id='4f530d79-9ce7-4aca-b1ee-e2c61233dc1c', 
# source='user', models_usage=None, metadata={}, created_at=datetime.datetime(2025, 7, 29, 17, 2, 4, 704195, tzinfo=datetime.timezone.utc), content='Give me a random cat fact', type='TextMessage'), ToolCallRequestEvent(id='5633951b-f8e1-4afc-8cb8-6ff62c3e2011', source='CatFactsAgent', models_usage=RequestUsage(prompt_tokens=98, completion_tokens=36), metadata={}, created_at=datetime.datetime(2025, 7, 29, 17, 2, 8, 322903, tzinfo=datetime.timezone.utc), content=[FunctionCall(id='call_Dkkg9DlVW6y7duenMZHIAtRf', arguments='{"fact":"Cats have five toes on their front paws, but only four toes on their back paws.","length":65}', name='cat_facts_api')], type='ToolCallRequestEvent'), ToolCallExecutionEvent(id='bef40188-76a9-4012-a351-f09cc2649050', source='CatFactsAgent', models_usage=None, metadata={}, created_at=datetime.datetime(2025, 7, 29, 17, 2, 8, 836948, tzinfo=datetime.timezone.utc), content=[FunctionExecutionResult(content='{\'fact\': \

# 'The first commercially cloned pet was a cat named "Little Nicky." He cost his owner $50,000, making him one of the most expensive cats ever.\', 
# 
# \'length\': 140}', 
# 
# name='cat_facts_api', call_id='call_Dkkg9DlVW6y7duenMZHIAtRf', is_error=False)],
# 
#  type='ToolCallExecutionEvent'), TextMessage(id='d1b22001-475b-46b3-8aa2-f56676f38d7c', source='CatFactsAgent', models_usage=RequestUsage(prompt_tokens=130, completion_tokens=39), metadata={}, created_at=datetime.datetime(2025, 7, 29, 17, 2, 10, 344477, tzinfo=datetime.timezone.utc), content='Here\'s an interesting cat fact: The first commercially cloned pet was a cat named "Little Nicky." He cost his owner $50,000, making him one of the most expensive cats ever.', type='TextMessage')]
