import requests
import os,json

FilePATH="/Users/qingliu/00-Study/AI/gradio_venv"
envfile="platform_env"
url="https://aip.baidubce.com/oauth/2.0/token"


class baidu:

    def __init__(self,envfile) -> None:
        self.ak_sk=self.__get_env(envfile)


    def __get_env(self,envfile):
        ak_sk=dict()
        with open(FilePATH+"/"+envfile,'r') as file:
            while True:
                line=file.readline()
                if not line:
                    return ak_sk
                if line.split('=')[0] == "baidu_apikey":
                    ak_sk['ak']= line.split('=')[1].rstrip()
                    
                elif line.split('=')[0] == "baidu_secret":
                    ak_sk['sk']= line.split('=')[1].rstrip()

            
    def get_token(self):
        payload = ""
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
         }
        params = {'grant_type': 'client_credentials', 
                  'client_id': self.ak_sk['ak'] , 
                  'client_secret': self.ak_sk['sk']}

        response = requests.request("POST", url, params=params, headers=headers, data=payload)
        access_token=json.loads(response.text)["access_token"]
        return access_token
    

    def chat(self,access_token,model_name,chat_content):
        url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{model_name}?access_token={access_token}"
        headers = {
        'Content-Type': 'application/json'
        }
        payload = json.dumps(chat_content)
        response = requests.request("POST", url, headers=headers, data=payload)
        return(response.text)

if __name__=="__main__":
    llmobj=baidu(envfile)
    access_token=llmobj.get_token()
    model_name='chatglm2_6b_32k'
    chat_content={
        "messages": [
            {
                "role": "user",
                "content": "今天天气不错"
            },
            {
                "role": "assistant",
                "content": "是的，我从天气预报上看适合爬山"
            },
            {
                "role": "user",
                "content": "什么时候一起去?"
            }
        ]
    }
    result=llmobj.chat(access_token,model_name,chat_content)
    print(json.loads(result)["result"])


