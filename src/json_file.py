import json
import os
from src.jss import AbstractFile

class JsonFile(AbstractFile):
    def __init__(self, name_file: str='vacancies.json'):
        self.name_file = name_file
        self.status_file = None
        self.archive_vacancy = {}
        self.check_file()

    def check_file(self):
        if not os.path.exists(self.name_file):
            with open(self.name_file, 'w') as file:
                self.status_file = 1
        elif os.path.exists(self.name_file):
            self.status_file = 1
            self.__archive_vacancy(self.name_file, self.archive_vacancy)

    def add_vacancy(self, new_data: dict):
        with open(self.name_file, 'r', encoding='utf-8') as rfile:
            text = rfile.read()
            if not text == '':
                old_data = json.loads(text)
            else:
                old_data = {}
        with open(self.name_file, 'w', encoding='utf-8') as wfile:
            json.dump(old_data | new_data, wfile, indent=2, ensure_ascii=False)

    def sel_vacancy(self, name_vacancy: str) -> list:
        with open(self.name_file, 'r', encoding='utf-8') as rfile:
            return json.load(rfile)[name_vacancy]

    def del_vacancy(self, name_vacancy):
        with open(self.name_file, 'r', encoding='utf-8') as rfile:
            json_data: dict = json.load(rfile)
        del json_data[name_vacancy]
        with open(self.name_file, 'w', encoding='utf-8') as wfile:
            json.dump(json_data, wfile, indent=2, ensure_ascii=False)
        # json_data

    @staticmethod
    def __archive_vacancy(name_file, arch_vacancy):
        position = 0
        with open(name_file, 'r', encoding='utf-8') as rfile:
            text = rfile.read()
            if not text == '':
                json_data = json.loads(text)
                for i in json_data:
                    position += 1
                    arch_vacancy[position] = i
