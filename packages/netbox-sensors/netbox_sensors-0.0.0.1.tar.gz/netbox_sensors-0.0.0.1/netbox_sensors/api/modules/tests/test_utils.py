from typing import Dict, List
from unittest import TestCase

from freezegun import freeze_time
from pandas import DataFrame, to_datetime
from sens_platform.api.modules.utils import detect_alerts, zero_data_control
from sens_platform.constants import AVERAGE_TRANSDUCER_TYPES, LAST_MEASUREMENTS

from .database_setup import setup_test_database


class TestUtils(TestCase):
    def setUp(self) -> None:
        self._db = setup_test_database()

    def test_zero_data_control(self) -> None:
        """Validation of the fake structures of the modules."""
        _fake_average_transducer_types = self._db["fake_average_transducer_types"]
        _fake_last_measurements = self._db["fake_last_measurements"]
        fake_data = zero_data_control(module=AVERAGE_TRANSDUCER_TYPES)
        assert isinstance(fake_data, Dict)
        assert _fake_average_transducer_types == fake_data

        fake_data = zero_data_control(module=LAST_MEASUREMENTS)
        assert isinstance(fake_data, List)
        assert _fake_last_measurements == fake_data

    @freeze_time("2023-09-07 12:00:00")
    def test_detect_alerts(self) -> None:
        """Verify the generation of alerts."""
        _data: DataFrame = self._db["diagnostic_alert"]
        _data["time"] = to_datetime(
            _data["time"], format="%Y-%m-%d %H:%M:%S%z", errors="coerce"
        )
        _data["type"] = _data.apply(detect_alerts, axis=1)
        result = _data["type"].value_counts().reset_index()
        result.set_index("type", inplace=True)
        assert result.at["no value", "count"] == 2
        assert result.at["non responsive", "count"] == 3
        assert result.at["does not alert", "count"] == 1
