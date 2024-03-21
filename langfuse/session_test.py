import uuid
from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    AIMessage, #等价于OpenAI接口中的assistant role
    HumanMessage, #等价于OpenAI接口中的user role
    SystemMessage #等价于OpenAI接口中的system role
)
from langfuse.callback import CallbackHandler
import os

llm = ChatOpenAI()

messages = [
    SystemMessage(content="你是物理老师。"), 
]

handler = CallbackHandler(
    user_id="bjdzliu",
    #session包含多个trace
    session_id="my_chat_session"
)


while True:
    user_input=input("User: ")
    if user_input.strip() == "":
        break
    messages.append(HumanMessage(content=user_input))
    response = llm.invoke(messages,config={"callbacks":[handler]})
    print("AI: "+response.content)
    #response作为AIMessage被添加到 messages 中
    messages.append(response)
    print(response)
    print(messages)