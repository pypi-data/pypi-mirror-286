from typing import Dict, Tuple, Union

from amqpstorm import management
from netbox.settings import configuration
from sens_platform.platforms.abc_client_platform import AbstractClientPlatform


class AmqpstormCli(AbstractClientPlatform):
    """
    Revisión: https://www.amqpstorm.io/management_examples/create_user.html
    """

    _name = "rabbitmq"
    _connection: management.ManagementApi
    _queue: str
    _base_url: str
    _host: str
    _port: Union[int, None]
    _vhost: str
    _user: str
    _password: str

    def __init__(self):
        """
        Initialization of the configuration.
        """
        if configuration.RABBITMQ_CLI["RMQ2SQL_RMQ_HOST"] is None:
            raise Exception("Error, environment variable null: RMQ2SQL_RMQ_HOST.")
        else:
            self._host = configuration.RABBITMQ_CLI["RMQ2SQL_RMQ_HOST"]

        if configuration.RABBITMQ_CLI["RMQ2SQL_RMQ_PORT_API"] is None:
            raise Exception("Error, environment variable null: RMQ2SQL_RMQ_PORT_API.")
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

        super().__init__()
        self._create_url_base()
        self._connect()

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
            self._base_url = f"http://{self._host}:{self._port}"
        else:
            self._base_url = f"http://{self._host}"

    def _connect(self) -> Union[None, str]:
        """
        Connection to influxdb.

        Returns
        -------
        Void or str.
        """
        try:
            self._connection = management.ManagementApi(
                api_url=self._base_url,
                username=self._user,
                password=self._password,
                verify=True,
            )
        except management.ApiConnectionError as why:
            return f"Connection Error: {why}"

    def execute_query(self, query: str, queue: str, durable: bool = True) -> None:
        """."""
        raise NotImplementedError("`execute_query` function not implemented.")

    def create_user(
        self, user: str, password: str, tags: str = None
    ) -> Union[bool, str]:
        """
        Method to create user.

        Parameters
        ----------
        user: str
            Username.
        password: str
            User password.
        tags: str
            Grants different roles and permissions to users.

        Returns
        -------
        bool or str
        """
        try:
            self._connection.user.create(username=user, password=password, tags=tags)
            return True
        except management.ApiError as why:
            return f"Failed to create user: {why}"

    def assign_permissions_to_user(self, user: str, levels: Tuple) -> Union[bool, str]:
        """
        Assign permissions to user.

        Parameters
        ----------
        user: str
            Username.
        levels: Tuple
            Permission level for user.

        Notes
        -----
        A user's permissions can be for the "levels" parameter:
        - w: writing
        - a: reading
        - c: configuration

        Returns
        -------
        str or bool.
        """
        try:
            self._connection.user.set_permission(
                username=user,
                virtual_host=self._vhost,
                configure_regex=".*" if "c" in levels else "",
                write_regex=".*" if "w" in levels else "",
                read_regex=".*" if "r" in levels else "",
            )
            return True
        except Exception as ex:
            return f"Error: {ex}"
        pass

    def get_user(self, user: str) -> Union[Dict, str]:
        """
        Get user.

        Parameters
        ----------
        user: str
            Username.

        Returns
        -------
        Dict or str.
        """
        try:
            return self._connection.user.get(user)
        except management.ApiError as why:
            if why.error_code == 404:
                return f"Error, user not found: {why}"
        except Exception as ex:
            return f"Error (delete user): {ex}"

    def delete_user(self, user: str) -> Union[None, bool, str]:
        """
        Delete user.

        Parameters
        ----------
        user: str
            Username.
        Returns
        -------
        None or bool or str.
        """
        try:
            self._connection.user.delete(user)
        except management.ApiError as why:
            if why.error_code == 404:
                return f"Error, user not found: {why}"
        except Exception as ex:
            return f"Error (delete user): {ex}"
