from datetime import datetime
from typing import Dict, Union

from sens_platform.api.modules.types_modules import (
    AllData,
    AverageData,
    AverageTransducerTypes,
    DeviceLocation,
    DeviceLocations,
    DeviceStatus,
    DiagnosticAlert,
    DynamicKPIs,
    LastMeasurements,
    PolarGraphs,
)
from sens_platform.constants import (
    ALL_DATA,
    AVERAGE_DATA,
    AVERAGE_TRANSDUCER_TYPES,
    DEVICE_LOCATION,
    DEVICE_LOCATIONS,
    DEVICE_STATUS,
    DIAGNOSTIC_ALERT,
    DYNAMIC_KPIS,
    LAST_MEASUREMENTS,
    POLAR_GRAPHS,
)


class FactoryModule:
    """
    Module factory that aims to dynamically generate the configuration of
    the modules that are painted on the dashboard.
    """

    _name: str
    _settings: Dict
    _module: Union[AverageTransducerTypes]
    _types_modules: Dict = {
        AVERAGE_TRANSDUCER_TYPES: AverageTransducerTypes,
        LAST_MEASUREMENTS: LastMeasurements,
        DIAGNOSTIC_ALERT: DiagnosticAlert,
        ALL_DATA: AllData,
        DYNAMIC_KPIS: DynamicKPIs,
        AVERAGE_DATA: AverageData,
        DEVICE_LOCATION: DeviceLocation,
        DEVICE_LOCATIONS: DeviceLocations,
        POLAR_GRAPHS: PolarGraphs,
        DEVICE_STATUS: DeviceStatus,
    }

    def __init__(self, name: str, settings: Dict) -> None:
        """
        Initializer in the module factory.

        Parameters
        ----------
        name: str
            Name of module.
        settings: Dict
            Configuration of module.
        """
        self._name = name
        self._settings = settings

    def build_module(self) -> Dict:
        """
        Dynamic module builder.

        Returns
        -------
        module_configuration: Dict
        """
        self._module = self._types_modules[self._name](**self._settings)
        _module_configuration: Dict
        _module_configuration = self._module.execute()
        return _module_configuration
