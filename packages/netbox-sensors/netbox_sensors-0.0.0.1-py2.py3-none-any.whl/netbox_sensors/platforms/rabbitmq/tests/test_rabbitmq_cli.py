from sens_platform.platforms.rabbitmq.rabbitmq_cli import RabbitmqCli
from vcr_unittest import VCRTestCase


class TestRabbitmqCli(VCRTestCase):
    def setUp(self):
        super().setUp()

    def test__init(self) -> None:
        """Validation of class initialization."""
        cli = RabbitmqCli()
        assert cli._connection.is_open is True
        assert cli._connection.is_closed is False

    def test__exit(self) -> None:
        """Validation of the class exit."""
        cli = RabbitmqCli()
        cli.__exit__()
        assert cli._connection.is_open is False
        assert cli._connection.is_closed is True

    def test__connect(self) -> None:
        """Connection validation."""
        cli = RabbitmqCli()
        assert cli._connection.is_open is True
        assert cli._connection.is_closed is False
        assert cli._channel.is_open is True
        assert cli._channel.is_closed is False

    def test_execute_query(self) -> None:
        """Query execution validation."""
        query: str = "Hello world."
        cli = RabbitmqCli()
        result = cli.execute_query(query=query, queue="s3dp.DATA")
