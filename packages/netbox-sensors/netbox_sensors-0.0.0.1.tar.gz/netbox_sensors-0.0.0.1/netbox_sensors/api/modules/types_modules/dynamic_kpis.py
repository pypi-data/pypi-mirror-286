from datetime import datetime
from typing import Union

from django_pandas.io import read_frame
from pandas import DataFrame, merge
from sens_platform.api.modules.utils import zero_data_control
from sens_platform.constants import *
from sens_platform.models import Transducer
from sens_platform.platforms.influxdb.influxdb import InfluxManagement

from .abc_type_modules import AbstractTypeModules


class DynamicKPIs(AbstractTypeModules):
    _name: str = DYNAMIC_KPIS
    _calculate: str = "average"

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

    def execute(self) -> List[Dict]:
        self._generate_settings()
        return self._generate_data()

    def _generate_settings(self) -> None:
        self._setting = {
            "slug": self._slug,
            "postgres": {
                "model": Transducer,
                "columns_init": [
                    "name",
                    "sensor__id",
                    "unit",
                    "max_warning",
                    "max_critical",
                    "min_warning",
                    "min_critical",
                ],
            },
            "influxdb": {
                "settings_query": {
                    "slug": self._slug,
                    "measurement": "environment",
                    "bucket": "data",
                    "sensors": None,
                    "devices": None,
                    "group": None,
                    "drop": None,
                    "mean": False,
                    "windows-aggregate-mean": False,
                    "windows": False,
                    "range": self._adapter_date(dates=self._dates),
                    "field": self._transducer,
                    "last": None,
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

    def _generate_data(self) -> List[Dict]:
        transducer: Transducer
        transducers = (
            Transducer.objects.filter(
                sensor__device__site__slug=self._setting["slug"],
                name=self._transducer,
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
                "sensor__id": "sensor_id",
            }
        )

        if len(list(set(_transducers["sensor_id"]))) > 0:
            self._setting["influxdb"]["settings_query"]["sensors"] = list(
                set(_transducers["sensor_id"])
            )

        influx_management = InfluxManagement(
            type_connect="client", settings=self._setting["influxdb"]["settings_query"]
        )
        _influxdb: DataFrame
        _influxdb = influx_management.query_management()
        if list(_influxdb.columns) == 0:
            return zero_data_control(module=LAST_MEASUREMENTS)

        _influxdb = _influxdb.rename(
            columns={
                FIELDS_INFLUXDB_FIELD: ALIAS_INFLUXDB_NAME,
                FIELDS_INFLUXDB_VALUE: ALIAS_INFLUXDB_VALUE,
                FIELDS_INFLUXDB_TIME: ALIAS_INFLUXDB_TIME,
            }
        )
        _data: DataFrame
        _data = merge(_transducers, _influxdb, on=["name", "sensor_id"], how="inner")

        if len(_data) > 1:
            drop_columns = [
                "sensor_id",
                "max_warning",
                "max_critical",
                "min_warning",
                "min_critical",
                "time",
            ]
            _data = _data.drop(columns=drop_columns)
            _data = _data.groupby(["name", "unit"]).agg({"value": "mean"}).reset_index()
        else:
            drop_columns = []
            _data = _data.drop(columns=drop_columns)
            _data = _data.reset_index()
        return self._to_dict(_data)
