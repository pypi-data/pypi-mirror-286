from typing import Dict, List
from unittest.mock import patch

import django
from pandas import DataFrame
from sens_platform.platforms.influxdb.influxdb import InfluxManagement
from vcr_unittest import VCRTestCase

django.setup()


class TestInfluxDB(VCRTestCase):
    def setUp(self):
        super().setUp()

    def test_assert_is_instance(self) -> None:
        """Validation of the initial values of the class."""
        influx = InfluxManagement()
        self.assertIsInstance(influx, InfluxManagement)
        self.assertEqual(influx._endpoint_orgs, "orgs")
        self.assertEqual(influx._endpoint_buckets, "buckets")
        self.assertEqual(influx._endpoint_authorizations, "authorizations")

    def test_search_for_the_right_organization(self) -> None:
        """Search for the right organization."""
        influx = InfluxManagement()
        org = influx.search_site_organization(organization="cern")
        assert isinstance(org, Dict)
        assert len(org.keys()) == 6

    def test_organization_search_with_no_results(self) -> None:
        """Organization search with no results."""
        influx = InfluxManagement()
        org = influx.search_site_organization(organization="fail")
        assert org is None

    @patch("sens_platform.influxdb.influxdb.InfluxManagement._connections")
    def test_organization_search_failed(self, connect_mock) -> None:
        """Organization search failed."""
        influx = InfluxManagement()
        connect_mock.get_data.side_effect = Exception()
        org = influx.search_site_organization(organization="cern")
        assert org is None

    def test_search_for_the_right_bucket(self) -> None:
        """Search for the right bucket."""
        influx = InfluxManagement()
        bucket = influx.search_bucket(organization="cern", bucket_name="data")
        assert isinstance(bucket, Dict)
        assert len(bucket.keys()) == 11
        assert bucket["description"] == "Generic bucket for data."
        assert bucket["type"] == "user"

    def test_bucket_search_with_no_results(self) -> None:
        """Bucket search with no results."""
        influx = InfluxManagement()
        bucket = influx.search_bucket(organization="fail", bucket_name="data")
        assert bucket is None

    @patch("sens_platform.influxdb.influxdb.InfluxManagement._connections")
    def test_bucket_search_failed(self, connect_mock) -> None:
        """Bucket search failed."""
        connect_mock.get_data.side_effect = Exception()
        influx = InfluxManagement()
        bucket = influx.search_bucket(organization="fail", bucket_name="data")
        assert bucket is None

    def test_create_organization_in_influx_correctly(self) -> None:
        """Create an organization in influx correctly."""
        influx = InfluxManagement()
        org = influx.search_site_organization(organization="NewOrg")
        if org:
            _ = influx.delete_organization_in_influx(organization_id=org["id"])
        org = influx.create_organization_in_influx(
            organization="NewOrg", description="Example for tests."
        )
        _ = influx.delete_organization_in_influx(organization_id=org["id"])
        assert isinstance(org, Dict)
        assert len(org.keys()) == 6
        assert org["name"] == "NewOrg"
        assert org["description"] == "Example for tests."

    def test_create_organization_in_influx_error(self) -> None:
        """Create an organization in influx error."""
        message_influx_error = {
            "code": "conflict",
            "message": "organization with name NewOrg already exists",
        }
        influx = InfluxManagement()
        org = influx.search_site_organization(organization="NewOrg")
        if org is None:
            _ = influx.create_organization_in_influx(
                organization="NewOrg", description="Example for tests."
            )
        org = influx.create_organization_in_influx(
            organization="NewOrg", description="Example for tests."
        )
        assert isinstance(org, Dict)
        assert org == message_influx_error

    def test_delete_organizations_in_influx_correctly(self) -> None:
        """Delete an organization in influxdb correctly."""
        influx = InfluxManagement()
        org = influx.search_site_organization(organization="NewOrg")
        if org is None:
            _ = influx.create_organization_in_influx(
                organization="NewOrg", description="Example for tests."
            )
        result = influx.delete_organization_in_influx(organization_id=org["id"])
        assert result is True

    def test_delete_organizations_in_influx_error(self) -> None:
        """Delete an organization in influxdb error."""
        organization_id = "ds6f5sd65f"
        influx = InfluxManagement()
        influx._api = Exception()
        result = influx.delete_organization_in_influx(organization_id=organization_id)
        assert result is False

    def test__get_retention_rules_correctly(self) -> None:
        """Get retention rules correctly."""
        influx = InfluxManagement()
        rule = influx._get_retention_rules(bucket_name="")
        assert isinstance(rule, Dict)
        assert len(rule.keys()) == 3
        assert rule == {
            "everySeconds": 86400,
            "shardGroupDurationSeconds": 0,
            "type": "expire",
        }
        rule = influx._get_retention_rules(bucket_name="status")
        assert isinstance(rule, Dict)
        assert len(rule.keys()) == 3
        assert rule == {
            "everySeconds": 7776000,
            "shardGroupDurationSeconds": 0,
            "type": "expire",
        }
        rule = influx._get_retention_rules(bucket_name="data")
        assert isinstance(rule, Dict)
        assert len(rule.keys()) == 2
        assert rule == {"everySeconds": 0, "shardGroupDurationSeconds": 0}

    def test_create_bucket_in_organization_correctly(self) -> None:
        """Create a bucket in organization correctly."""
        influx = InfluxManagement()
        org = influx.create_organization_in_influx(
            organization="NewOrg", description="Example for tests."
        )
        result = influx.create_bucket_in_organization(
            organization_id=org["id"], bucket_name="data"
        )
        _ = influx.delete_organization_in_influx(organization_id=org["id"])
        assert isinstance(result, Dict)
        assert len(result.keys()) == 11
        assert result["name"] == "data"
        assert result["description"] == "Generic bucket for data."
        assert result["retentionRules"][0] == {
            "everySeconds": 0,
            "shardGroupDurationSeconds": 604800,
            "type": "expire",
        }

    def test_create_bucket_in_organization_error(self) -> None:
        """Create a bucket in organization with error."""
        organization_id = "65gdf64g6d"
        influx = InfluxManagement()
        influx._api = Exception()
        result = influx.create_bucket_in_organization(
            organization_id=organization_id, bucket_name="data"
        )
        assert result is None

    def test_get_and_create_authorizations_correctly(self) -> None:
        """Obtain and create authorizations."""
        influx = InfluxManagement()
        org = influx.create_organization_in_influx(
            organization="NewOrg", description="Example for tests."
        )
        bucket = influx.create_bucket_in_organization(
            organization_id=org["id"], bucket_name="data"
        )
        authorization = influx.create_an_authorization(
            organization_id=org["id"], organization=org["name"], bucket_id=bucket["id"]
        )
        result = influx.get_authorizations(organization=org["name"])
        _ = influx.delete_organization_in_influx(organization_id=org["id"])
        assert isinstance(authorization, Dict)
        assert len(authorization.keys()) == 12
        assert authorization["orgID"] == org["id"]
        assert isinstance(result, List)
        assert len(result) == 1
        assert isinstance(result[0], Dict)
        assert result[0]["description"] == "Authorization: NewOrg"
        assert isinstance(result[0]["permissions"], List)
        assert len(result[0]["permissions"]) == 1
        assert result[0]["permissions"][0]["action"] == "read"

    def test_execute_query_full_run(self) -> None:
        """Complete verification of the management of a query flux."""
        settings_query: Dict = {
            "slug": "site",
            "measurement": "environment",
            "bucket": "data",
            "sensors": [2, 3],
            "group": ["_field", "sensor_id"],
            "range": "-1h",
            "last": True,
            "columns_dataframe": ["sensor_id", "_value", "_field"],
        }
        influx = InfluxManagement(type_connect="client", settings=settings_query)
        result = influx.query_management()
        assert isinstance(result, DataFrame)
