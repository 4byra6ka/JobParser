import os
import re
import requests
from src.jss import JobSearchService
from src.vacancy import Vacancy, ValidationVacancy
from pydantic import ValidationError
from utl.utils import check_vacancy_company
from datetime import datetime


class SuperJobAPI(JobSearchService):

    def get_vacancies(self, search):
        headers = {
            'X-Api-App-Id': os.getenv('SUPERJOB_API_KEY')
            }

        sj_request = requests.get(url="https://api.superjob.ru/2.0/vacancies/", headers=headers, params=search)
        if sj_request.status_code != 200:
            raise NameError(f"Удаленный сервер не отвечает {sj_request.status_code}")
        return sj_request.json() #['objects']

    def insert_vacancies(self,name_vacancy, city, salary_from, found_vacancies):
        search = {"keyword": name_vacancy,
                  "count": 100
                }
        if salary_from is not None and salary_from != '':
            search["payment_from"] = salary_from
            search["no_agreement"] = 1
        for page in range(5):
            search["page"] = page
            for vacancy in self.get_vacancies(search)['objects']:
                data_vacancies = {}
                data_vacancies['site'] = "SJ"
                data_vacancies['name'] = vacancy['profession']
                data_vacancies['city'] = vacancy['town']['title']
                data_vacancies['salary_min'] = vacancy['payment_from']
                data_vacancies['salary_max'] = vacancy['payment_to']
                data_vacancies['currency'] = vacancy['currency'].upper()
                data_vacancies['experience'] = vacancy['experience']['title']
                try:
                    data_vacancies['description'] = ' '.join(re.sub(r'\<[^>]*\>', ' ', vacancy['vacancyRichText']).split())
                except:
                    data_vacancies['description'] = 'Пусто'
                # data_vacancies['date_published'] = datetime.fromtimestamp(vacancy['date_published'])
                data_vacancies['date_published'] = vacancy['date_published']
                data_vacancies['company_name'] = check_vacancy_company(vacancy['client'])
                data_vacancies['url'] = vacancy['link']
                try:
                    ValidationVacancy(**data_vacancies)
                except ValidationError as e:
                    print(e.errors())
                found_vacancies.append(Vacancy(**data_vacancies))


