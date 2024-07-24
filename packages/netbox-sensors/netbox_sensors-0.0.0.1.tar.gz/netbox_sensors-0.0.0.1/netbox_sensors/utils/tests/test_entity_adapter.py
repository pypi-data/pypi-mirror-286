from typing import Dict
from unittest import TestCase

from sens_platform.constants import ENTITIES, SENSOR_TYPE_UNIFICATION
from sens_platform.utils.entity_adapter import EntityAdapter


class TestEntityAdapter(TestCase):
    def setUp(self) -> None:
        self._sensor_type_data: Dict = {"Name": "ST-1"}
        pass

    def test__init(self) -> None:
        """Check init."""
        adapter = EntityAdapter(
            entity_name=ENTITIES.SENSOR_TYPE, data=self._sensor_type_data
        )
        assert adapter._entity_name == ENTITIES.SENSOR_TYPE
        assert adapter._entity_guide[adapter._entity_name] == SENSOR_TYPE_UNIFICATION

    def test_full_run(self) -> None:
        """Check complete operation."""
        adapter = EntityAdapter(
            entity_name=ENTITIES.SENSOR_TYPE, data=self._sensor_type_data
        )
        result = adapter.transformation()
        assert isinstance(result, Dict)
        assert result == {"name": "ST-1"}
