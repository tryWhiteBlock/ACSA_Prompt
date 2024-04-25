import openai
import os
api_key_path="/home/su/acsa_prompt/api_key"
base_url_path="/home/su/acsa_prompt/api_base_url"
with open(api_key_path) as f:
    openai.api_key=f.read()
with open(base_url_path) as f:
    openai.base_url=f.read()
openai.default_headers = {"x-foo": "true"}
def chat(message):
    completion = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=message,
    )
    return completion.choices[0].message.content

if __name__=="__main__":
    message=[{"role":"user","content":"hello"}]
    print(chat(message))