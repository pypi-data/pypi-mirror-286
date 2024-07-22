import requests
import typer
from rich import print


class BaseRequestWrapper:
    base_url = None
    bearer_token = None

    def __init__(self, base_url, bearer_token=None):    
        self.base_url = base_url + "/api/v1"
        self.bearer_token = bearer_token

    def set_bearer_token(self, bearer_token):
        self.bearer_token = bearer_token

    def get(self, endpoint, params=None):
        url = self.base_url + endpoint
        if self.bearer_token is not None:
            headers = {"Authorization": f"Bearer {self.bearer_token}"}
        else:
            headers = {}
        response = requests.get(url, headers=headers, params=params)
        return response.json(), response.status_code

    def post(self, endpoint, data=None):
        url = self.base_url + endpoint
        if self.bearer_token is not None:
            headers = {"Authorization": f"Bearer {self.bearer_token}"}
        else:
            headers = {}
        response = requests.post(url, headers=headers, json=data)
        return response.json(), response.status_code

    def patch(self, endpoint, data=None):
        url = self.base_url + endpoint
        if self.bearer_token is not None:
            headers = {"Authorization": f"Bearer {self.bearer_token}"}
        else:
            headers = {}
        response = requests.patch(url, headers=headers, json=data)
        return response.json(), response.status_code

    def delete(self, endpoint):
        url = self.base_url + endpoint
        if self.bearer_token is not None:
            headers = {"Authorization": f"Bearer {self.bearer_token}"}
        else:
            headers = {}
        response = requests.delete(url, headers=headers)
        return response.json(), response.status_code
