from typing import List

from influxdb_client import InfluxDBClient
from netbox.settings import configuration
from pandas import DataFrame


class InfluxdbCli:
    _client: InfluxDBClient
    _token: str
    _org: str
    _url: str

    def __init__(self, org: str):
        """
        Initialization of the configuration.
        """
        if configuration.INFLUX_API["INFLUX_API_HOST"] is None:
            raise Exception("Error, environment variable null: INFLUX_API_HOST.")
        else:
            base_url = configuration.INFLUX_API["INFLUX_API_HOST"]
        if configuration.INFLUX_API["INFLUX_API_PORT"] is None:
            raise Exception("Error, environment variable null: INFLUX_API_PORT.")
        else:
            port = configuration.INFLUX_API["INFLUX_API_PORT"]
        if configuration.INFLUX_API["INFLUX_API_VERSION"] is None:
            raise Exception("Error, environment variable null: INFLUX_API_VERSION.")
        else:
            _ = configuration.INFLUX_API["INFLUX_API_VERSION"]
        if configuration.INFLUX_API["INFLUX_ADMIN_TOKEN"] is None:
            raise Exception("Error, environment variable null: INFLUX_ADMIN_TOKEN.")
        else:
            auth_token = configuration.INFLUX_API["INFLUX_ADMIN_TOKEN"]

        self._url = f"http://{base_url}:{port}"
        self._token = auth_token
        self._org = org
        self._connect()

    def _connect(self) -> None:
        """
        Connection to influxdb.

        Returns
        -------
        Void.
        """
        self._client = InfluxDBClient(url=self._url, token=self._token, org=self._org)

    def execute_query(self, query: str) -> DataFrame:
        """
        Run the queries and convert the dataset to a pandas dataFrame.

        Parameters
        ----------
        query: str
            influxdb query in Flux.

        Returns
        -------
        DataFrame.
        """
        result = self._client.query_api().query(query, org=self._org)
        records: List = []
        for table in result:
            for record in table.records:
                records.append(record.values)
        return DataFrame(records)
