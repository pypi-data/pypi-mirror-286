from typing import Dict
from unittest import TestCase

from sens_platform.scripts.user_generator import (
    generate_password,
    generate_username,
    new_rabbitmq_user,
)


class TestUserGenerator(TestCase):
    def setUp(self):
        super().setUp()

    def test_generate_password(self) -> None:
        """User generation validation."""
        password = generate_password()
        assert len(password) == 32
        assert password.isdigit()
        password = generate_password(level=2, password_length=21)
        assert len(password) == 21
        assert password.isalnum()
        password = generate_password(level=1, password_length=21)
        assert len(password) == 21
        assert password.isascii()

    def test_generate_username(self) -> None:
        """Validation of username generation."""
        username = generate_username(first_name="Test")
        assert isinstance(username, str)
        assert username.islower()
        assert len(username.split("_")) == 3

    def test_new_rabbitmq_user(self) -> None:
        """Validating the structure of a RabbitMQ user."""
        user_rabbitmq = new_rabbitmq_user(
            first_name="Test", level=3, password_length=32
        )
        assert isinstance(user_rabbitmq, Dict)
        assert "rabbitmq" in user_rabbitmq
        assert "user" in user_rabbitmq["rabbitmq"]
        assert "password" in user_rabbitmq["rabbitmq"]
        assert len(user_rabbitmq["rabbitmq"]["password"]) == 32
