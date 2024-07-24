from typing import Dict, List
from unittest import TestCase

import django
from pandas import DataFrame

django.setup()

from database_setup import setup_test_database, setup_test_database_influxdb
from sens_platform.api.modules.types_modules import DiagnosticAlert
from sens_platform.constants import DIAGNOSTIC_ALERT


class TestDiagnosticAlert(TestCase):
    def setUp(self) -> None:
        self._db_influxdb = setup_test_database_influxdb()
        self._db = setup_test_database()
        self._slug: str = "site"

    def test__init_(self) -> None:
        """Verify initialization."""
        diagnostic = DiagnosticAlert(self._slug)
        assert diagnostic.name == DIAGNOSTIC_ALERT
        assert diagnostic._slug == self._slug

    def test__to_dict(self) -> None:
        """_."""
        diagnostic = DiagnosticAlert(self._slug)
        result = diagnostic._to_dict(alerts=DataFrame(self._db["diagnostic_alert"]))
        assert isinstance(result, Dict)
        assert "incidents" in result
        assert "incident_map" in result
        assert "incident_types" in result
        assert isinstance(result["incidents"], List)
        assert isinstance(result["incident_map"], Dict)
        assert isinstance(result["incident_types"], List)
        assert "no value" in result["incident_map"]
        assert "non responsive" in result["incident_map"]
        assert "does not alert" in result["incident_map"]

    def test_execute_all_run(self) -> None:
        """Verify the entire execution."""
        diagnostic = DiagnosticAlert(self._slug)
        result = diagnostic.execute()
