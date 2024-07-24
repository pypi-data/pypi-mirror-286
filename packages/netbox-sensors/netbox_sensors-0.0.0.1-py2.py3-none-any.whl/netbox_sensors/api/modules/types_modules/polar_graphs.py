from collections import defaultdict
from typing import Any, Union

from django_pandas.io import read_frame
from pandas import DataFrame, merge
from sens_platform.api.modules.utils import zero_data_control
from sens_platform.constants import *
from sens_platform.models import Transducer
from sens_platform.platforms.influxdb.influxdb import InfluxManagement

from .abc_type_modules import AbstractTypeModules

__all__ = ("PolarGraphs",)


class PolarGraphs(AbstractTypeModules):
    _name: str = POLAR_GRAPHS

    def __init__(
        self,
        slug: str,
        dates: Dict,
        location: str = None,
        device: List[str] = None,
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

    def execute(self) -> List[Dict]:
        self._generate_settings()
        return self._generate_data()

    def _generate_settings(self) -> None:
        self._setting = {
            "slug": self._slug,
            "postgres": {
                "model": Transducer,
                "columns_init": [
                    "id",
                    "name",
                    "sensor__id",
                    "sensor__device__name",
                    "sensor__device__id",
                    "sensor__name",
                ],
            },
            "influxdb": {
                "settings_query": {
                    "slug": self._slug,
                    "measurement": "environment",
                    "bucket": "data",
                    "sensors": None,
                    "devices": None,
                    "field": self._transducer,
                    "group": None,
                    "drop": ["_start", "_stop"],
                    "windows": False,
                    "mean": False,
                    "windows-aggregate-mean": False,
                    "range": self._adapter_date(dates=self._dates),
                    "last": True,
                    "columns_dataframe": [
                        FIELDS_INFLUXDB_SENSOR_ID,
                        FIELDS_INFLUXDB_VALUE,
                        FIELDS_INFLUXDB_FIELD,
                        FIELDS_INFLUXDB_TIME,
                    ],
                }
            },
        }

    @staticmethod
    def _to_dict(data: DataFrame) -> Union[List[Dict], Dict]:
        return data.to_dict(orient="records")

    @staticmethod
    def _transform_data(data_list):
        # Agrupar los datos por el nombre del sensor
        grouped_data = defaultdict(list)
        for item in data_list:
            grouped_data[item["name"]].append(item)

        # Transformar cada grupo en el formato deseado
        transformed_data = {"measurements": []}
        for sensor_name, group in grouped_data.items():
            r_values = [item["value"] for item in group]
            theta_values = [item["device"] for item in group]
            transformed_data["measurements"].append(
                {
                    "fill": "toself",
                    "name": TRANSDUCER_ALIAS[sensor_name],
                    "r": r_values,
                    "theta": theta_values,
                    "type": "scatterpolar",
                }
            )

        return transformed_data

    def _generate_data(
        self,
    ) -> dict | list[dict] | dict[Any, list[dict[str, list[Any] | str | Any]]]:
        transducer: Transducer
        transducers = (
            Transducer.objects.filter(
                **({"sensor__device__name__in": self._device} if self._device else {}),
                **({"name__in": self._transducer} if self._transducer else {}),
                sensor__device__site__slug=self._setting["slug"],
                **(
                    {"sensor__device__location__name": self._location}
                    if self._location
                    else {}
                ),
            )
            .select_related("type")
            .select_related("sensor")
        )

        _transducers: DataFrame
        _transducers = read_frame(
            transducers,
            fieldnames=self._setting["postgres"]["columns_init"],
            verbose=False,
        )
        _transducers = _transducers.astype(str)
        _transducers = _transducers.rename(
            columns={
                "sensor__device__location__name": ALIAS_LOCATION,
                "sensor__id": ALIAS_SENSOR_ID,
                "sensor__name": ALIAS_SENSOR_NAME,
                "sensor__device__name": ALIAS_DEVICE_NAME,
            }
        )

        if self._device is not None or self._location is not None:
            self._setting["influxdb"]["settings_query"]["devices"] = list(
                set(_transducers["sensor__device__id"])
            )

        influx_management = InfluxManagement(
            type_connect="client", settings=self._setting["influxdb"]["settings_query"]
        )
        _influxdb: DataFrame
        _influxdb = influx_management.query_management()
        if _influxdb.empty:
            return zero_data_control(module=POLAR_GRAPHS)
        _influxdb = _influxdb.rename(
            columns={
                FIELDS_INFLUXDB_FIELD: ALIAS_INFLUXDB_NAME,
                FIELDS_INFLUXDB_VALUE: ALIAS_INFLUXDB_VALUE,
                FIELDS_INFLUXDB_TIME: ALIAS_INFLUXDB_TIME,
            }
        )

        indices_a_eliminar = _influxdb[_influxdb["sensor_id"] == "9999"].index
        _influxdb = _influxdb.drop(indices_a_eliminar)

        _data: DataFrame
        _data = merge(_transducers, _influxdb, on=["name", "sensor_id"], how="inner")
        drop_columns = ["id"]
        _data = _data.drop(columns=drop_columns)
        _data = _data.reset_index(drop=True)
        data_dict = self._to_dict(_data)
        return self._transform_data(data_dict)
