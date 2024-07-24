from typing import Dict

import requests
from requests.auth import HTTPBasicAuth
from sens_platform.platforms.abc_api_platform import AbstractApiPlatform


class GrafanaApi(AbstractApiPlatform):
    CANONICAL_NAME = "grafana_api"
    _name: str

    def __init__(
        self, host: str, username: str, password: str, *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self._name = self.CANONICAL_NAME
        self._host = host
        self._username = username
        self._password = password

    @property
    def name(self) -> str:
        return self._name

    def get_data(self, patch: str, params: Dict = None) -> Dict:
        url = f"{self._host}{patch}"
        response = requests.get(
            url, auth=HTTPBasicAuth(self._username, self._password), params=params
        )
        response.raise_for_status()
        return response.json()

    def post_data(self, patch: str, data: Dict) -> Dict:
        url = f"{self._host}{patch}"
        response = requests.post(
            url, auth=HTTPBasicAuth(self._username, self._password), json=data
        )
        response.raise_for_status()
        return response.json()

    def put_data(self, patch: str, data: Dict) -> Dict:
        url = f"{self._host}{patch}"
        response = requests.put(
            url, auth=HTTPBasicAuth(self._username, self._password), json=data
        )
        response.raise_for_status()
        return response.json()

    def delete_data(self, patch: str) -> bool:
        url = f"{self._host}{patch}"
        response = requests.delete(
            url, auth=HTTPBasicAuth(self._username, self._password)
        )
        response.raise_for_status()
        return response.ok

    def patch_data(self, patch: str, data: Dict) -> Dict:
        url = f"{self._host}{patch}"
        response = requests.patch(
            url, auth=HTTPBasicAuth(self._username, self._password), json=data
        )
        response.raise_for_status()
        return response.json()
