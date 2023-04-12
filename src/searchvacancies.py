from src.hh import HeadHunterAPI
from src.superjob import SuperJobAPI
from src.vacancy import Vacancy
from src.json_file import JsonFile
from utl.utils import print_vacancy
from datetime import datetime


class SearchVacancies(JsonFile):
    def __init__(self, name_vacancy: str = None, salary_from=None):
        self.name_vacancy = name_vacancy    # Условие для поиска Вакансии
        self.count_vacancy = 0              # Кол-во вакансий
        self.salary_from = salary_from      # Условие для поиска от заданной ЗП
        self.__list_vacancy = []            # Список найденных вакансий
        super().__init__()
        self.current_vacancy_data = int     # Дата первой вакансии для обновления запроса

    def add_vacancy(self, **kwargs):
        """Добавление текущего запроса вакансии в файл"""
        data = {}
        self.__list_vacancy = sorted(self.__list_vacancy, key=lambda vacancy: vacancy.date_published, reverse=True)
        data[f'{self.name_vacancy} {self.salary_from}'] = [one_vacancy.__dict__ for one_vacancy in self.__list_vacancy]
        super().add_vacancy(data)
        self.__list_vacancy = []

    def sel_vacancy(self, value_vacancy):
        """Загрузить данные выбранной вакансии"""
        for dict_vacancy in super().sel_vacancy(value_vacancy):
            self.__list_vacancy.append(Vacancy(**dict_vacancy))
        self.current_vacancy_data = self.__list_vacancy[0].date_published

    def del_vacancy(self, **kwargs):
        """Удаление текущей выбранной вакансии"""
        super().del_vacancy(f'{self.name_vacancy} {self.salary_from}')
        self.__list_vacancy = []

    def list_value_vacancy(self):
        """Вывод списка архивных запросов по вакансиям"""
        if not self.archive_vacancy == {}:
            print(f"\nВаши прошлые запросы по поиску вакансии:\n{'*' * 32}")
            for number_item, param_vacancy_item in self.archive_vacancy.items():
                vacancy_item = param_vacancy_item.split(" ")
                if vacancy_item[1] == "":
                    salary_item = "ЗП не указано"
                else:
                    salary_item = f"ЗП от {vacancy_item[1]}"
                print(f"{number_item}: Запрос поиска: {vacancy_item[0]} {salary_item} "
                      f"(Найдено вакансий:{vacancy_item[2]})")
            print(f"{'*' * 32}")
        else:
            print(f"\nМеню:\n{'*' * 32}")

        print(f"9: Новый поиск")
        print(f"0: Выход")

    def menu_search(self):
        """Меню для поиска новой вакансии"""
        if len(self.archive_vacancy) < 8:
            self.name_vacancy = input("Введите поисковый запрос вакансий: ")
            # self.city = input("Введите город в котором нужно найти вакансий или нажми 'Enter' для поиска везде: ")
            self.salary_from = input("Введите ЗП от для вакансий или нажми 'Enter' если не нужно : ")
            self.find_vacancy()
            self.add_vacancy()
            super().check_file()
        else:
            print("\nПревышен лимит запросов. Не может быть больше 8 запросов. Удалите!!!\n")

    def menu_query(self, position_menu):
        """Меню действий в выбранном запросе вакансий"""
        if position_menu in self.archive_vacancy.keys():
            self.name_vacancy, self.salary_from, self.count_vacancy = self.archive_vacancy[position_menu].split(" ")
            self.sel_vacancy(f"{self.name_vacancy} {self.salary_from}")

            text_menu_query = {
                1: "Вывести все вакансии в сортированном виде по дате публикации",
                2: "Вывести ТОП N Вакансий по минимальному порогу ЗП",
                3: "Вывести вакансии по ключевому слову в описании",
                4: "Удаление запроса",
            }
            if (datetime.utcnow() - datetime.fromtimestamp(float(self.current_vacancy_data))).seconds > 3600:
                text_menu_query[5] = "Обновить вакансии по запросу(Вероятно уже есть новые)"
            [print(f"{number_item}: {query_item}") for number_item, query_item in text_menu_query.items()]
            position_menu_query = int(input("Введи номер:"))
            # position_menu_query = 2
            if position_menu_query == 1:
                print_vacancy(self.__list_vacancy)
            elif position_menu_query == 2:
                count_view = int(input("Какое кол-во ТОП запросов вывести:"))
                print_vacancy(self.sort_count_salary_min(count_view))
            elif position_menu_query == 3:
                query_word = str(input("Введите ключевые слова через пробел:")).strip().split(" ")
                print_vacancy(self.keyword_search(query_word))
            elif position_menu_query == 4:
                self.del_vacancy()
                self.check_file()
            elif position_menu_query == 5 and \
                    (datetime.utcnow() - datetime.fromtimestamp(float(self.current_vacancy_data))).seconds > 3600:
                self.__list_vacancy = []
                self.find_vacancy()
                self.add_vacancy()
                self.sel_vacancy(f'{self.name_vacancy} {self.salary_from}')
        else:
            print("\nДанного запроса нету. Повторите попытку")

    def sort_count_salary_min(self, count_view=None):
        """Сортировка ТОП по минимальному значению зарплаты с N-ым выводом"""
        return sorted(self.__list_vacancy, reverse=True)[:count_view]

    def keyword_search(self, keywords: list) -> list:
        """Поиск в текущем запросе ключевых слов"""
        result_list = []
        data_file: list = self.__list_vacancy
        for item in data_file:
            for keyword in keywords:
                if keyword.lower() in str(item.description).lower():
                    result_list.append(item)
                    break
        return result_list

    def find_vacancy(self):
        """Запуск поиска вакансий по площадкам HH и SJ"""
        sj = SuperJobAPI()
        sj.insert_vacancies(self.name_vacancy, self.salary_from, self.__list_vacancy)
        hh = HeadHunterAPI()
        hh.insert_vacancies(self.name_vacancy, self.salary_from, self.__list_vacancy)
