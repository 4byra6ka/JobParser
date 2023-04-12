import json
import os


class JsonFile:
    def __init__(self, name_file: str = 'vacancies.json'):
        self.name_file = name_file
        self.archive_vacancy = {}
        self.check_file()

    def check_file(self):
        """Проверка файла на существование"""
        if not os.path.exists(self.name_file):
            with open(self.name_file, 'w') as w_file:
                json.dump({}, w_file, indent=4)
        elif os.path.exists(self.name_file):
            self.archive_vacancy = {}
            self.__archive_vacancy(self.name_file, self.archive_vacancy)

    def add_vacancy(self, new_data: dict):
        """Добавление запроса вакансий из файла в формате json"""
        with open(self.name_file, 'r', encoding='utf-8') as rfile:
            text = rfile.read()
            if not text == '':
                old_data = json.loads(text)
            else:
                old_data = {}
        with open(self.name_file, 'w', encoding='utf-8') as w_file:
            json.dump(old_data | new_data, w_file, indent=2, ensure_ascii=False)

    def sel_vacancy(self, name_vacancy: str) -> list:
        """Получение архивного запроса из файла в формате json"""
        with open(self.name_file, 'r', encoding='utf-8') as rfile:
            return json.load(rfile)[name_vacancy]

    def del_vacancy(self, name_vacancy):
        """Удаление архивного запроса из файла в формате json"""
        with open(self.name_file, 'r', encoding='utf-8') as rfile:
            json_data: dict = json.load(rfile)
        del json_data[name_vacancy]
        with open(self.name_file, 'w', encoding='utf-8') as w_file:
            json.dump(json_data, w_file, indent=2, ensure_ascii=False)

    @staticmethod
    def __archive_vacancy(name_file, arch_vacancy):
        """Получение списка вакансий в архиве"""
        position = 0
        with open(name_file, 'r', encoding='utf-8') as rfile:
            text = rfile.read()
            if not text == '':
                json_data = json.loads(text)
                for i in json_data:
                    position += 1
                    arch_vacancy[position] = f"{i} {len(json_data[i])}"
            else:
                arch_vacancy = {}
