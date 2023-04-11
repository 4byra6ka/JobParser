from src.hh import HeadHunterAPI
from src.superjob import SuperJobAPI
from src.vacancy import Vacancy
from src.json_file import JsonFile
from utl.utils import print_vacancy
from datetime import datetime


class SearchVacancies(JsonFile):
    def __init__(self, name_vacancy: str = None, city: str = None, salary_from=None):
        self.name_vacancy = name_vacancy    # Условие для поиска Вакансии
        self.city = city                    # Условие для поиска по городу
        self.salary_from = salary_from      # Условие для поиска от заданной ЗП
        self.__list_vacancy = []            # Список найденных вакансий
        super().__init__()
        self.current_vacancy_data = int     # Дата первой вакансии для обновления запроса

    def add_vacancy(self):
        data = {}
        self.__list_vacancy = sorted(self.__list_vacancy, key=lambda vacancy: vacancy.date_published, reverse=True)
        data[f'{self.name_vacancy} {self.city} {self.salary_from}'] = [one_vacancy.__dict__ for one_vacancy in self.__list_vacancy]
        super().add_vacancy(data)

    def sel_vacancy(self, value_vacancy):
        for dict_vacancy in super().sel_vacancy(value_vacancy):
            self.__list_vacancy.append(Vacancy(**dict_vacancy))
        # self.сurrent_vacancy[value_vacancy] = self.__list_vacancy[0].date_published
        self.current_vacancy_data = self.__list_vacancy[0].date_published

    def del_vacancy(self):
        super().del_vacancy(f'{self.name_vacancy} {self.city} {self.salary_from}')

    def list_value_vacancy(self):
        if not self.archive_vacancy == {}:
            print(f"\nВаши запросы по поиску вакансии:\n{'*' * 32}")
            for namber_item, vacancy_item in self.archive_vacancy.items():
                print(f"{namber_item}: {vacancy_item}")
            print(f"{'*' * 32}")
        else:
            print(f"\nМеню:\n{'*' * 32}")

        print(f"9: Новый поиск")
        print(f"0: Выход")
        return True

    def menu_search(self):
        if len(self.archive_vacancy) <= 8:
            self.name_vacancy = input("Введите поисковый запрос вакансий: ")
            self.city = input("Введите город в котором нужно найти вакансий или нажми 'Enter' для поиска везде: ")
            self.salary_from = input("Введите ЗП от для вакансий или нажми 'Enter' если не нужно : ")
            self.find_vacancy()
            self.add_vacancy()
            super().check_file()
        else:
            print("\nПривышин лимит запросов. Не может быть больше 8 запросов. Удалите!!!\n")

    def menu_query(self, position_menu):
        if position_menu in self.archive_vacancy.keys():
            self.name_vacancy, self.city, self.salary_from = self.archive_vacancy[1].split(" ")
            self.sel_vacancy(self.archive_vacancy[1])
            # if (datetime.utcnow() - datetime.fromtimestamp(self.сurrent_vacancy_data)).seconds > 3600:
            #     print("\nУстарели вакансии более чем на час. Обновляю вакансии по текущему запросу.")
            #     self.find_vacancy()
            #     self.add_vacancy()
            #     self.sel_vacancy(self.archive_vacancy[1])
            text_menu_query = {
                1: "Вывести все вакансии в сортированном виде по дате публикации",
                2: "Вывести ТОП N Вакансий по минимальному порогу ЗП",
                3: "Вывести вакансии по ключевому слову в описании",
                4: "Удаление запроса",
            }
            [print(f"{namber_item}: {query_item}") for namber_item, query_item in text_menu_query.items()]
            # position_menu_query = int(input("Введи номер:"))
            position_menu_query = 2
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
        else:
            print("Данного запроса нету. Повторите попытку")

    def sort_count_salary_min(self, count_view=None):
        return sorted(self.__list_vacancy, reverse=True)[:count_view]

    def keyword_search(self, keywords: list) -> list:
        result_list = []
        data_file: list = self.__list_vacancy
        for item in data_file:
            for keyword in keywords:
                if keyword.lower() in str(item.description).lower():
                    result_list.append(item)
                    break
        return result_list

    def find_vacancy(self):
        sj = SuperJobAPI()
        sj.insert_vacancies(self.name_vacancy, self.city, self.salary_from, self.__list_vacancy)
