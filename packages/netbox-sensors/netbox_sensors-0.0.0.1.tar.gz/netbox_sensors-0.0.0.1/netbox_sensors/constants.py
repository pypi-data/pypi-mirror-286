from enum import Enum
from typing import Dict, List

PLUGIN_APPLICATION_NAME = "sens_platform"
PLUGIN_APPLICATION_BASE_URL = "sens-platform"
IMPORT_AUTO_DEVICE = (
    "Devices of the same type do not exist, sensors cannot be generated. "
    "Only the new device will be created."
)
IMPORT_AUTO_SENSOR = (
    "There are no sensors assigned to the device. The device will be "
    "created without sensors."
)
IMPORT_AUTO_TRANSDUCER = (
    "The sensor has no transducers assigned to it. The sensor will "
    "be created without transducers."
)

DEVICE_SCHEMATIC = {
    "name": str,
    "dev_id": int,
    "serial": str,
    "ts": str,
    "type": int,
    "type_version": int,
    "slug": str,
    "broker-servers": List,
    "dns-servers": List,
    "ntp_servers": List,
    "payload": {},
}
ICON_TYPES = (
    ("device_hub", "Undefined"),
    ("grain", "ppm, Pathogen, Small particle, CL"),
    ("group_work", "Particle, Large particle, KL"),
    ("cloud", "CO, CO2, NO2, H2S, CH4"),
    ("cloud_queue", "Organic"),
    ("ac_unit", "Humidity, Percentage (%), MRSA"),
    ("wb_sunny", "Temperature, degc"),
)

FIELDS_INFLUXDB_FIELD = "_field"
FIELDS_INFLUXDB_VALUE = "_value"
FIELDS_INFLUXDB_TIME = "_time"
FIELDS_INFLUXDB_MEASUREMENT = "_measurement"
FIELDS_INFLUXDB_DEVICE_TYPE = "device_type"
FIELDS_INFLUXDB_DEVICE_ID = "device_id"
FIELDS_INFLUXDB_MESSAGE_TYPE = "message_type"
FIELDS_INFLUXDB_SENSOR_ID = "sensor_id"
FIELDS_INFLUXDB_SENSOR_NAME = "sensor_name"

ALIAS_LOCATION = "location"
ALIAS_SENSOR_ID = "sensor_id"
ALIAS_DASH_SENSOR_NAME = "label_html"
ALIAS_SENSOR_NAME = "sensor_name"
ALIAS_DEVICE_NAME = "device"
ALIAS_TRANSDUCER_TYPE_ID = "type_id"
ALIAS_INFLUXDB_NAME = "name"
ALIAS_INFLUXDB_VALUE = "value"
ALIAS_INFLUXDB_TIME = "time"

AVERAGE_TRANSDUCER_TYPES = "average_transducer_types"
LAST_MEASUREMENTS = "last_measurements"
DIAGNOSTIC_ALERT = "diagnostic_alert"
ALL_DATA = "all_data"
DYNAMIC_KPIS = "dynamic_kpis"
AVERAGE_DATA = "average_data"
DEVICE_LOCATION = "device_location"
DEVICE_LOCATIONS = "device_locations"
POLAR_GRAPHS = "polar_graphs"
DEVICE_STATUS = "device_status"

SENSOR_TYPE_UNIFICATION: Dict = {"Name": "name", "name": "name"}


class ENTITIES(Enum):
    SENSOR_TYPE = "sensor_type"
    SENSOR = "sensor"
    TRANSDUCER = "transducer"
    TRANSDUCER_TYPE = "transducer_type"


TRANSDUCERS_NAME_CHOICES: List = [
    ("co2", "co2"),
    ("h", "h"),
    ("t", "t"),
    ("voc", "voc"),
    ("nox", "nox"),
    ("pm1", "pm1"),
    ("pm10", "pm10"),
    ("pm2", "pm2"),
    ("pm4", "pm4"),
    ("ch4", "ch4"),
    ("co", "co"),
    ("db", "db"),
    ("ch2o", "ch2o"),
    ("h2s", "h2s"),
    ("so2", "so2"),
    ("o3", "o3"),
    ("no2", "no2"),
    ("lat", "lat"),
    ("lon", "lon"),
    ("elev", "elev"),
    ("CL", "CL"),
    ("KP", "KP"),
    ("MRSA", "MRSA"),
    ("noise", "noise"),
    ("mV", "mV"),
    ("h2", "h2"),
    ("et", "et"),
    ("co2e", "co2e"),
]

TRANSDUCER_ALIAS = {
    "co2": "Carbon Dioxide",
    "h": "Humidity",
    "t": "Temperature",
    "voc": "Volatile Organic Compounds",
    "nox": "Nitrogen Oxides",
    "pm1": "Particulate Matter 1.0",
    "pm10": "Particulate Matter 10",
    "pm2": "Particulate Matter 2.5",
    "pm4": "Particulate Matter 4",
    "ch4": "Methane",
    "co": "Carbon Monoxide",
    "db": "Decibels",
    "ch2o": "Formaldehyde",
    "h2s": "Hydrogen Sulfide",
    "so2": "Sulfur Dioxide",
    "o3": "Ozone",
    "no2": "Nitrogen Dioxide",
    "lat": "Latitude",
    "lon": "Longitude",
    "elev": "Elevation",
    "CL": "Chlorine",
    "KP": "Key Performance",
    "MRSA": "Methicillin-Resistant Staphylococcus Aureus",
    "noise": "Noise",
    "mV": "Millivolts",
    "h2": "Hydrogen",
    "et": "Ethanol",
    "co2e": "Carbon Dioxide Equivalent",
}


DATATYPE_NAME_CHOICES: List = [
    ("int", "int"),
    ("float", "float"),
    ("str", "str"),
]

CATEGORIES_NAME_CHOICES: List = [
    ("transducer_type", "transducer_type"),
]
