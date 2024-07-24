from datetime import datetime
from typing import Union

from django_pandas.io import read_frame
from pandas import DataFrame, merge
from sens_platform.constants import *
from sens_platform.models import Transducer
from sens_platform.platforms.influxdb.influxdb import InfluxManagement

from .abc_type_modules import AbstractTypeModules


class AverageData(AbstractTypeModules):
    _name: str = AVERAGE_DATA

    def __init__(
        self,
        slug: str,
        dates: Dict,
        location: str = None,
        device: str = None,
        dimension: str = None,
        time_window: str = None,
        transducer: List[str] = None,
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
                    "sensor__device__location__name",
                    "sensor__device__name",
                    "sensor__device__id",
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
                    "windows": False,
                    "group": None,
                    "drop": None,
                    "mean": False,
                    "windows-aggregate-mean": False,
                    "range": self._adapter_date(dates=self._dates),
                    "last": False,
                    "columns_dataframe": [
                        FIELDS_INFLUXDB_DEVICE_ID,
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

    def _generate_data(self) -> List[Dict]:
        transducer: Transducer
        transducers = (
            Transducer.objects.filter(
                sensor__device__site__slug=self._setting["slug"],
                **(
                    {"sensor__device__location__name": self._location}
                    if self._location
                    else {}
                ),
                **({"sensor__device__name": self._device} if self._device else {}),
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
        _influxdb = _influxdb.rename(
            columns={
                FIELDS_INFLUXDB_FIELD: ALIAS_INFLUXDB_NAME,
                FIELDS_INFLUXDB_VALUE: ALIAS_INFLUXDB_VALUE,
                FIELDS_INFLUXDB_TIME: ALIAS_INFLUXDB_TIME,
            }
        )

        _data: DataFrame
        _data = merge(_transducers, _influxdb, on=["name", "sensor_id"], how="inner")
        drop_columns = ["id", "sensor_id", "sensor__device__id", "time"]
        _data = _data.drop(columns=drop_columns)

        if self._dimension == "location":
            _data = _data.drop(columns=["device", "device_id"])
            _data = (
                _data.groupby(["name", "location"]).agg({"value": "mean"}).reset_index()
            )

        if self._dimension == "device":
            _data = _data.drop(columns=["location"])
            _data = (
                _data.groupby(["name", "device", "device_id"])
                .agg({"value": "mean"})
                .reset_index()
            )

        if self._dimension is None:
            _data = _data.drop(columns=["location", "device", "device_id"])
            _data = _data.groupby(["name"]).agg({"value": "mean"}).reset_index()

        _data = _data.reset_index(drop=True)
        return self._to_dict(_data)
