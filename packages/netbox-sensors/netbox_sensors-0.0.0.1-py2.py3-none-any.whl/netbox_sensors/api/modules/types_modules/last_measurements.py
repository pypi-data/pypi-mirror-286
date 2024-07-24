from typing import Union

from django_pandas.io import read_frame
from pandas import DataFrame, merge
from sens_platform.api.modules.utils import zero_data_control
from sens_platform.constants import *
from sens_platform.models import Sensor, Transducer
from sens_platform.platforms.influxdb.influxdb import InfluxManagement

from .abc_type_modules import AbstractTypeModules


class LastMeasurements(AbstractTypeModules):
    _name: str = LAST_MEASUREMENTS

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
        sensors: Sensor
        sensors = Sensor.objects.filter(device__site__slug=self._slug).values_list(
            "id", flat=True
        )
        self._setting = {
            "slug": self._slug,
            "postgres": {
                "model": Transducer,
                "columns_init": [
                    "id",
                    "name",
                    "sensor__id",
                    "unit",
                    "icon",
                    "type__id",
                    "max_warning",
                    "max_critical",
                    "min_warning",
                    "min_critical",
                    "sensor__device__location__name",
                    "sensor__name",
                ],
            },
            "influxdb": {
                "settings_query": {
                    "slug": self._slug,
                    "measurement": "environment",
                    "bucket": "data",
                    "sensors": list(sensors),
                    "devices": None,
                    "field": None,
                    "group": [FIELDS_INFLUXDB_FIELD, FIELDS_INFLUXDB_SENSOR_ID],
                    "drop": None,
                    "windows": False,
                    "mean": False,
                    "windows-aggregate-mean": False,
                    "range": "-1h",
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

    def _generate_data(self) -> List[Dict]:
        transducer: Transducer
        transducers = (
            Transducer.objects.filter(sensor__device__site__slug=self._setting["slug"])
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
                "type__id": ALIAS_TRANSDUCER_TYPE_ID,
                "sensor__name": ALIAS_SENSOR_NAME,
            }
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

        grouped = _data.groupby(["type_id", "name"])["sensor_id"].unique().reset_index()
        grouped["sensors"] = grouped["sensor_id"].apply(list)
        _data = _data.merge(
            grouped[["type_id", "name", "sensors"]], on=["type_id", "name"], how="left"
        )

        drop_columns = ["id"]
        _data = _data.drop(columns=drop_columns)
        # _data = _data[0:6]
        _data = _data.reset_index(drop=True)

        # temporal.
        _data["route"] = "/sensors/" + _data["sensor_id"].astype(str)
        _data["unit_html"] = _data["unit"]

        return self._to_dict(_data)
