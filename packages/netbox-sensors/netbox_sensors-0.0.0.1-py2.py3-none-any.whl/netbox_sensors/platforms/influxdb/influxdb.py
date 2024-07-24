import logging
from typing import Dict, List, Union

from pandas import DataFrame

from .influxdb_api import ApiRest
from .influxdb_cli import InfluxdbCli


class InfluxManagement:
    """
    Class for influxdb management.
    """

    _api = Union[ApiRest, InfluxdbCli]
    _connections: Dict = {"api_rest": ApiRest, "client": InfluxdbCli}
    _endpoint_orgs: str = "orgs"
    _endpoint_buckets: str = "buckets"
    _endpoint_authorizations: str = "authorizations"
    _settings: Dict

    def __init__(self, type_connect: str = "api_rest", settings: Dict = None) -> None:
        self._settings = settings
        if type_connect == "api_rest":
            self._api = self._connections[type_connect]()
        elif type_connect == "client":
            self._api = self._connections[type_connect](org=self._settings["slug"])

    def search_site_organization(self, organization: str) -> Union[Dict, None]:
        """
        Search for a site's slug as an organization name in influxdb.

        Parameters
        ----------
        organization: str
            Site slug, used as an organization name.

        Returns
        -------
        Dict or None.
            An organization.
        """
        try:
            orgs = self._api.get_data(endpoint=self._endpoint_orgs)
            for org in orgs["orgs"]:
                if org["name"] == organization:
                    return org
        except Exception as ex:
            logging.debug(f"Error: {ex} \n Possible cause: {organization}")
        return None

    def search_bucket(self, organization: str, bucket_name: str) -> Union[Dict, None]:
        """
        Search if the bucket exists.

        Parameters
        ----------
        organization: str
            Site slug, used as an organization name.
        bucket_name: str
            Name bucket.

        Returns
        -------
        Dict or None.
            Return a bucket.
        """
        try:
            buckets = self._api.get_data(
                endpoint=self._endpoint_buckets, params={"org": organization}
            )

            for bucket in buckets["buckets"]:
                if bucket["name"] == bucket_name:
                    return bucket
        except Exception as ex:
            logging.debug(
                f"Error: {ex} \n Possible cause: {organization}/{bucket_name}."
            )
        return None

    def create_organization_in_influx(
        self, organization: str, description: str
    ) -> Dict:
        """
        Method for creating a new organization.

        Parameters
        ----------
        organization: str
            Site slug, used as an organization name.
        description: str
            Description of the organization.

        Returns
        -------
        Dict.
            Data of the organization created.

        """
        org = None
        try:
            data: Dict = {"description": description, "name": organization}
            org = self._api.post_data(endpoint=self._endpoint_orgs, data=data)
        except Exception as ex:
            logging.debug(f"Error: {ex} \n Possible cause: {organization}.")
        return org

    def delete_organization_in_influx(self, organization_id: str) -> bool:
        """
        Method to delete an organization by id.

        Parameters
        ----------
        organization_id: str
            Organization identifier.

        Returns
        -------
        Dict.
            Data of the eliminated organization.

        """
        org: bool = False
        try:
            org = self._api.delete_data(
                endpoint=f"{self._endpoint_orgs}/{organization_id}"
            )
        except Exception as ex:
            logging.debug(
                f"Error: {ex} \n Possible cause organization id: {organization_id}."
            )
        return org

    @staticmethod
    def _get_retention_rules(bucket_name) -> Dict:
        """
        Rule management by bucket name.

        Parameters
        ----------
        bucket_name: str
            Name bucket.

        Returns
        -------
        Dict.
            Returns a dict with the rule related to the bucket name.

        """
        rule = {"everySeconds": 86400, "shardGroupDurationSeconds": 0, "type": "expire"}
        if bucket_name == "status":
            rule = {
                "everySeconds": 7776000,
                "shardGroupDurationSeconds": 0,
                "type": "expire",
            }
        elif bucket_name == "data":
            rule = {"everySeconds": 0, "shardGroupDurationSeconds": 0}
        return rule

    def create_bucket_in_organization(
        self, organization_id: str, bucket_name: str
    ) -> Dict:
        """
        Create a bucket in an organization.

        Parameters
        ----------
        organization_id: str
            Organization identifier.
        bucket_name: str
            Name bucket.

        Returns
        -------
        Dict.
            _.
        """
        bucket = None
        try:
            data: Dict = {
                "description": "Generic bucket for data.",
                "name": bucket_name,
                "orgID": organization_id,
                "retentionRules": [],
                "rp": "0",
                "schemaType": "implicit",
            }
            data["retentionRules"].append(
                self._get_retention_rules(bucket_name=bucket_name)
            )
            bucket = self._api.post_data(endpoint=self._endpoint_buckets, data=data)
        except Exception as ex:
            logging.debug(
                f"Error: {ex} \n Possible cause organization id: {organization_id}."
                f"And bucket name: {bucket_name}."
            )
        return bucket

    def get_authorizations(self, organization: str = None) -> Union[List[Dict], None]:
        """
        Gets the permissions that an organization contains.

        Parameters
        ----------
        organization: str
            Name of the  organization.

        Returns
        -------
        authorizations: Union[List[Dict], None]
            _.
        """
        authorizations = None
        try:
            authorizations = self._api.get_data(
                endpoint=self._endpoint_authorizations, params={"org": organization}
            )
            authorizations = authorizations["authorizations"]
        except Exception as ex:
            logging.debug(
                f"Error: {ex} \n Possible cause organization name: {organization}."
            )
        return authorizations

    def create_an_authorization(
        self, organization_id: str, organization: str, bucket_id: str
    ) -> Dict:
        """
        Create a token with read permissions.

        Parameters
        ----------
        organization_id: str
            Organization identifier.
        organization: str
            Organization name.
        bucket_id: str
            Bucket identifier.

        Returns
        -------
        Dict.
            _.
        """
        authorization = None
        data: Dict = {
            "description": f"Authorization: {organization}",
            "orgID": organization_id,
            "permissions": [
                {"action": "read", "resource": {"type": "buckets", "id": bucket_id}}
            ],
        }
        try:
            authorization = self._api.post_data(
                endpoint=self._endpoint_authorizations, data=data
            )
        except Exception as ex:
            logging.debug(
                f"Error: {ex} \n Possible cause organization name: {organization}."
            )
        return authorization

    def delete_authorization(self, auth_id: str) -> bool:
        """
        Method to delete an authorization by id.

        Parameters
        ----------
        auth_id: str
            Authorization identifier.

        Returns
        -------
        bool.
            Data of the eliminated authorization.

        """
        result: bool = False
        try:
            _ = self._api.delete_data(
                endpoint=f"{self._endpoint_authorizations}/{auth_id}"
            )
            result = True
        except Exception as ex:
            logging.debug(f"Error: {ex} \n Possible cause authorization id: {auth_id}.")
        return result

    def query_management(self) -> DataFrame:
        """This method mounts influxdb's flux queries with the configuration it receives."""
        data: DataFrame
        query = (
            f'from(bucket: "{self._settings["bucket"]}")  '
            f'|> range({self._settings["range"]})  '
            f'|> filter(fn: (r) => r._measurement == "{self._settings["measurement"]}")  '
        )
        if self._settings["sensors"]:
            sensors: List = []
            for sensor_id in self._settings["sensors"]:
                sensors.append(f'r.sensor_id == "{sensor_id}"')
            combined_condition = " or ".join(sensors)
            query += f"|> filter(fn: (r) => {combined_condition})  "

        if self._settings["devices"]:
            devices: List = []
            for device_id in self._settings["devices"]:
                devices.append(f'r.device_id == "{device_id}"')
            combined_condition = " or ".join(devices)
            query += f"|> filter(fn: (r) => {combined_condition})  "

        if self._settings["field"]:
            fields: List = []
            for field in self._settings["field"]:
                fields.append(f'r._field == "{field}"')
            combined_condition = " or ".join(fields)
            query += f"|> filter(fn: (r) => {combined_condition})  "

        if self._settings["drop"]:
            drops: List = []
            for drop in self._settings["drop"]:
                drops.append(f'"{drop}"')
            combined_condition = ", ".join(drops)
            query += f"  |> drop(columns: [{combined_condition}])"

        if self._settings["group"]:
            groups: List = []
            for group in self._settings["group"]:
                groups.append(f'"{group}"')
            combined_condition = ", ".join(groups)
            query += f"  |> group(columns: [{combined_condition}])"

        if self._settings["windows"]:
            query += f"  |> window(every: {self._settings['windows']}m)"

        if self._settings["mean"]:
            query += f"  |> mean()"
            query += f'  |> yield (name: "mean")'

        if self._settings["windows-aggregate-mean"]:
            query += f"  |> aggregateWindow(every: {self._settings['windows-aggregate-mean']}m, fn: mean, createEmpty: false)"

        if self._settings["last"]:
            query += f"  |> last()"

        try:
            data = self._api.execute_query(query=query)
        except Exception as ex:
            print(f"INFLUX ERROR: {ex}")
        if data.empty is False:
            if self._settings["columns_dataframe"]:
                data = data[self._settings["columns_dataframe"]]
        return data
