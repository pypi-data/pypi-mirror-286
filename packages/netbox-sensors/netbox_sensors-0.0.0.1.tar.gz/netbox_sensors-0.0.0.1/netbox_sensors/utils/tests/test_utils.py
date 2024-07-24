from unittest import TestCase

import django

django.setup()

from sens_platform.utils.utils import generate_password_grafana


class TestUtils(TestCase):
    def setUp(self) -> None:
        pass

    def test_generate_password_grafana(self) -> None:
        origin_password: str = (
            "pbkdf2_sha256$600000$8X9lZUnxklgvOlLdn7RbOn$ZPjcSWn"
            "O0XTiHPPEGE3PCtPhqAE5o+tw+FyJi7PZIRQ="
        )
        pass1: str
        pass2: str
        pass1 = generate_password_grafana(input_string=origin_password)
        pass2 = generate_password_grafana(input_string=origin_password)
        assert pass1 == pass2
