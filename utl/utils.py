import requests
from datetime import datetime
from bs4 import BeautifulSoup


def check_vacancy_company(data_client: str):
    """Проверка поле названия компании"""
    try:
        return data_client['title']
    except KeyError:
        return "Без названия"


def print_vacancy(report_vacancy: list):
    """Вывод всех вакансий по запросу"""
    if not report_vacancy == []:
        for single_vacancy in report_vacancy:
            print(f'\n{"*" * 200}\n')
            print(single_vacancy)
        print(f'\n{"*" * 200}')
    else:
        print(f'\n{"*" * 200}\n\nПо запросу нет данных\n\n{"*" * 200}')


def srt_datetime_utf(date_text: str) -> int:
    """Конвертация строки в UTF"""
    date_format = datetime.strptime(date_text, "%Y-%m-%dT%H:%M:%S%z")
    return int(datetime.timestamp(date_format))


def check_salary(salary):
    """Приведение значения зарплата в нужный вид"""
    return salary if not salary is None else 0


def get_experience_vacancy_parsing(url_vacancy):
    """Парсин страницы для приведения опыт работы в нужный формат"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}
    hh_request = requests.get(url=url_vacancy, headers=headers)
    if hh_request.status_code != 200:
        raise NameError(f"Удаленный сервер не отвечает {hh_request.status_code}")
    soup = BeautifulSoup(hh_request.text, features="html.parser")
    try:
        vacancies_names = soup.find('span', {'data-qa': 'vacancy-experience'}).text.split("–")
        if len(vacancies_names) == 2:
            return f"от {vacancies_names[0]} до {vacancies_names[1]}"
        elif vacancies_names[0] == 'не требуется':
            return f"Без опыта"
        elif vacancies_names[0] == 'более 6 лет':
            return f"от {vacancies_names[0][6:]}"
    except ValueError:
        print(f"Подтвердите на сайте {url_vacancy} что не робот")
        get_experience_vacancy(url_vacancy)


def get_experience_vacancy(url_vacancy):
    """Запрос вакансии страницы для HH в json формате. При большом количестве запросов возможно блокировка по DDos"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}
    hh_request = requests.get(url=url_vacancy, headers=headers)
    if hh_request.status_code != 200:
        raise NameError(f"Удаленный сервер не отвечает {hh_request.status_code}")
    return hh_request.json()
