from sens_platform.scripts.user_generator import new_rabbitmq_user

from .rabbitmq_cli import RabbitmqCli


class RabbitMQManagement:
    _cli: RabbitmqCli
    _queue: str

    def __init__(self, queue: str) -> None:
        """_."""
        self._queue = queue
        self._cli = RabbitmqCli()

    def create_user(
        self, first_name: str, level: int = None, password_length: int = None
    ):
        """

        Parameters
        ----------
        first_name: str
            First part of the username.
        level: int
            Security level.
        password_length: int
            Number of characters that the password will have.

        Returns
        -------

        """
        query: str
        user = new_rabbitmq_user(
            first_name=first_name, level=level, password_length=password_length
        )
        query = f"create_user {user['rabbitmq']['user']} {user['rabbitmq']['password']}"
        result = self._cli.execute_query(queue=self._queue, query=query)
        pass

    def assign_permissions_to_user(self):
        """_."""
        pass
