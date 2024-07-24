from typing import Dict, List

from requests import Response
from sens_platform.platforms.rabbitmq.rabbitmq_api import ApiRest
from vcr_unittest import VCRTestCase


class TestApiRest(VCRTestCase):
    def setUp(self):
        super().setUp()

    def test__init(self) -> None:
        """Verification of class initialization."""
        api = ApiRest()
        assert api.CANONICAL_NAME == "abstract_api_platform"
        assert api._vhost == "s3dp"
        assert api._base_url == f"http://{api._host}/api/"

    def test__create_url_base(self) -> None:
        """Verification of url creation."""
        api = ApiRest()
        assert api._base_url == "http://localhost:5672/api/"

    def test_get_data(self) -> None:
        """Get operator verification."""
        endpoint = "users/"
        api = ApiRest()
        result = api.get_data(endpoint=endpoint)
        assert isinstance(result, List)
        assert isinstance(result[0], Dict)

    def test_post_data(self) -> None:
        """Post operator verification."""
        endpoint = "rebalance/queues"
        api = ApiRest()
        result = api.post_data(endpoint=endpoint)
        assert isinstance(result, Response)

    def test_put_data(self) -> None:
        """Put operator verification."""
        pass

    def test_delete_data(self) -> None:
        """Delete operator verification."""
        pass

    def test_patch_data(self) -> None:
        """Patch operator verification."""
        pass
