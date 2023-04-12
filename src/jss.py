from abc import ABC, abstractmethod


class JobSearchService(ABC):

    @abstractmethod
    def get_vacancies(self, search):
        pass

    @abstractmethod
    def insert_vacancies(self, name_vacancy, salary_from, found_vacancies):
        pass


class AbstractFile(ABC):

    @abstractmethod
    def add_vacancy(self, new_data):
        pass
