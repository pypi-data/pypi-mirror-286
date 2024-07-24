from json import loads
from typing import Dict, Union

from netbox.settings import configuration
from requests import Response, delete, get, patch, post, put
from sens_platform.platforms.abc_api_platform import AbstractApiPlatform


class ApiRest(AbstractApiPlatform):
    """
    Source: http://localhost:15672/api/index.html
    """

    _base_url: str
    _host: str
    _port: Union[int, None]
    _vhost: str
    _user: str
    _password: str

    def __init__(self) -> None:
        """
        Initialization of the configuration.
        """
        super().__init__()
        if configuration.RABBITMQ_CLI["RMQ2SQL_RMQ_HOST"] is None:
            raise Exception("Error, environment variable null: RMQ2SQL_RMQ_HOST.")
        else:
            self._host = configuration.RABBITMQ_CLI["RMQ2SQL_RMQ_HOST"]

        if configuration.RABBITMQ_CLI["RMQ2SQL_RMQ_PORT_API"] is None:
            self._port = None
        else:
            self._port = configuration.RABBITMQ_CLI["RMQ2SQL_RMQ_PORT_API"]

        if configuration.RABBITMQ_CLI["RMQ2SQL_RMQ_VHOST"] is None:
            raise Exception("Error, environment variable null: RMQ2SQL_RMQ_VHOST.")
        else:
            self._vhost = configuration.RABBITMQ_CLI["RMQ2SQL_RMQ_VHOST"]

        if configuration.RABBITMQ_CLI["RMQ2SQL_RMQ_USER"] is None:
            raise Exception("Error, environment variable null: RMQ2SQL_RMQ_USER.")
        else:
            self._user = configuration.RABBITMQ_CLI["RMQ2SQL_RMQ_USER"]

        if configuration.RABBITMQ_CLI["RMQ2SQL_RMQ_PASSWORD"] is None:
            raise Exception("Error, environment variable null: RMQ2SQL_RMQ_PASSWORD.")
        else:
            self._password = configuration.RABBITMQ_CLI["RMQ2SQL_RMQ_PASSWORD"]

        self._create_url_base()

    def _create_url_base(self) -> None:
        """
        Construction of the base url, depending on whether there is access by port
        or not

        Notes
        -----
        In the future condition for http or https.

        Returns
        -------
        Void.
        """
        if self._port:
            self._base_url = f"http://{self._host}:{self._port}/api/"
        else:
            self._base_url = f"http://{self._host}/api/"

    def get_data(self, endpoint: str, params: Dict = None) -> Dict:
        """
        Request with the get operator

        Parameters
        ----------
        endpoint: str
            _.
        params: Dict
            _.
        Returns
        -------
        Dict.
        """
        url = self._base_url + endpoint
        response = get(url, params=params, auth=(self._user, self._password))
        return loads(response.text)

    def post_data(self, endpoint: str, data: Dict = None) -> Response:
        """
        Request with the post operator

        Parameters
        ----------
        endpoint: str
            _.
        data: DIct
            _.
        Returns
        -------
        Response.
        """
        url = self._base_url + endpoint
        headers = {"Content-Type": "application/json"}
        response = post(
            url, json=data, headers=headers, auth=(self._user, self._password)
        )
        return response

    def put_data(self, endpoint: str, data: Dict = None) -> Dict:
        """
        Request with the put operator.

        Parameters
        ----------
        endpoint: str
            _.
        data: Dict
            _.

        Returns
        -------
        Dict.
        """
        url = self._base_url + endpoint
        response = put(url, json=data)
        return response.json()

    def delete_data(self, endpoint: str) -> bool:
        """
        Request with the delete operator.

        Parameters
        ----------
        endpoint: str

        Returns
        -------
        bool
        """
        url = self._base_url + endpoint
        _ = delete(url, timeout=8)
        return True

    def patch_data(self, endpoint: str) -> Response:
        """
        Request with the patch operator.

        Parameters
        ----------
        endpoint: str
            _.
        Returns
        -------
        Response.

        """
        url = self._base_url + endpoint
        response = patch(url, timeout=8)
        return response
