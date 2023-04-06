from abc import ABC, abstractmethod


class JobSearchService(ABC):

    @abstractmethod
    def api_request(self):
        pass
