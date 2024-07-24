from typing import Union

from django_pandas.io import read_frame
from pandas import DataFrame, merge
from sens_platform.api.modules.utils import zero_data_control
from sens_platform.constants import *
from sens_platform.models import Device
from sens_platform.platforms.influxdb.influxdb import InfluxManagement

from .abc_type_modules import AbstractTypeModules

__all__ = ("DeviceStatus",)


class DeviceStatus(AbstractTypeModules):
    _name: str = DEVICE_STATUS
    _location: str
    _device: str
    _dates: Dict

    def __init__(
        self,
        slug: str,
        dates: Dict,
        device: str = None,
        location: str = None,
        time_window: str = None,
    ):
        super().__init__(
            slug=slug,
            dates=dates,
            location=location,
            device=device,
            time_window=time_window,
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
                    "field": None,
                    "windows": False,
                    "group": ["_field", "device_id"],
                    "drop": ["_start", "_stop", "_time"],
                    "mean": True,
                    "windows-aggregate-mean": False,
                    "range": self._adapter_date(dates=self._dates),
                    "last": False,
                    "columns_dataframe": [
                        FIELDS_INFLUXDB_DEVICE_ID,
                        FIELDS_INFLUXDB_VALUE,
                        FIELDS_INFLUXDB_FIELD,
                    ],
                }
            },
        }

    @staticmethod
    def _to_dict(data: DataFrame) -> Union[List[Dict], Dict]:
        return data.to_dict(orient="records")

    def _generate_data(self) -> List[Dict]:
        devices: Device
        devices = Device.objects.filter(site__slug=self._setting["slug"])
        _devices: DataFrame
        _devices = read_frame(
            devices,
            fieldnames=self._setting["postgres"]["columns_init"],
            verbose=False,
        )
        _devices = _devices.rename(
            columns={
                "id": "device_id",
            }
        )
        _devices["device_id"] = _devices["device_id"].astype(str)

        influx_management = InfluxManagement(
            type_connect="client", settings=self._setting["influxdb"]["settings_query"]
        )
        _influxdb: DataFrame
        _influxdb = influx_management.query_management()
        if _influxdb.empty:
            return zero_data_control(module=DEVICE_STATUS)
        _data: DataFrame
        _data = merge(_devices, _influxdb, on=["device_id"], how="inner")
        _data["check"] = _data.groupby("device_id")["_value"].transform(
            lambda x: x.notnull().any()
        )
        _data = _data[["name", "device_id", "check"]].drop_duplicates()

        _devices_copy = _devices.copy()
        _devices_copy["check"] = False
        merged_data = merge(_data, _devices_copy, on=["device_id", "name"], how="outer")
        merged_data["check"] = merged_data["check_x"].combine_first(
            merged_data["check_y"]
        )
        merged_data = merged_data.drop(columns=["check_x", "check_y"])
        merged_data = merged_data.drop_duplicates(subset="device_id", keep="first")
        return self._to_dict(merged_data)
