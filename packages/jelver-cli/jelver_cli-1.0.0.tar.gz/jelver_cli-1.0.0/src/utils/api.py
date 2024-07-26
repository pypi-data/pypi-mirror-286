import requests
from utils.jelver_exceptions import JelverAPIException
from utils.jelver_exceptions import JelverCasesException

class Api:
    def __init__(self, api_key):
        self.host_url = 'https://api.jelver.com'
        # self.host_url = 'https://api.skyronix.link'
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        if not self.api_key:
            raise JelverAPIException('API Key is required to run the tests')

    def validate_response(self, response):
        if response.status_code != 200:
            raise JelverAPIException('Your API Key is invalid. Please provide a valid API Key to run')

    def start_test(self, url, username, password):    
        response = requests.post(
            f'{self.host_url}/start_testing_job',
            json={
                'url': url,
                'username': username,
                'password': password
            },
            headers=self.headers)
        self.validate_response(response)
        return response.json()

    def get_status(self, job_id):
        response = requests.get(
            f'{self.host_url}/testing_job_status?jobId={job_id}',
            headers=self.headers)
        self.validate_response(response)
        return response.json()

    def list_cases(self):
        response = requests.get(
            f'{self.host_url}/list_cases',
            headers=self.headers)
        self.validate_response(response)
        result = response.json()
        if len(result['testingCases']) == 0 and len(result['excludedCases']) == 0:
            raise JelverAPIException('We have not found any test cases for your account, please make sure you are properly integrated with Jelver')
        return result

    def add_case(self, case_ids):
        result = self.list_cases()
        available_cases_ids = [case['caseId'] for case in result['excludedCases']]
        if not set(case_ids).issubset(set(available_cases_ids)):
            raise JelverCasesException('The case ids provided are not part of your list of excluded cases.')
        response = requests.post(
            f'{self.host_url}/include_cases',
            json={
                'cases': case_ids
            },
            headers=self.headers)
        self.validate_response(response)
        return True 


    def remove_case(self, case_ids):
        result = self.list_cases()
        available_cases_ids = [case['caseId'] for case in result['testingCases']]
        if not set(case_ids).issubset(set(available_cases_ids)):
            raise JelverCasesException('The case ids provided are not part of your list of included cases')
        response = requests.post(
            f'{self.host_url}/exclude_cases',
            json={
                'cases': case_ids
            },
            headers=self.headers)
        self.validate_response(response)
        return True
