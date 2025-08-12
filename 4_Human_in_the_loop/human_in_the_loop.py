import asyncio
from codecs import StreamReader
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from dotenv import load_dotenv,dotenv_values
from autogen_agentchat.ui import Console
import os

load_dotenv()
env_vars = dotenv_values(".env")
api_key = env_vars.get("OPENAI_API_KEY")
model_client = OpenAIChatCompletionClient(model='gpt-4o-mini', api_key=api_key)



assistant = AssistantAgent(
    name='Assistant',
    description='you are a great assistant',
    model_client=model_client,
    system_message='You are a really helpful assistant who help on the task given.'
)

user_proxy_agent = UserProxyAgent(
    name ='UserProxy',
    description='you are a user proxy agent',
    input_func=input
)

termination_condition = TextMentionTermination(text='APPROVE')


team = RoundRobinGroupChat(
    participants=[assistant, user_proxy_agent],
    termination_condition=termination_condition,
    max_turns=10
)

stream = team.run_stream(task = 'Write a great poem about india?')

async def main():
    await Console(stream)

if (__name__ == '__main__'):
    asyncio.run(main())