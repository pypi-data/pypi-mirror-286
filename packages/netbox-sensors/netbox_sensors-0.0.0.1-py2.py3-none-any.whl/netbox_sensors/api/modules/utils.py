from datetime import datetime
from typing import Dict, List, Union

from pandas import Series, isna
from sens_platform.constants import (
    ALL_DATA,
    AVERAGE_TRANSDUCER_TYPES,
    DEVICE_LOCATION,
    DEVICE_STATUS,
    DIAGNOSTIC_ALERT,
    DYNAMIC_KPIS,
    LAST_MEASUREMENTS,
    POLAR_GRAPHS,
)


def zero_data_control(module: str) -> Union[Dict, List[Dict]]:
    """
    Fake data is sent to the dashboard when there is no
    measurement data.

    Parameters
    ----------
    module: str
        Module name.

    Returns
    -------
    fake: Union[Dick, List[Dict]]
        Fake data.
    """
    fake: Union[Dict, List[Dict]]
    if module in [LAST_MEASUREMENTS, DIAGNOSTIC_ALERT]:
        fake = [
            {
                "name": "--",
                "sensor_id": "0",
                "unit": "---",
                "icon": "cloud",
                "type_id": "0",
                "max_warning": "None",
                "max_critical": "None",
                "min_warning": "None",
                "min_critical": "None",
                "location": "-------",
                "label_html": "------",
                "value": 0.000,
                "time": "2023-01-01 00:00:00+0000",
                "sensors": ["0"],
                "route": "/sensors/0",
                "unit_html": "--",
            },
        ]
    if module == AVERAGE_TRANSDUCER_TYPES:
        fake = {
            "--": {
                "name": "---",
                "unit": "---",
                "icon": "cloud",
                "type_id": "--",
                "average": 0.000,
                "minimum": 0.000,
                "maximum": 0.000,
                "sensors": ["0"],
                "label_html": "--",
                "route": "--",
                "unit_html": "--",
            },
        }
    if module == DEVICE_LOCATION:
        fake = [
            {
                "key": "Sens solutions",
                "latitude": 41.5015227372152,
                "longitude": 2.1086484702714694,
                "tooltip": "Sens solutions: No devices.",
            }
        ]
    if module == ALL_DATA:
        fake = [
            {
                "name": "None",
                "sensor_id": "0",
                "unit": "None",
                "max_warning": "None",
                "max_critical": "None",
                "min_warning": "None",
                "min_critical": "None",
                "location": "None",
                "device": "None",
                "sensor__device__id": "0",
                "sensor_name": "None",
                "value": 0.00,
                "time": "0000-00-00T00:00:00Z",
            }
        ]
    if module == DYNAMIC_KPIS:
        fake = {
            "name": "None",
            "unit": "-",
            "value": 00.00,
        }
    if module == DEVICE_STATUS:
        fake = [{"name": "None", "device_id": "0", "check": True}]
    if module == POLAR_GRAPHS:
        fake = {
            "none": [
                {
                    "fill": "toself",
                    "name": "None",
                    "r": [
                        0,
                    ],
                    "theta": [
                        "None",
                    ],
                    "type": "scatterpolar",
                }
            ],
        }
    return fake


def detect_alerts(row: Series) -> str:
    """
    Method to detect alerts based on log values and time. Basic version.

    Parameters
    ----------
    row: Series
        Value and time of measurement.

    Returns
    -------
    str
        Types alerts.
    """
    current_date = datetime.now()
    tz = row["time"].tzinfo
    current_date = current_date.replace(tzinfo=tz)
    elapsed_time_minutes = (current_date - row["time"]).total_seconds() / 60
    if elapsed_time_minutes > 20:
        return "non responsive"
    if isna(row["value"]) or row["value"] is None:
        return "no value"
    if row["value"] == 0.0:
        return "no value"
    return "does not alert"
