from typing import Dict, List

from pandas import DataFrame, merge
from sens_platform.api.modules.utils import zero_data_control
from sens_platform.constants import (
    AVERAGE_TRANSDUCER_TYPES,
    FIELDS_INFLUXDB_FIELD,
    FIELDS_INFLUXDB_SENSOR_ID,
    FIELDS_INFLUXDB_VALUE,
)
from sens_platform.models import Sensor, Transducer
from sens_platform.platforms.influxdb.influxdb import InfluxManagement

from .abc_type_modules import AbstractTypeModules


class AverageTransducerTypes(AbstractTypeModules):
    _name: str = AVERAGE_TRANSDUCER_TYPES

    def __init__(
        self,
        slug: str,
        dates: Dict,
        location: str = None,
        device: str = None,
        time_window: str = None,
        transducer: List[str] = None,
        dimension: str = None,
    ):
        super().__init__(
            slug=slug,
            dates=dates,
            location=location,
            device=device,
            time_window=time_window,
            transducer=transducer,
            dimension=dimension,
        )

    def execute(self) -> Dict:
        self._generate_settings()
        return self._generate_data()

    def _generate_settings(self) -> None:
        sensors: Sensor
        sensors = Sensor.objects.filter(device__site__slug=self._slug).values_list(
            "id", flat=True
        )
        self._setting = {
            "slug": self._slug,
            "postgres": {
                "model": Transducer,
                "columns_init": ["id", "name", "sensor_id", "unit", "icon", "type_id"],
            },
            "influxdb": {
                "settings_query": {
                    "slug": self._slug,
                    "measurement": "environment",
                    "bucket": "data",
                    "sensors": list(sensors),
                    "devices": None,
                    "field": None,
                    "windows": False,
                    "group": [FIELDS_INFLUXDB_FIELD, FIELDS_INFLUXDB_SENSOR_ID],
                    "drop": None,
                    "mean": False,
                    "windows-aggregate-mean": False,
                    "range": "-1h",
                    "last": True,
                    "columns_dataframe": [
                        FIELDS_INFLUXDB_SENSOR_ID,
                        FIELDS_INFLUXDB_VALUE,
                        FIELDS_INFLUXDB_FIELD,
                    ],
                }
            },
        }

    @staticmethod
    def _to_dict(data: DataFrame) -> Dict:
        result: Dict = {}
        for transducer_type in data.to_dict(orient="records"):
            result[transducer_type["name"]] = transducer_type
        return result

    def _generate_data(self) -> Dict:
        transducer: Transducer
        transducers = Transducer.objects.filter(
            sensor__device__site__slug=self._setting["slug"]
        ).select_related("type")

        _transducers: DataFrame
        _transducers = DataFrame(list(transducers.values()))
        _transducers = _transducers[self._setting["postgres"]["columns_init"]]
        _transducers = _transducers.astype(str)

        influx_management = InfluxManagement(
            type_connect="client", settings=self._setting["influxdb"]["settings_query"]
        )
        _influxdb: DataFrame
        _influxdb = influx_management.query_management()
        if list(_influxdb.columns) == 0:
            return zero_data_control(module=AVERAGE_TRANSDUCER_TYPES)

        _influxdb = _influxdb.rename(columns={"_field": "name"})

        _data: DataFrame
        _data = merge(_transducers, _influxdb, on=["name", "sensor_id"], how="inner")
        _data["average"] = _data.groupby(["type_id", "name"])["_value"].transform(
            "mean"
        )

        grouped = _data.groupby(["type_id", "name"]).agg({"_value": ["min", "max"]})
        grouped = grouped.reset_index()
        grouped.columns = ["type_id", "name", "minimum", "maximum"]

        _data = _data.merge(grouped, on=["type_id", "name"], how="left")

        grouped = _data.groupby(["type_id", "name"])["sensor_id"].unique().reset_index()
        grouped["sensors"] = grouped["sensor_id"].apply(list)

        _data = _data.merge(
            grouped[["type_id", "name", "sensors"]], on=["type_id", "name"], how="left"
        )

        drop_columns = ["id", "sensor_id", "_value"]
        _data = _data.drop(columns=drop_columns)
        _data = _data.drop_duplicates(subset=["type_id"])
        _data = _data.reset_index(drop=True)

        # temporal.
        _data["label_html"] = _data["name"]
        valor_relleno = "route"
        _data["route"] = _data["label_html"].fillna(valor_relleno)
        _data["unit_html"] = _data["unit"]

        return self._to_dict(data=_data)
