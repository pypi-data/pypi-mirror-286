from typing import Union

from netbox.settings import configuration
from pandas import DataFrame
from pika import BlockingConnection, ConnectionParameters, PlainCredentials, channel
from sens_platform.platforms.abc_client_platform import AbstractClientPlatform


class RabbitmqCli(AbstractClientPlatform):
    _name = "rabbitmq"
    _connection: BlockingConnection
    _channel: channel
    _queue: str
    _base_url: str
    _port: int
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
            self._base_url = configuration.RABBITMQ_CLI["RMQ2SQL_RMQ_HOST"]

        if configuration.RABBITMQ_CLI["RMQ2SQL_RMQ_PORT"] is None:
            raise Exception("Error, environment variable null: RMQ2SQL_RMQ_PORT.")
        else:
            self._port = configuration.RABBITMQ_CLI["RMQ2SQL_RMQ_PORT"]

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
        self._connect()

    def __exit__(self) -> None:
        self._channel.close()
        self._connection.close()

    def _connect(self) -> None:
        """
        Connection to influxdb.

        Returns
        -------
        Void.
        """
        self._connection = BlockingConnection(
            ConnectionParameters(
                host=self._base_url,
                port=self._port,
                virtual_host=self._vhost,
                credentials=PlainCredentials(self._user, self._password),
            )
        )
        self._channel = self._connection.channel()

    def execute_query(
        self, query: str, queue: str, durable: bool = True
    ) -> Union[DataFrame, None, bool]:
        """
        Run the queries and convert the dataset to a pandas dataFrame.

        Parameters
        ----------
        query: str
            Query rabbitMQ.
        queue: str
            Queue rabbitMQ.
        durable: bool
            Queue configuration, message duration.

        Returns
        -------
        DataFrame.
        """
        self._channel.queue_declare(queue=queue, durable=durable)
        result = self._channel.basic_publish(
            exchange="", routing_key=queue, body=b"{query}"
        )
        return result
