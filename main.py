from src.searchvacancies import SearchVacancies


def user_interaction():
    print("Привет, я помогу тебе найти вакансию по площадкам HeadHunter и SuperJob")
    lv = SearchVacancies()
    while True:
        lv.list_value_vacancy()
        # position_nam = int(input("Введи номер:"))
        position_nam = 1
        if not position_nam in range(10):
            print("Введи цифру из списка")
            continue
        if position_nam == 0:
            break
        elif position_nam == 9:
            lv.menu_search()
            continue
        elif position_nam in range(1,9):
            lv.menu_query(position_nam)
            break


    # list_vacancy = FindVacancies(search_vacancy,search_city,search_zp[0],search_zp[1])
    # list_vacancy = FindVacancies(name_vacancy=search_vacancy, zp_from=search_zp[0])
    # lv = SearchVacancies(name_vacancy="Python developer", salary_from=60000)
    # lv = SearchVacancies(name_vacancy="sql")
    # lv.find_sj()
    # lv.add_vacancy()
    # lv.__str__()
    # lv.sel_vacancy("sql")
    # list_vacancy.find_sj()
    # print(list_vacancy.list_vacancy)


    # platforms = ["HeadHunter", "SuperJob"]
    # search_query = input("Введите поисковый запрос: ")
    # top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    # filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    # filtered_vacancies = filter_vacancies(hh_vacancies, superjob_vacancies, filter_words)
    #
    # if not filtered_vacancies:
    #     print("Нет вакансий, соответствующих заданным критериям.")
    #     return
    #
    # sorted_vacancies = sort_vacancies(filtered_vacancies)
    # top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    # print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()
