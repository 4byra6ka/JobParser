import re
import requests
from src.jss import JobSearchService
from src.vacancy import Vacancy, ValidationVacancy
from pydantic import ValidationError
from utl.utils import srt_datetime_utf, check_salary, get_experience_vacancy


class HeadHunterAPI(JobSearchService):

    def get_vacancies(self, search):
        """ Формирование запроса на HeadHunter"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
            }
        hh_request = requests.get(url=f"https://api.hh.ru/vacancies", headers=headers, params=search)
        if hh_request.status_code != 200:
            raise NameError(f"Удаленный сервер не отвечает {hh_request.status_code}")
        return hh_request.json()

    def insert_vacancies(self, name_vacancy, salary_from, found_vacancies):
        """Обработка вакансий по параметрам с сайта SuperJob и добавления в класс SearchVacancies"""
        data_vacancies = {}
        end_page = True
        search = {"text": name_vacancy,
                  "per_page": 20,
                  }
        if salary_from is not None and salary_from != '':
            search["salary"] = salary_from
            search["only_with_salary "] = True
        search["page"] = 0
        while end_page:
            hh_vacancies = self.get_vacancies(search)
            page = hh_vacancies['page']
            if 0 != hh_vacancies['page'] <= 4:
                page += len(hh_vacancies['items'])
                search["page"] += 1
            else:
                page += len(hh_vacancies['items'])
                end_page = False
            for vacancy in hh_vacancies['items']:
                # Если загружать все 2000 страниц то HH отмечает DDoS блочит на 5 минут
                hh_vacancy = get_experience_vacancy(vacancy['url'])
                data_vacancies['site'] = "HH"
                data_vacancies['name'] = hh_vacancy['name']
                data_vacancies['city'] = hh_vacancy['area']['name']
                try:
                    data_vacancies['salary_min'] = check_salary(hh_vacancy['salary']['from'])
                    data_vacancies['salary_max'] = check_salary(hh_vacancy['salary']['to'])
                    data_vacancies['currency'] = hh_vacancy['salary']['currency'].upper()
                except TypeError:
                    data_vacancies['salary_min'] = 0
                    data_vacancies['salary_max'] = 0
                    data_vacancies['currency'] = 0
                # Возможен парсинг страницы по html тегу
                # data_vacancies['experience'] = get_experience_vacancy(vacancy['alternate_url'])
                data_vacancies['experience'] = hh_vacancy['experience']['name']
                try:
                    data_vacancies['description'] = ' '.join(
                        re.sub(r'\<[^>]*\>', ' ', hh_vacancy['description']).split())
                except TypeError:
                    data_vacancies['description'] = 'Пусто'
                data_vacancies['date_published'] = srt_datetime_utf(hh_vacancy['published_at'])
                data_vacancies['company_name'] = hh_vacancy['employer']['name']
                data_vacancies['url'] = hh_vacancy['alternate_url']
                try:
                    ValidationVacancy(**data_vacancies)
                    found_vacancies.append(Vacancy(**data_vacancies))
                except ValidationError as e:
                    print(e.errors())
                data_vacancies = {}
            print(f"Обработано {page} вакансий HeadHunter")
