from typing import Dict
from unittest import TestCase

import django

django.setup()

from sens_platform.api.modules.module import FactoryModule
from sens_platform.api.modules.types_modules import AverageTransducerTypes
from sens_platform.constants import AVERAGE_TRANSDUCER_TYPES


class TestModule(TestCase):
    def setUp(self) -> None:
        pass

    def test__init_with_average_transducer_types(self) -> None:
        """Verify that initialization values are not alerted."""
        name: str = AVERAGE_TRANSDUCER_TYPES
        settings: Dict = {"slug": "site"}
        factory = FactoryModule(name=name, settings=settings)
        assert factory._name == AVERAGE_TRANSDUCER_TYPES
        assert isinstance(factory._settings, Dict)
        assert factory._settings["slug"] == settings["slug"]

    def test_build_module_all_run(self) -> None:
        """Verify complete operation of the factory."""
        name: str = AVERAGE_TRANSDUCER_TYPES
        settings: Dict = {"slug": "site"}
        factory = FactoryModule(name=name, settings=settings)
        result = factory.build_module()
        assert isinstance(factory._module, AverageTransducerTypes)
        assert isinstance(result, Dict)
