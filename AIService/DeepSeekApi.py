from openai import OpenAI
from environs import Env
import logging


env: Env = Env()
logger = logging.getLogger(__name__)

try:
    # Добавляем в переменное окружение данные из .env
    env.read_env(path=None)
    api_key=env('DEEP_SEEK_API')

except Exception:
    logger.error("Cant read env")

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)