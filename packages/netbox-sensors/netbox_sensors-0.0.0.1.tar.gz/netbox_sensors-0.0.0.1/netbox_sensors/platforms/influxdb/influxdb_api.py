from typing import Dict

from netbox.settings import configuration
from requests import delete, get, patch, post, put
from sens_platform.platforms.abc_api_platform import AbstractApiPlatform


class ApiRest(AbstractApiPlatform):
    def __init__(self) -> None:
        """
        Initialization of the configuration.
        """
        super().__init__()
        if configuration.INFLUX_API["INFLUX_API_HOST"] is None:
            raise Exception("Error, environment variable null: INFLUX_API_HOST.")
        else:
            base_url = configuration.INFLUX_API["INFLUX_API_HOST"]
        if configuration.INFLUX_API["INFLUX_API_PORT"] is None:
            raise Exception("Error, environment variable null: INFLUX_API_PORT.")
        else:
            port = configuration.INFLUX_API["INFLUX_API_PORT"]
        if configuration.INFLUX_API["INFLUX_API_VERSION"] is None:
            raise Exception("Error, environment variable null: INFLUX_API_VERSION.")
        else:
            version = configuration.INFLUX_API["INFLUX_API_VERSION"]
        if configuration.INFLUX_API["INFLUX_ADMIN_TOKEN"] is None:
            raise Exception("Error, environment variable null: INFLUX_ADMIN_TOKEN.")
        else:
            auth_token = configuration.INFLUX_API["INFLUX_ADMIN_TOKEN"]
        self._base_url = f"http://{base_url}:{port}/api/{version}/"
        self._auth_token = auth_token
        self._headers = {"Authorization": f"Token {self._auth_token}"}

    def get_data(self, endpoint: str, params: Dict = None) -> Dict:
        url = self._base_url + endpoint
        response = get(url, params=params, headers=self._headers)
        return response.json()

    def post_data(self, endpoint: str, data: Dict = None) -> Dict:
        url = self._base_url + endpoint
        self._headers["Content-Type"] = "application/json"
        response = post(url, json=data, headers=self._headers)
        return response.json()

    def put_data(self, endpoint: str, data: Dict = None) -> Dict:
        url = self._base_url + endpoint
        self._headers["Content-Type"] = "application/json"
        response = put(url, json=data, headers=self._headers)
        return response.json()

    def delete_data(self, endpoint: str) -> bool:
        url = self._base_url + endpoint
        _ = delete(url, headers=self._headers)
        return True

    def patch_data(self, endpoint: str) -> Dict:
        url = self._base_url + endpoint
        response = patch(url, headers=self._headers)
        return response.json()
