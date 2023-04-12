from src.searchvacancies import SearchVacancies


def user_interaction():
    print("Привет, я помогу тебе найти вакансию по площадкам HeadHunter и SuperJob")
    lv = SearchVacancies()
    while True:
        lv.list_value_vacancy()
        position_nam = input("Введи номер:")
        if position_nam in [str(i) for i in range(10)]:
            position_nam = int(position_nam)
        else:
            print("\nВведи цифру из списка")
            continue
        if position_nam == 0:
            break
        elif position_nam == 9:
            lv.menu_search()
            continue
        elif position_nam in range(1, 9):
            lv.menu_query(position_nam)
            continue


if __name__ == "__main__":
    user_interaction()
