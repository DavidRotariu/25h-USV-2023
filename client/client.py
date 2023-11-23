import requests


class Client:
    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json'
        }

    def get(self, endpoint):
        response = requests.get(endpoint, headers=self.headers)
        success_response = self._check_response(response)
        if success_response:
            return response.json()
        return None

    def post(self, endpoint, body):
        response = requests.post(endpoint, headers=self.headers, json=body)
        success_response = self._check_response(response)
        if success_response:
            return response.json()
        return None

    def put(self, endpoint, body):
        response = requests.put(endpoint, headers=self.headers, json=body)
        success_response = self._check_response(response)
        if success_response:
            return response.json()
        return None

    @staticmethod
    def _check_response(response):
        success = response.ok
        if not success:
            print("API error message", response.content)

        return success
