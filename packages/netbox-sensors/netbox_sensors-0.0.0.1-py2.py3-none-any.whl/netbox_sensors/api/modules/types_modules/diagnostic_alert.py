from typing import Dict, List, Union

from django_pandas.io import read_frame
from pandas import DataFrame, merge
from sens_platform.api.modules.utils import detect_alerts, zero_data_control
from sens_platform.constants import *
from sens_platform.models import Sensor, Transducer
from sens_platform.platforms.influxdb.influxdb import InfluxManagement

from .abc_type_modules import AbstractTypeModules


class DiagnosticAlert(AbstractTypeModules):
    _name: str = DIAGNOSTIC_ALERT

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
                    "windows-aggregate-mean": True,
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
    def _to_dict(alerts: DataFrame) -> Union[List[Dict], Dict]:
        diagnostic: Dict = {"incidents": [], "incident_map": {}, "incident_types": []}
        for idx, alert in alerts.iterrows():
            diagnostic["incidents"].append(
                {"sensor": alert.to_dict(), "type": alert["type"]}
            )
            if alert["type"] not in diagnostic["incident_map"]:
                diagnostic["incident_map"][alert["type"]] = []
            diagnostic["incident_map"][alert["type"]].append(
                {"sensor": alert.to_dict(), "type": alert["type"]}
            )
        for idx, type_alert in enumerate(diagnostic["incident_map"]):
            diagnostic["incident_types"].append(
                {
                    "type": type_alert,
                    "incidents": diagnostic["incident_map"][type_alert],
                }
            )
        return diagnostic

    def _generate_data(self) -> Union[List[Dict], Dict]:
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
                "type__id": ALIAS_TRANSDUCER_TYPE_ID,
                "sensor__name": ALIAS_DASH_SENSOR_NAME,
                "sensor__id": ALIAS_SENSOR_ID,
            }
        )

        influx_management = InfluxManagement(
            type_connect="client", settings=self._setting["influxdb"]["settings_query"]
        )
        _influxdb: DataFrame
        _influxdb = influx_management.query_management()
        if list(_influxdb.columns) == 0:
            return zero_data_control(module=DIAGNOSTIC_ALERT)

        _influxdb = _influxdb.rename(
            columns={
                FIELDS_INFLUXDB_FIELD: ALIAS_INFLUXDB_NAME,
                FIELDS_INFLUXDB_VALUE: ALIAS_INFLUXDB_VALUE,
                FIELDS_INFLUXDB_TIME: ALIAS_INFLUXDB_TIME,
            }
        )

        _data: DataFrame = DataFrame()
        _data = merge(_transducers, _influxdb, on=["name", "sensor_id"], how="inner")

        grouped = _data.groupby(["type_id", "name"])["sensor_id"].unique().reset_index()
        grouped["sensors"] = grouped["sensor_id"].apply(list)
        _data = _data.merge(
            grouped[["type_id", "name", "sensors"]], on=["type_id", "name"], how="left"
        )

        drop_columns = ["id"]
        _data = _data.drop(columns=drop_columns)
        _data = _data.reset_index(drop=True)

        # temporal.
        _data["route"] = "/sensors/" + _data["sensor_id"].astype(str)
        _data["unit_html"] = _data["unit"]

        # calculation alert
        _data["type"] = _data.apply(detect_alerts, axis=1)
        alerts: DataFrame = _data[_data["type"] != "does not alert"]
        if alerts.shape[0] == 0:
            return {"incidents": [], "incident_map": {}, "incident_types": []}
        return self._to_dict(alerts)
