import requests
import datetime as dt
import time as tm
from pprint import pprint

DELAY = 1


# Задача №1
# Нужно определить кто самый умный(intelligence) из трех супергероев- Hulk, Captain America, Thanos.
def print_the_smartest(hero_names_lst):
    url = 'https://akabab.github.io/superhero-api/api/all.json'
    headers = {'Authorization': 'secret - token - 123'}
    response = requests.get(url=url, headers=headers, timeout=DELAY)
    srv_heroes_lst = [(dict(hero)['powerstats']['intelligence'],
                       dict(hero)['name'])
                      for hero in response.json()
                      ]
    heroes_to_rate_lst = [(value, name) for value, name in srv_heroes_lst
                          if name in hero_names_lst]
    for value, name in sorted(heroes_to_rate_lst, reverse=True):
        pprint(f'The most intelligent hero is {name} with {value} of IQ.')
        return


# Задача №2
# ...принимает на вход путь до файла на компьютере и сохраняет на Яндекс.Диск с таким же именем.
class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_files_list(self):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(files_url, headers=headers)
        return response.json()

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload_file_to_disk(self, disk_file_path):
        href = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
        response = requests.put(href, data=open(disk_file_path, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")
        else:
            pprint(response.json())


# Задача №3
# ...выводит все вопросы за последние два дня и содержит тэг 'Python'.
class StackOverFlower:
    def print_questions(self, p_tag, p_days):
        url = 'https://api.stackexchange.com'\
              '/2.3/questions?order=desc&sort=activity&site=stackoverflow'
        date_from = round(tm.mktime((dt.date.today() - dt.timedelta(days=p_days - 1)).timetuple()))
        date_to = round(dt.datetime.now().timestamp())
        params = f'&tagged={p_tag}&fromdate={date_from}&todate={date_to}'
        response = dict(requests.get(url=url+params, headers='', timeout=DELAY).json())['items']
        result = ''
        for elmt in response:
            result += f'id: {elmt["question_id"]}, link: {elmt["link"]}\n'
        print(result[:-1])


if __name__ == '__main__':
    # Задача №1
    print('Задача №1:')
    print_the_smartest(['Hulk', 'Captain America', 'Thanos'])
    print('====================================================')
    # Задача №2
    print('Задача №2:')
    path_to_file = 'yad_upload.txt'
    token = 'y0_AgAAAAAAN0b6AADLWwAAAADdwB2DxDb-vB2PTxuQ0odTp2aFsl1mIV0'
    uploader = YaUploader(token)
    uploader.upload_file_to_disk(path_to_file)
    print('====================================================')
    # Задача №3
    print('Задача №3:')
    stack_over_flow = StackOverFlower()
    stack_over_flow.print_questions('Python', 2)
