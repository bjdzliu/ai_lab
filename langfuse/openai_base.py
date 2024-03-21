from datetime import datetime
from langfuse.openai import openai
from langchain_openai import OpenAI
from langfuse import Langfuse 
import os

class openai_langfuse:
    def __init__(self,name,user_id,release) -> None:
        self.name=name
        self.user_id=user_id
        self.release=release

    def _create_openai(self) -> openai:
        self_api_key = os.environ["devcto_key"]
        self_baseurl = os.environ["devcto_baseurl"]
        client = openai.OpenAI(
        api_key = self_api_key,
        base_url = self_baseurl
    )
        return client

    def _create_trace(self):
        trace = Langfuse().trace(
        name = self.name,
        user_id = self.user_id,
        release = self.release
     )
        return trace

    def call_openai(self):
        client=self._create_openai()
        trace=self._create_trace()
        completion = client.chat.completions.create(
          #GENERATION的名字
          name="gpt3.5_talk",
          model="gpt-3.5-turbo",
          messages=[
              {"role": "user", "content": "给我讲一个关于老虎的笑话，字数在50字以内"}
          ],
          temperature=0,
          trace_id=trace.id,
        )

        print(completion.choices[0].message.content)


if __name__=="__main__":
    caller=openai_langfuse("new_trace_name_1","bjdzliu","v0.0.2")
    caller.call_openai()

    








