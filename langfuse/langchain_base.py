from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough

from langfuse.callback import CallbackHandler
import os

 

model = ChatOpenAI(model="gpt-3.5-turbo")

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("you are aenglish teacher"),
    HumanMessagePromptTemplate.from_template("give me a sentence that contain short-phase {input}!") ,
    
])


# 定义输出解析器
parser = StrOutputParser()

chain = (
    {"input":RunnablePassthrough()} 
    | prompt
    | model
    | parser
)
print(os.environ["LANGFUSE_PUBLIC_KEY"])


user01=CallbackHandler(trace_name="langchain_trace",user_id="bjdzliu",public_key=os.environ["LANGFUSE_PUBLIC_KEY"],secret_key=os.environ["LANGFUSE_SECRET_KEY"])

response=chain.invoke(input="go through",config={"callbacks":[user01]})
print(response)