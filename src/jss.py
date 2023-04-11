from abc import ABC, abstractmethod


class JobSearchService(ABC):

    @abstractmethod
    def get_vacancies(self):
        pass


class AbstractFile(ABC):

    @abstractmethod
    def add_vacancy(self, new_data):
        pass
