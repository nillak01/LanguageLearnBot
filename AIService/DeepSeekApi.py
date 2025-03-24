from openai import OpenAI
import logging



logger = logging.getLogger(__name__)


def speak(word: str | None, api_key: str):
    logger.info(
            'Вошли в функцию speak'
        )
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    logger.info(
            'Связались с клиентом'
        )
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful language assistant"},
            {"role": "user", "content": f"Make one unique sentence with these words The sentence must be in the language of the word   Words: {word}. Just sentence"},
        ],
        stream=False
    )
    logger.info(
            'Получили ответ у функции speak'
        )

    return response.choices[0].message.content