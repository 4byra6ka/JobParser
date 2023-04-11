def check_vacancy_company(data_client):
    try:
        return data_client['title']
    except KeyError:
        return "Без названия"


def print_vacancy(report_vacancy:list):
    if not report_vacancy == []:
        for single_vacancy in report_vacancy:
            print(f'\n{"*" * 200}\n')
            print(single_vacancy)
        print(f'\n{"*" * 200}')
    else:
        print(f'\n{"*" * 200}\n\nПо запросу нет данных\n\n{"*" * 200}')
