from unittest.mock import patch

import django
from pandas import DataFrame
from sens_platform.platforms.influxdb.influxdb_cli import InfluxdbCli
from vcr_unittest import VCRTestCase

django.setup()


class TestInfluxDBClient(VCRTestCase):
    def setUp(self):
        super().setUp()

    @patch(
        "sens_platform.influxdb.influxdb_cli.configuration.INFLUX_API",
        {
            "INFLUX_API_HOST": "my_host",
            "INFLUX_API_PORT": "8087",
            "INFLUX_API_VERSION": "v10",
            "INFLUX_ADMIN_TOKEN": "dsf65dsf",
        },
    )
    def test_init_success(self) -> None:
        """Initialization validation successful."""
        influx = InfluxdbCli(org="site")
        self.assertEqual(influx._org, "site")
        self.assertEqual(influx._url, "http://my_host:8087")
        self.assertEqual(influx._token, "dsf65dsf")

    @patch(
        "sens_platform.influxdb.influxdb_cli.configuration.INFLUX_API",
        {
            "INFLUX_API_HOST": None,
            "INFLUX_API_PORT": "8087",
            "INFLUX_API_VERSION": "v10",
            "INFLUX_ADMIN_TOKEN": "dsf65dsf",
        },
    )
    def test_init_missing_host(self) -> None:
        """Generate error on initialization."""
        with self.assertRaises(Exception):
            InfluxdbCli(org="site")

    @patch(
        "sens_platform.influxdb.influxdb_cli.configuration.INFLUX_API",
        {
            "INFLUX_API_HOST": "my_host",
            "INFLUX_API_PORT": None,
            "INFLUX_API_VERSION": "v10",
            "INFLUX_ADMIN_TOKEN": "dsf65dsf",
        },
    )
    def test_init_missing_port(self) -> None:
        """Generate error on initialization."""
        with self.assertRaises(Exception):
            InfluxdbCli(org="site")

    @patch(
        "sens_platform.influxdb.influxdb_cli.configuration.INFLUX_API",
        {
            "INFLUX_API_HOST": "my_host",
            "INFLUX_API_PORT": "8087",
            "INFLUX_API_VERSION": None,
            "INFLUX_ADMIN_TOKEN": "dsf65dsf",
        },
    )
    def test_init_missing_version(self) -> None:
        """Generate error on initialization."""
        with self.assertRaises(Exception):
            InfluxdbCli(org="site")

    @patch(
        "sens_platform.influxdb.influxdb_cli.configuration.INFLUX_API",
        {
            "INFLUX_API_HOST": "my_host",
            "INFLUX_API_PORT": "8087",
            "INFLUX_API_VERSION": "v10",
            "INFLUX_ADMIN_TOKEN": None,
        },
    )
    def test_init_missing_token(self) -> None:
        """Generate error on initialization."""
        with self.assertRaises(Exception):
            InfluxdbCli(org="site")

    def test_execute_query(self) -> None:
        """Verify the execution of different flux queries."""
        query = f"""
          from(bucket: "data")
            |> range(start: -1h)
            |> filter(fn: (r) => r._measurement == "environment")
            |> range(start: -1h)
            |> filter(fn: (r) => r.sensor_id == "2")
            |> group(columns: ["_field"])
            |> last()
        """
        influx = InfluxdbCli(org="site")
        result = influx.execute_query(query=query)
        assert isinstance(result, DataFrame)

        query = f"""
          from(bucket: "data")
            |> range(start: -1h)
            |> filter(fn: (r) => r._measurement == "environment")
            |> filter(fn: (r) => r.sensor_id == "2" or r.sensor_id == "3")
            |> group(columns: ["_field", "sensor_id"])
            |> last()
        """
        result = influx.execute_query(query=query)
        assert isinstance(result, DataFrame)
