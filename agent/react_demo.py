from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv

script_dir = os.path.dirname(__file__)
EnvCconfigPath = os.path.dirname(os.path.dirname(script_dir))
envfile="platform_env"

load_dotenv(EnvCconfigPath+"/"+envfile)
OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')
OPENAI_API_BASE=os.environ.get('OPENAI_API_BASE')

client = OpenAI(
    api_key = OPENAI_API_KEY,
    base_url = OPENAI_API_BASE
)
instruction = """
you shuold follow the instruction to answer the question.
1.Each time you make a decision, you use only one tool, and you can use it as many times as you like.
2.Ensure that the command you invoke or the tool you use is included in the following given list of tools.

Answer the following questions as best you can. You have access to the following tools:

[
Name: github_api. Description: Retrieve information about a specified GitHub repository.
Name: jenkins_api. Description: Retrieve information about a specified Jenkins job.
]

If you find you need to find information from one of these tools, you can use the corresponding action. Tell me what action you want to take, and I will provide you with the information you need.
If you need action, tell me the action name and wait for the result i send you.

Print the content using the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [github_api, jenkins_api]
Action Input: the input to the action

Begin!
"""

input_text = """
Question: What is the latest commit in the repository demo2_jenkinsfile in github?
"""
tool_output = ''

prompt = f"""
{instruction}

Question: 
{input_text}
"""
messages = [{"role": "user", "content": prompt}] 

chat_completion = client.chat.completions.create(
    messages=messages,
    model="gpt-3.5-turbo", #此处更换其它模型,请参考模型列表 eg: google/gemma-7b-it
)
print(chat_completion.choices[0].message.content)
# parse Action: github_api
re=chat_completion.choices[0].message.content.split("Action:")[1].split("Action Input:")[0].strip()
print(re)


