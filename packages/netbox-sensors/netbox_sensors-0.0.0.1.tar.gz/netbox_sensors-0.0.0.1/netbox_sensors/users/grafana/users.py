from typing import Dict

from sens_platform.platforms.grafana import GrafanaCli
from sens_platform.utils import AdministrationEmail, generate_password_grafana

__all__ = ("ManagementUserGrafana",)


class ManagementUserGrafana:
    """
    Management user grafana:
    Created to centralize the management of Grafana users associated with Netbox.
    """

    _url_login: str = "https://graf.dev.sens.solutions/login"
    _access: Dict
    _user: Dict
    _cli: GrafanaCli

    def __init__(self, access: Dict, user: Dict):
        self._access = access
        self._user = user
        self._cli = GrafanaCli()

    def management(self):
        if self._user_exists():
            self._assign_permissions()
        else:
            self._user["password"] = self._generate_pass()
            self._cli.create_user(**self._user)
            self._assign_permissions()
            self._send_email()

    def _assign_permissions(self):
        for slug, _ in self._access.items():
            if self._cli.organization_exists(org_name=slug) is False:
                continue
            org = self._cli.get_organization(org_name=slug)
            self._cli.assign_user(org_id=org["id"], email=self._user["email"])

    def _user(self) -> Dict:
        return self._cli.get_user(user_name=self._user["name"])

    def _user_exists(self) -> bool:
        return self._cli.user_exists(user_name=self._user["name"])

    def _generate_pass(self) -> str:
        return generate_password_grafana(self._user["password"])

    def _send_email(self):
        email = AdministrationEmail(
            subject="Sens solutions, Dash user.",
            body=f"\n"
            f"User: {self._user['name']} created in Grafana.\n"
            f"Pssword: {self._user['password']}\n"
            f"Url access: {self._url_login}",
            to_email=self._user["email"],
        )
        email.send_email()
