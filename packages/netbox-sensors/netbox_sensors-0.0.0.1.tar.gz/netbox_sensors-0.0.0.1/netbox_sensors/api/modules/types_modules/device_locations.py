import json
from datetime import datetime
from typing import Union

from dcim.models import Device
from django_pandas.io import read_frame
from pandas import DataFrame, merge
from sens_platform.api.modules.utils import zero_data_control
from sens_platform.constants import *
from sens_platform.platforms.influxdb.influxdb import InfluxManagement

from .abc_type_modules import AbstractTypeModules

__all__ = ("DeviceLocations",)


class DeviceLocations(AbstractTypeModules):
    _name: str = DEVICE_LOCATION

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
                "model": Device,
                "columns_init": ["id", "name"],
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
                    "windows": False,
                    "mean": False,
                    "windows-aggregate-mean": False,
                    "range": self._adapter_date(dates=self._dates),
                    "field": ["lat", "lon", "elev"],
                    "last": True,
                    "columns_dataframe": [
                        FIELDS_INFLUXDB_DEVICE_ID,
                        FIELDS_INFLUXDB_VALUE,
                        FIELDS_INFLUXDB_FIELD,
                        FIELDS_INFLUXDB_TIME,
                    ],
                }
            },
        }

    @staticmethod
    def _adapter_date(dates: Dict):
        formatted_start = datetime.strptime(
            dates["start"], "%Y-%m-%dT%H:%M:%S.%fZ"
        ).strftime("%Y-%m-%dT%H:%M:%SZ")
        formatted_end = datetime.strptime(
            dates["end"], "%Y-%m-%dT%H:%M:%S.%fZ"
        ).strftime("%Y-%m-%dT%H:%M:%SZ")
        return f"start: {formatted_start}, stop: {formatted_end}"

    @staticmethod
    def _to_dict(data: DataFrame) -> Union[List[Dict], Dict]:
        return data.to_dict(orient="records")

    def _generate_data(self) -> List[Dict]:
        devs = Device.objects.filter(
            site__slug=self._setting["slug"],
            **({"name": self._device} if self._device else {}),
        )
        _devices: DataFrame
        _devices = read_frame(
            devs,
            fieldnames=self._setting["postgres"]["columns_init"],
            verbose=False,
        )
        _devices = _devices.rename(columns={"id": "device_id", "name": "device"})
        influx_management = InfluxManagement(
            type_connect="client", settings=self._setting["influxdb"]["settings_query"]
        )
        _influxdb: DataFrame
        _influxdb = influx_management.query_management()
        if _influxdb.empty:
            return zero_data_control(module=DEVICE_LOCATION)
        _influxdb = _influxdb.rename(
            columns={
                FIELDS_INFLUXDB_FIELD: ALIAS_INFLUXDB_NAME,
                FIELDS_INFLUXDB_VALUE: ALIAS_INFLUXDB_VALUE,
                FIELDS_INFLUXDB_TIME: ALIAS_INFLUXDB_TIME,
            }
        )
        _influxdb["device_id"] = _influxdb["device_id"].astype("int64")
        _data: DataFrame
        _data = merge(_devices, _influxdb, on=["device_id"], how="inner")

        if len(_data) > 1:
            drop_columns = [
                "time",
            ]
            _data = _data.drop(columns=drop_columns)
            # _data = (
            #     _data.groupby(["device_id", "name", "device"])
            #     .agg({"value": "mean"})
            #     .reset_index()
            # )
        else:
            drop_columns = []
            _data = _data.drop(columns=drop_columns)
            _data = _data.reset_index()

        processed_data = []
        devices = {}
        for item in self._to_dict(_data):
            if item["device"] not in devices:
                devices[item["device"]] = {}
            devices[item["device"]][item["name"]] = item["value"]

        for device, info in devices.items():
            processed_data.append(
                {
                    "key": device,
                    "latitude": info["lat"] * 10**-7,
                    "longitude": info["lon"] * 10**-7,
                    "tooltip": f"Device ID: {device.split('-')[-1]}, "
                    f"Elevation: {round(info['elev'] * 10**-3, 4)}",
                }
            )
        return processed_data
