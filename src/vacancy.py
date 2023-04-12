from datetime import datetime
from pydantic import BaseModel


class ValidationVacancy(BaseModel):
    name: str
    city: str
    salary_min: int
    salary_max: int
    currency: str
    experience: str
    description: str
    date_published: int
    company_name: str
    url: str


class Vacancy:
    def __init__(self, site: str, name: str, city: str, salary_min: int, salary_max: int, currency: str,
                 experience: str, description: str, date_published: int, company_name: str, url: str):
        self.site = site
        self.name = name
        self.city = city
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.currency = currency
        self.experience = experience
        self.description = description
        self.date_published = date_published
        self.company_name = company_name
        self.url = url

    def __str__(self):
        """Вывод вакансии"""
        salary = ""
        if self.salary_min != 0:
            salary += f" от {self.salary_min}"
        if self.salary_max != 0:
            salary += f" до {self.salary_max}"
        return f'{datetime.fromtimestamp(self.date_published)} {self.site}: {self.name}({self.company_name}, ' \
               f'{self.city}), Опыт: {self.experience}, ЗП:{salary} {self.currency}, {self.url}\n' \
               f'Описание: {self.description[:200]}'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.site}, {self.name}, {self.city}, {self.company_name}, ' \
               f'{self.salary_min}, {self.salary_max}, {self.currency}, {self.experience}, {self.date_published}, ' \
               f'{self.url}, {self.description})'

    def __gt__(self, other):
        """Сравнение между вакансиями"""
        if not isinstance(other, Vacancy):
            raise TypeError('Аргумент должен быть типом Vacancy')
        if not other.salary_min:
            return True
        if not self.salary_min:
            return False
        return self.salary_min >= other.salary_min
