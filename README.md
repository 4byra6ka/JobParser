# <img src="https://notion-emojis.s3-us-west-2.amazonaws.com/prod/svg-twitter/1f99a.svg" width="89"/>

## Проект “Парсер вакансий”

#### Проект парсер по API с площадок вакансий HeadHunter и SuperJob и сохранение его в файл JSON.
***
#### Реализованы операции:
* Вывод всего списка вакансий
* Вывод ТОП N вакансий по минимальному порогу ЗП
* Вывод вакансии по ключевому слову из описания
* Обновление, удаления архивных запросов по вакансиям

***
Прежде чем начать использовать проект по API от SuperJob, необходимо [зарегистрироваться](https://api.superjob.ru/register) и получить `Secret key` для работы
***
### Разворачивание проекта “Парсер вакансий”
    git cline https://github.com/4byra6ka/JobParser.git
    cd JobParser
    poetry install
    set SUPERJOB_API_KEY="<Secret key>"
    poetry run main.py
