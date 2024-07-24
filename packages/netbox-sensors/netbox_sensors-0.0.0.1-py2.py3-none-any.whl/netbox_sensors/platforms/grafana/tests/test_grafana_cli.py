from typing import Dict, List
from unittest import TestCase

from sens_platform.platforms.grafana.grafana_api import GrafanaApi
from sens_platform.platforms.grafana.grafana_cli import GrafanaCli


class TestGrafanaCli(TestCase):
    def setUp(self) -> None:
        self._user: Dict = {
            "name": "DELETE_USER",
            "email": "DELETE_USER@sens.solutioins",
            "login": "DELETE_USER",
            "password": "DELETE_USER",
        }

    def test__init(self) -> None:
        """Test the full build in Grafana."""
        cli = GrafanaCli()
        assert isinstance(cli._api, GrafanaApi)

    def test_get_organizations(self) -> None:
        """Test get orgs."""
        cli = GrafanaCli()
        result = cli.create_organization(org_name="TEST")
        org_id = result["orgId"]
        result = cli.get_organizations()
        assert isinstance(result, List)
        assert isinstance(result[0], Dict)
        _ = cli.delete_organization(org_id=org_id)

    def test_organization_exists(self) -> None:
        """Test org exists."""
        cli = GrafanaCli()
        org_name = "TEST"
        org = cli.create_organization(org_name=org_name)
        org_id = org["orgId"]
        exists = cli.organization_exists(org_name=org_name)
        assert isinstance(exists, bool)
        assert exists is True
        _ = cli.delete_organization(org_id=org_id)

    def test_organization_not_exists(self) -> None:
        """Test org not exists."""
        cli = GrafanaCli()
        org_name = "TEST_NOT_EXISTS"
        exists = cli.organization_exists(org_name=org_name)
        assert isinstance(exists, bool)
        assert exists is False

    def test_create_user(self) -> None:
        cli = GrafanaCli()
        user = cli.create_user(**self._user)
        assert isinstance(user, Dict)
        assert "message" in user
        assert user["message"] == "User created"
        cli.delete_user(user_id=user["id"])

    def test_get_users(self) -> None:
        """User list of all organizations."""
        cli = GrafanaCli()
        users = cli.get_users()
        assert isinstance(users, List)

    def test_user_exists(self) -> None:
        cli = GrafanaCli()
        user = cli.create_user(**self._user)
        exists = cli.user_exists(user_name=self._user["name"])
        assert exists is True
        cli.delete_user(user_id=user["id"])

    def test_create_user_with_org(self) -> None:
        cli = GrafanaCli()
        org = cli.create_organization(org_name="TEST")
        org_id = org["orgId"]
        data: Dict = {
            "name": "DELETE_USER",
            "email": "DELETE_USER@sens.solutioins",
            "login": "DELETE_USER",
            "password": "DELETE_USER",
            "org_id": org_id,
        }
        user = cli.create_user(**data)
        assert isinstance(user, Dict)
        assert "message" in user
        assert user["message"] == "User created"
        cli.delete_user(user_id=user["id"])
        cli.delete_organization(org_id=org_id)

    def test_create_and_delete_organization(self) -> None:
        """Test the full build in Grafana."""
        cli = GrafanaCli()
        result = cli.create_organization(org_name="TEST")
        assert isinstance(result, Dict)
        assert "orgId" in result

        result = cli.delete_organization(org_id=result["orgId"])
        assert result is True

    def test_assign_user(self) -> None:
        """Assign user to org."""
        cli = GrafanaCli()
        org = cli.create_organization(org_name="TEST")
        org_id = org["orgId"]
        user = cli.create_user(**self._user)
        user = cli.get_user(user_id=user["id"])
        result = cli.assign_user(org_id=org_id, email=user["email"])
        assert isinstance(result, Dict)
        assert result["message"] == "User added to organization"
        _ = cli.delete_user(user_id=user["id"])
        _ = cli.delete_organization(org_id=org_id)

    def test_assign_user_org_context(self) -> None:
        """Assign user org context."""
        cli = GrafanaCli()
        result = cli.create_organization(org_name="TEST")
        org_id = result["orgId"]
        result = cli.assign_user_org_context(org_id=result["orgId"])
        assert result is True
        _ = cli.assign_user_org_context(org_id=1)
        result = cli.delete_organization(org_id=org_id)
        assert result is True

    def test_create_service_account(self) -> None:
        """Create service account."""
        name_service: str = "admin_tmp"
        role = "Admin"
        cli = GrafanaCli()
        result = cli.create_organization(org_name="TEST")
        org_id = result["orgId"]
        _ = cli.assign_user_org_context(org_id=org_id)
        result = cli.create_service_account(name=name_service, role=role)
        assert result["name"] == name_service
        assert result["role"] == role
        assert result["tokens"] == 0
        _ = cli.delete_service_account(service_id=result["id"])
        _ = cli.assign_user_org_context(org_id=1)
        _ = cli.delete_organization(org_id=org_id)

    def test_create_service_account_token(self) -> None:
        """Create service account token."""
        name_service: str = "admin_tmp_5"
        role = "Admin"

        cli = GrafanaCli()
        result = cli.create_organization(org_name="TEST")
        org_id = result["orgId"]
        _ = cli.assign_user_org_context(org_id=org_id)
        result = cli.create_service_account(name=name_service, role=role)
        service_account_id = result["id"]
        token_name = f"token_{name_service}"
        result = cli.create_service_account_token(
            token_name=token_name, service_account_id=service_account_id
        )
        assert isinstance(result, Dict)
        assert result["name"] == token_name
        assert "key" in result
        _ = cli.delete_service_account(service_id=service_account_id)
        _ = cli.assign_user_org_context(org_id=1)
        _ = cli.delete_organization(org_id=org_id)

    def test_create_datasource(self) -> None:
        """Creating templated data sources."""
        cli = GrafanaCli()
        result = cli.create_organization(org_name="TEST")
        org_id = result["orgId"]
        _ = cli.assign_user_org_context(org_id=org_id)
        result = cli.create_data_sources(org_id=org_id)
        assert isinstance(result, List)
        assert len(result) == 3
        _ = cli.assign_user_org_context(org_id=1)
        _ = cli.delete_organization(org_id=org_id)

    def test_create_dashboard(self) -> None:
        """Creating templated dashboard."""
        cli = GrafanaCli()
        result = cli.create_organization(org_name="TEST")
        org_id = result["orgId"]
        _ = cli.assign_user_org_context(org_id=org_id)
        ds = cli.create_data_sources(org_id=org_id)
        result = cli.create_dash(data_sources=ds)
        pass
        _ = cli.assign_user_org_context(org_id=1)
        _ = cli.delete_organization(org_id=org_id)

    def test_full_run(self) -> None:
        """Test the full build in Grafana."""
        cli = GrafanaCli()
        org = cli.create_grafana(org_name="TEST")
        _ = cli.delete_organization(org_id=org["orgId"])
