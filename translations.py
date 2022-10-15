import json
import requests
from bs4 import BeautifulSoup
from uuid import uuid4


URL = 'https://govzalla.com/dosh/'
SUGGESTIONS = 'https://govzalla.com/dosh/api/suggestion'
TEST_ENDPOINT = 'http://localhost:8765'


def reformat_translation(translation):
    if '\n' in translation:
        translation = translation.replace('\n', '')
        return reformat_translation(translation)

    if translation.startswith(' '):
        translation = translation[1:]
        return reformat_translation(translation)

    if translation.endswith(' '):
        translation = translation[:-1]
        return reformat_translation(translation)

    if translation.endswith('.'):
        translation = translation[:-1]
        return reformat_translation(translation)

    return translation


def generate_uuid_for_key(key):
    # open new_data.json file as python dictionary
    with open('new_data_1.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    if '1' in key:
        key = key.replace('1', 'Ӏ')

    data[uuid4().hex] = {
        'term': key,
        'translation': ''
    }

    del data[key]

    # write updated data to new file
    with open('new_data_1.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_word_translation(key, suggestion):
    page = requests.get(f'{URL}translate/{suggestion["id"]}/{suggestion["term"]}')

    soup = BeautifulSoup(page.content, 'html.parser')

    translation = soup.find('p', class_=['formatted-search-result', 'font-weight-bold']).text

    translation = reformat_translation(translation)

    # open new_data.json file as python dictionary
    with open('new_data_1.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    if '1' in key:
        key = key.replace('1', 'Ӏ')

    data[uuid4().hex] = {
        'term': key,
        'translation': translation
    }

    del data[key]

    # write updated data to new file
    with open('new_data_1.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # open new_data.json file as python dictionary
    with open('new_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for key, value in data.items():
        if 'Ӏ' in key:
            key = key.replace('Ӏ', '1')

        session = requests.Session()

        suggestion = session.post(
            SUGGESTIONS,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'referer': URL,
            },
            data={'offset': key}
        )

        if suggestion.status_code == 200 and len(suggestion.json()) > 0:
            print('Suggestion found for', key)
            get_word_translation(key, suggestion.json()[0])

        else:
            print('No suggestion found for', key)
            generate_uuid_for_key(key)
