from typing import List

from pandas import DataFrame


def setup_test_database() -> dict:
    """Implemented to do tests with temporary data."""
    diagnostic_alert = DataFrame(
        {
            "name": {0: "ch2o", 1: "ch4", 2: "co", 3: "co2", 4: "co2", 5: "dB"},
            "sensor_id": {0: "14", 1: "7", 2: "12", 3: "3", 4: "4", 5: "13"},
            "unit": {0: "ppm", 1: "ppm", 2: "ppm", 3: "ppm", 4: "ppm", 5: "dB"},
            "icon": {
                0: "cloud",
                1: "cloud",
                2: "cloud",
                3: "device_hub",
                4: "device_hub",
                5: "device_hub",
            },
            "type_id": {0: "17", 1: "10", 2: "15", 3: "9", 4: "9", 5: "16"},
            "max_warning": {
                0: "None",
                1: "None",
                2: "None",
                3: "None",
                4: "None",
                5: "None",
            },
            "max_critical": {
                0: "None",
                1: "None",
                2: "None",
                3: "None",
                4: "None",
                5: "None",
            },
            "min_warning": {
                0: "None",
                1: "None",
                2: "None",
                3: "None",
                4: "None",
                5: "None",
            },
            "min_critical": {
                0: "None",
                1: "None",
                2: "None",
                3: "None",
                4: "None",
                5: "None",
            },
            "location": {
                0: "location 2",
                1: "location 2",
                2: "location 2",
                3: "Location 1",
                4: "location 2",
                5: "location 2",
            },
            "label_html": {
                0: "SFA30",
                1: "INIR-ME",
                2: "ULPSMCO",
                3: "SCD30",
                4: "SCD30",
                5: "MAX4466",
            },
            "value": {0: 0.0, 1: None, 2: 0.435, 3: 51.0, 4: 51.0, 5: 0.385},
            "time": {
                0: "2023-09-07 11:58:40+0000",
                1: "2023-09-07 11:55:40+0000",
                2: "2023-09-07 10:00:40+0000",
                3: "2023-09-07 11:57:00+0000",
                4: "2023-09-07 10:59:40+0000",
                5: "2023-09-07 10:59:40+0000",
            },
            "sensors": {
                0: ["14"],
                1: ["7"],
                2: ["12"],
                3: ["3", "4"],
                4: ["3", "4"],
                5: ["13"],
            },
            "route": {
                0: "/sensors/14",
                1: "/sensors/7",
                2: "/sensors/12",
                3: "/sensors/3",
                4: "/sensors/4",
                5: "/sensors/13",
            },
            "unit_html": {0: "ppm", 1: "ppm", 2: "ppm", 3: "ppm", 4: "ppm", 5: "dB"},
        }
    )
    fake_average_transducer_types = {
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
    fake_last_measurements: List = [
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
    return locals()
