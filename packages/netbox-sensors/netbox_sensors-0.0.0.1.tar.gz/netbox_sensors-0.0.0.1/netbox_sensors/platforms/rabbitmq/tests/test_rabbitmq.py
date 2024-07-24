from sens_platform.platforms.rabbitmq.rabbitmq import RabbitMQManagement
from sens_platform.platforms.rabbitmq.rabbitmq_cli import RabbitmqCli
from vcr_unittest import VCRTestCase


class TestRabbitmq(VCRTestCase):
    def setUp(self):
        super().setUp()

    def test__init(self) -> None:
        actions = RabbitMQManagement(queue="s3dp.DATA")
        assert actions._queue == "s3dp.DATA"
        assert isinstance(actions._cli, RabbitmqCli)
        assert actions._cli.name == "rabbitmq"

    def test_create_user(self) -> None:
        actions = RabbitMQManagement(queue="s3dp.DATA")
        pass
