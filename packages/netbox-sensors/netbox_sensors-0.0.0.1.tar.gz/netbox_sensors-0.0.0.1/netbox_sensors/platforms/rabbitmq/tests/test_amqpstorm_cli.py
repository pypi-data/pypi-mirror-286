from typing import Tuple

from sens_platform.platforms.rabbitmq.amqpstorm_cli import AmqpstormCli
from sens_platform.scripts.user_generator import new_rabbitmq_user
from vcr_unittest import VCRTestCase


class TestAmqpstormApi(VCRTestCase):
    def setUp(self):
        super().setUp()

    def test_create_user(self) -> None:
        """User creation validated."""
        user = new_rabbitmq_user(first_name="sens", level=1, password_length=12)
        cli = AmqpstormCli()
        result = cli.create_user(
            user=user["rabbitmq"]["user"],
            password=user["rabbitmq"]["password"],
            tags="administrator",
        )
        assert result is True
        _ = cli.delete_user(user["rabbitmq"]["user"])

    def test_assign_permissions_to_user(self) -> None:
        """Verified permission assignment."""
        user = new_rabbitmq_user(first_name="sens", level=1, password_length=12)
        cli = AmqpstormCli()
        result = cli.create_user(
            user=user["rabbitmq"]["user"],
            password=user["rabbitmq"]["password"],
            tags="none",
        )
        assert result is True
        levels: Tuple = ("w",)
        result = cli.assign_permissions_to_user(
            user=user["rabbitmq"]["user"],
            levels=levels,
        )
        assert result is True
        _ = cli.delete_user(user["rabbitmq"]["user"])

    def test_get_user(self) -> None:
        """Verify user data."""
        user = new_rabbitmq_user(first_name="sens", level=1, password_length=12)
        cli = AmqpstormCli()
        result = cli.create_user(
            user=user["rabbitmq"]["user"],
            password=user["rabbitmq"]["password"],
            tags="none",
        )
        assert result is True
        levels: Tuple = ("w",)
        result = cli.assign_permissions_to_user(
            user=user["rabbitmq"]["user"],
            levels=levels,
        )
        assert result is True
        result = cli.get_user(user=user["rabbitmq"]["user"])
        assert result["name"] == user["rabbitmq"]["user"]
        _ = cli.delete_user(user["rabbitmq"]["user"])

    def test_delete_user(self) -> None:
        """Verify delete user."""
        user = new_rabbitmq_user(first_name="sens", level=1, password_length=12)
        cli = AmqpstormCli()
        result = cli.create_user(
            user=user["rabbitmq"]["user"],
            password=user["rabbitmq"]["password"],
            tags="none",
        )
        assert result is True
        result = cli.get_user(user=user["rabbitmq"]["user"])
        assert result["name"] == user["rabbitmq"]["user"]
        _ = cli.delete_user(user["rabbitmq"]["user"])
        result = cli.get_user(user=user["rabbitmq"]["user"])
        assert result == (
            "Error, user not found: NOT-FOUND - "
            "The client attempted to work with a "
            "server entity that does not exist."
        )
