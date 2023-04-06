import os
import requests
from src.jss import JobSearchService


class SuperJobAPI(JobSearchService):

    def api_request(self):
        # {"'User-Agent': 'HH-User-Agent'"}
        headers = {
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            'X-Api-App-Id': os.getenv('SUPERJOB_API_KEY')
            }
        data = {"keyword": "Python Developer"
                }
        sj_request = requests.get(url="https://api.superjob.ru/2.0/vacancies/", headers=headers, params=data)
        if sj_request.status_code != 200:
            raise NameError(f"Удаленный сервер не отвечает {sj_request.status_code}")
        return sj_request.json()


test_sj = SuperJobAPI()
test_json = test_sj.api_request()
print(test_json)
