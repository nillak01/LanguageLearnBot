from bs4 import BeautifulSoup
import requests


def get_word_definition_from_html(word: str):
    """Получение определения слова через парсинг HTML"""

    url = f"https://www.larousse.fr/dictionnaires/francais/{word}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Извлечение данных (селекторы нужно уточнить через анализ HTML)
        definition_data = {}

        # Пример селекторов (нужно проверить в браузере)
        title = soup.find('h1')
        if title:
            definition_data['title'] = title.get_text().strip()

        # Определения
        definitions = soup.select('.Definitions .DivisionDefinition')
        definition_data['definitions'] = []

        for def_element in definitions[:5]:  # Первые 5 определений
            definition_text = def_element.get_text().strip()
            if definition_text:
                definition_data['definitions'].append(definition_text)

        # Примеры использования
        examples = soup.select('.Exemple')
        definition_data['examples'] = [ex.get_text().strip() for ex in examples[:3]]

        return definition_data

    except requests.exceptions.RequestException as e:
        return {'error': f'Request error: {e}'}
    except Exception as e:
        return {'error': f'Parsing error: {e}'}

# Тестирование
# result = get_word_definition_from_html("hourse")
# print(json.dumps(result, indent=2, ensure_ascii=False))