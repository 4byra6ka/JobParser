import requests
from src.jss import JobSearchService


class HeadHunterAPI(JobSearchService):

    def api_request(self):
        # {"'User-Agent': 'HH-User-Agent'"}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
        data = {"text": "Python Developer"
                }
        hh_request = requests.get(url="https://api.hh.ru/vacancies", headers=headers, params=data)
        if hh_request.status_code != 200:
            raise NameError(f"Удаленный сервер не отвечает {hh_request.status_code}")
        return hh_request.json()


test_hh = HeadHunterAPI()
test_json = test_hh.api_request()
print(test_json)