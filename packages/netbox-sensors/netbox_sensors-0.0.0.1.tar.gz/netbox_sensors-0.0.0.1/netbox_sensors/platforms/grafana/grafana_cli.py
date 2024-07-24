import logging
from typing import Dict, List, Union

from netbox.settings import configuration
from sens_platform.platforms.grafana.grafana_api import GrafanaApi
from sens_platform.platforms.grafana.templates import (
    constant_slug,
    db_base_1,
    ds_influxdb,
    ds_netbox,
    ds_postgresql,
    filter_device,
    filter_location,
    filter_measurement,
)
from sens_platform.platforms.grafana.templates.utils import (
    adapt_constant_variables,
    adapt_dashboard_with_datasources,
    adapt_dashboard_with_variables,
    adapt_filters_with_data_sources,
)

__all__ = ("GrafanaCli",)


class GrafanaCli:
    _logger: logging.Logger
    _api: GrafanaApi
    _patch: str
    _token: str
    _user: str
    _email: str
    _password: str
    _url: str

    def __init__(self):
        """
        Initialization of the configuration.
        """
        self._logger = logging.getLogger("sens_platform.platforms.grafana.grafana_cli")
        if configuration.GRAFANA_API["GRAFANA_HOST"] is None:
            raise Exception("Error, environment variable null: GRAFANA_HOST.")
        else:
            self._patch = configuration.GRAFANA_API["GRAFANA_HOST"]

        if configuration.GRAFANA_API["GRAFANA_ADMIN_USER"] is None:
            raise Exception("Error, environment variable null: GRAFANA_ADMIN_USER.")
        else:
            self._user = configuration.GRAFANA_API["GRAFANA_ADMIN_USER"]

        if configuration.GRAFANA_API["GRAFANA_ADMIN_PASSWORD"] is None:
            raise Exception("Error, environment variable null: GRAFANA_ADMIN_PASSWORD.")
        else:
            self._password = configuration.GRAFANA_API["GRAFANA_ADMIN_PASSWORD"]

        if configuration.GRAFANA_API["GRAFANA_ADMIN_EMAIL"] is None:
            raise Exception("Error, environment variable null: GRAFANA_ADMIN_EMAIL.")
        else:
            self._email = configuration.GRAFANA_API["GRAFANA_ADMIN_EMAIL"]

        self._url = f"http://{self._patch}"
        self._connect()

    def _connect(self) -> None:
        """
        Init to GrafanaAPI.

        Returns
        -------
        Void.
        """
        self._api = GrafanaApi(
            host=self._url, username=self._user, password=self._password
        )

    def create_grafana(self, org_name: str) -> Union[bool, Dict]:
        try:
            if self.organization_exists(org_name=org_name):
                return False
            org = self.create_organization(org_name=org_name)
            org_id = org["orgId"]
            _ = self.assign_user(org_id=org_id, email=self._email, role="Admin")
            _ = self.assign_user_org_context(org_id=org_id)
            ds = self.create_data_sources(org_id=org_id)
            self.create_dash(
                org_name=org_name,
                data_sources=ds,
                dashboard=db_base_1,
                filters=[filter_location, filter_device, filter_measurement],
                constants=[constant_slug],
            )
            return org
        except Exception as ex:
            self._logger.error(f"Error creating Grafana: {ex}")
            return False

    def organization_exists(self, org_name: str) -> Union[bool, None]:
        """Organization exists."""
        try:
            orgs = self.get_organizations()
            for org in orgs:
                if org["name"] == org_name:
                    return True
        except Exception as ex:
            self._logger.error(f"Error checking organization: {org_name}. {ex}")
            return None
        return False

    def get_organization(self, org_name: str) -> Union[Dict, None, bool]:
        """Get organization."""
        try:
            orgs = self.get_organizations()
            for org in orgs:
                if org["name"] == org_name:
                    return org
            return False
        except Exception as ex:
            self._logger.error(f"Error getting organization: {org_name}. {ex}")
            return None

    def get_organization_per_user(self, user_id: int):
        """
        List of organizations per User.
        GET /api/users/{user_id}/orgs HTTP/1.1
        Return: [
            {
                "orgId": 4,
                "name": "UPC-Awasuka",
                "role": "Viewer"
            }
        ]
        Returns
        -------
        Union[List, None]
        """
        try:
            result = self._api.get_data(patch=f"/api/users/{user_id}/orgs")
            if isinstance(result, List):
                return result
            return None
        except Exception as ex:
            self._logger.error(f"Error getting organization per user: {user_id}. {ex}")
            return None
        pass

    def get_organizations(self) -> Union[List, None]:
        """
        List of organizations.
        GET /api/orgs HTTP/1.1
        Return: {"id":1, "name":"Main Org."}

        Returns
        -------
        Union[Dict, None]
        """
        try:
            result = self._api.get_data(patch=f"/api/orgs")
            if isinstance(result, List):
                return result
            return None
        except Exception as ex:
            self._logger.error(f"Error getting organizations. {ex}")
            return None

    def get_user(
        self, user_id: int = None, user_name: str = None
    ) -> Union[Dict, None, bool]:
        """
        Get user.
        GET /api/users HTTP/1.1
        Return: {
            "id": 2,
            "email": "cturro@gmail.com",
            "name": "cturro",
            "login": "cturro",
            "theme": "",
            "orgId": 4,
            "isGrafanaAdmin": false,
            "isDisabled": false,
            "isExternal": false,
            "isExternallySynced": false,
            "authLabels": [],
            "updatedAt": "2024-02-29T14:24:52Z",
            "createdAt": "2024-02-29T14:24:52Z",
            "avatarUrl": "/avatar/9e4632ee3835918ca5d183c364eaa533"
        }

        Returns
        -------
        Union[Dict, None]
        """
        if user_id:
            try:
                user = self._api.get_data(patch=f"/api/users/{user_id}")
                if isinstance(user, Dict):
                    return user
                return None
            except Exception as ex:
                self._logger.error(
                    f"Error getting user: {user_id if user_id else user_name}. {ex}"
                )
                return None
        if user_name:
            try:
                users = self.get_users()
                for user in users:
                    if user["name"] == user_name:
                        return user
                return False
            except Exception as ex:
                self._logger.error(
                    f"Error getting user: {user_id if user_id else user_name}. {ex}"
                )
                return None

    def get_users(self) -> Union[List, None]:
        """
        Get user.
        GET /api/users HTTP/1.1
        Return: [{
            "id": 2,
            "email": "cturro@gmail.com",
            "name": "cturro",
            "login": "cturro",
            "theme": "",
            "orgId": 4,
            "isGrafanaAdmin": false,
            "isDisabled": false,
            "isExternal": false,
            "isExternallySynced": false,
            "authLabels": [],
            "updatedAt": "2024-02-29T14:24:52Z",
            "createdAt": "2024-02-29T14:24:52Z",
            "avatarUrl": "/avatar/9e4632ee3835918ca5d183c364eaa533"
        }]

        Returns
        -------
        Union[Dict, None]
        """
        try:
            users = self._api.get_data(patch=f"/api/users/")
            if isinstance(users, List):
                return users
            return None
        except Exception as ex:
            self._logger.error(f"Error getting users. {ex}")
            return None

    def user_exists(self, user_name: str) -> Union[bool, None]:
        """
        User exists.

        Returns
        -------
        Union[Dict, None]
        """
        try:
            users = self.get_users()
            for user in users:
                if user["name"] == user_name:
                    return True
            return False
        except Exception as ex:
            self._logger.error(f"Error checking user: {user_name}. {ex}")
            return None

    def create_user(
        self, name: str, email: str, login: str, password: str, org_id: int = None
    ) -> Union[Dict, None]:
        """
        Create user.
        GET /api/admin/users HTTP/1.1
        Return: {"id":1, "name":"Main Org."}

        Returns
        -------
        Union[Dict, None]
        """
        data: Dict = {
            "name": name,
            "email": email,
            "login": login,
            "password": password,
            **({"orgId": org_id} if org_id else {}),
        }
        try:
            user = self._api.post_data(patch=f"/api/admin/users", data=data)
            return user
        except Exception as ex:
            self._logger.error(f"Error creating user: {name}. {ex}")
            return None

    def delete_user(self, user_id: int) -> Union[bool, None]:
        """
        Delete user.
        DELETE /api/admin/users HTTP/1.1
        Return: {"name":"user deleted"}

        Returns
        -------
        Union[Dict, None]
        """
        try:
            _ = self._api.delete_data(patch=f"/api/admin/users/{user_id}")
            return True
        except Exception as ex:
            self._logger.error(f"Error deleting user: {user_id}. {ex}")
            return None

    def create_organization(self, org_name: str) -> Union[Dict, bool]:
        """
        Only works with Basic Authentication (username and password.
        POST /api/orgs HTTP/1.1
        Return: {"orgId":1, "message":"Organization created"}

        Parameters
        ----------
        org_name: str
            _.

        Returns
        -------
        Dict.
        """
        try:
            data: Dict = {"name": org_name}
            result = self._api.post_data(patch=f"/api/orgs", data=data)
            if isinstance(result, dict) and "message" in result:
                if result["message"] == "Organization created":
                    return result
            return False
        except Exception as ex:
            self._logger.error(f"Error creating organization: {org_name}. {ex}")
            return False

    def delete_organization(self, org_id: int) -> bool:
        """
        Only works with Basic Authentication (username and password)
        DELETE /api/orgs/:orgId
        Return: {"message":"Organization deleted"}

        Parameters
        ----------
        org_id: int
            _.

        Returns
        -------
        bool.
        """
        try:
            result = self._api.delete_data(patch=f"/api/orgs/{org_id}")
            if isinstance(result, dict) and "message" in result:
                if result["message"] == "Organization deleted":
                    return True
            if result:
                return True
            return False
        except Exception as ex:
            self._logger.error(f"Error deleting organization: {org_id}. {ex}")
            return False

    def assign_user(
        self, org_id: int, email: str, role: str = "Viewer"
    ) -> Union[Dict, bool]:
        """
        Assign member to organization. An existing user is associated with an
        organization, indicating the permissions.
        POST /api/orgs/7/users
        Return: {
            "message": "User added to organization",
            "userId": 1
        }

        Parameters
        ----------
        org_id: int
            _.
        email: str
            _.
        role: str
            Default Viewer, except Admin.

        Returns
        -------
        bool and Dict.
        """
        try:
            data: Dict = {
                "loginOrEmail": email,
                "role": role,
            }
            result = self._api.post_data(patch=f"/api/orgs/{org_id}/users", data=data)
            if isinstance(result, dict) and "message" in result and "userId" in result:
                return result
            return False
        except Exception as ex:
            self._logger.error(
                f"Error assigning user: {email if email else org_id}. {ex}"
            )
            return False

    def assign_user_org_context(self, org_id: int) -> Union[Dict, bool]:
        """
        Switch the org context for the Admin user to the new org.
        POST /api/user/using/<id of new org>
        Return: {'message': 'Active organization changed'}

        Parameters
        ----------
        org_id: int
            _.

        Returns
        -------
        bool and Dict.
        """
        try:
            result = self._api.post_data(patch=f"/api/user/using/{org_id}", data={})
            if isinstance(result, dict) and "message" in result:
                if result["message"] == "Active organization changed":
                    return True
            return False
        except Exception as ex:
            self._logger.error(f"Error assigning user org context: {org_id}. {ex}")
            return False

    def delete_service_account(self, service_id: int) -> bool:
        """
        DELETE /api/serviceaccounts/:id
        Return: {"message": "Service account deleted"}

        Returns
        -------
        bool
        """
        try:
            result = self._api.delete_data(patch=f"/api/serviceaccounts/{service_id}")
            if result:
                return True
            return False
        except Exception as ex:
            self._logger.error(f"Error deleting service account: {service_id}. {ex}")
            return False

    def create_service_account(self, name: str, role: str = "Admin") -> Dict:
        """
        Required permissions.
        POST /api/serviceaccounts HTTP/1.1
        Accept: application/json
        Content-Type: application/json
        Authorization: Basic YWRtaW46YWRtaW4=
        Return: {
            "id": 1,
            "name": "test",
            "login": "sa-test",
            "orgId": 1,
            "isDisabled": false,
            "createdAt": "2022-03-21T14:35:33Z",
            "updatedAt": "2022-03-21T14:35:33Z",
            "avatarUrl": "/avatar/8ea890a677d6a223c591a1beea6ea9d2",
            "role": "Viewer",
            "teams": []
        }

        Parameters
        ----------
        name: str
            _.
        role: str
            _.

        Returns
        -------
        Dict.
        """
        try:
            data: Dict = {"name": name, "role": role}
            result = self._api.post_data(patch=f"/api/serviceaccounts", data=data)
            return result
        except Exception as ex:
            self._logger.error(f"Error creating service account: {name}. {ex}")
            return False

    def create_service_account_token(
        self, token_name: str, service_account_id: int
    ) -> Union[Dict, bool]:
        """
        Create a Service Account token for the service account.
        POST /api/serviceaccounts/<service account id>/tokens

        Parameters
        ----------
        name: str
            _.
        role: str
            _.

        Returns
        -------
        bool or Dict
        """
        try:
            data: Dict = {"name": token_name}
            result = self._api.post_data(
                patch=f"/api/serviceaccounts/{service_account_id}/tokens", data=data
            )
            return result
        except Exception as ex:
            self._logger.error(
                f"Error creating service account token: {token_name}. {ex}"
            )
            return False

    def create_data_sources(self, org_id: int) -> Union[List, bool]:
        """
        Creation of datasource based on template.
        POST /api/datasources

        Parameters
        ----------
        org_id: int
            _.

        Returns
        -------
        bool or Dict
        """
        try:
            result: List = []
            for tmp in [ds_postgresql, ds_netbox, ds_influxdb]:
                tmp["orgId"] = org_id
                result.append(self._api.post_data(patch=f"/api/datasources/", data=tmp))
            return result
        except Exception as ex:
            self._logger.error(f"Error creating data sources: {ex}")
            return False

    def create_dash(
        self,
        org_name: str,
        data_sources: List,
        dashboard: Dict,
        filters: List,
        constants: List,
    ) -> Union[Dict, bool]:
        """
        Create a dash.
        POST /api/dashboards/db

        Parameters
        ----------
        org_name: str
            _.
        data_sources: List
            _.
        dashboard: Dict
            _.
        filters: List
            _.
        constants: List
            _.

        Returns
        -------
        bool or Dict
        """
        try:
            dashboard = adapt_dashboard_with_datasources(
                dash=dashboard, datasources=data_sources
            )
            constants = adapt_constant_variables(
                constants=constants, adapt={"ORGNAME": org_name}
            )
            filters = adapt_filters_with_data_sources(
                filters=filters, data_sources=data_sources
            )
            dashboard = adapt_dashboard_with_variables(
                dash=dashboard, variables=constants + filters
            )
            result = self._api.post_data(patch=f"/api/dashboards/db", data=dashboard)
            return result
        except Exception as ex:
            self._logger.error(f"Error creating dash: {ex}")
            return False
