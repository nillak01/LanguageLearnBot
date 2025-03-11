from openai import OpenAI
from config_data.config import load_DS_config

ds = load_DS_config()

client = OpenAI(api_key=ds.api_key, base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)