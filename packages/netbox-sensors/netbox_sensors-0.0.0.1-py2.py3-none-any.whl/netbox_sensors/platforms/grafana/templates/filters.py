from typing import Dict

__all__ = (
    "filter_location",
    "filter_device",
    "filter_measurement",
)

filter_location: Dict = {
    "allValue": "Null",
    "current": {"selected": False, "text": "All", "value": "$__all"},
    "datasource": {"type": "postgres", "uid": "f6c71ba7-66b1-40e6-a56a-530a4a6900db"},
    "definition": 'SELECT loc."name" AS location\nFROM public.dcim_location loc\nJOIN '
    "public.dcim_site st ON loc.site_id = st.id \nWHERE st.slug = "
    "'$slug';",
    "hide": 0,
    "includeAll": True,
    "label": "Location",
    "multi": False,
    "name": "location",
    "options": [],
    "query": 'SELECT loc."name" AS location\nFROM public.dcim_location loc\nJOIN '
    "public.dcim_site st ON loc.site_id = st.id \nWHERE st.slug = '$slug';",
    "refresh": 1,
    "regex": "",
    "skipUrlSync": False,
    "sort": 0,
    "type": "query",
}

filter_device: Dict = {
    "allValue": "Null",
    "current": {"selected": False, "text": "All", "value": "$__all"},
    "datasource": {
        "type": "postgres",
        "uid": "f6c71ba7-66b1-40e6-a56a-530a4a6900db",
    },
    "definition": 'SELECT dev."name" AS location\nFROM public.dcim_device dev\nJOIN '
    "public.dcim_site st ON dev.site_id = st.id \nWHERE st.slug = "
    "'$slug';",
    "description": "Device name.",
    "hide": 0,
    "includeAll": True,
    "label": "Device",
    "multi": False,
    "name": "device",
    "options": [],
    "query": 'SELECT dev."name" AS location\nFROM public.dcim_device dev\nJOIN '
    "public.dcim_site st ON dev.site_id = st.id \nWHERE st.slug = "
    "'$slug';",
    "refresh": 1,
    "regex": "",
    "skipUrlSync": False,
    "sort": 0,
    "type": "query",
}

filter_measurement: Dict = {
    "allValue": "Null",
    "current": {"selected": True, "text": ["All"], "value": ["$__all"]},
    "hide": 0,
    "includeAll": True,
    "label": "Measurement",
    "multi": True,
    "name": "measurement",
    "options": [
        {"selected": True, "text": "All", "value": "$__all"},
        {"selected": False, "text": "pm4", "value": "pm4"},
        {"selected": False, "text": "lat", "value": "lat"},
        {"selected": False, "text": "alt", "value": "alt"},
        {"selected": False, "text": "t", "value": "t"},
        {"selected": False, "text": "h", "value": "h"},
        {"selected": False, "text": "pm10", "value": "pm10"},
        {"selected": False, "text": "co2", "value": "co2"},
        {"selected": False, "text": "pm1", "value": "pm1"},
        {"selected": False, "text": "lon", "value": "lon"},
        {"selected": False, "text": "pm2", "value": "pm2"},
        {"selected": False, "text": "nox", "value": "nox"},
        {"selected": False, "text": "voc", "value": "voc"},
    ],
    "query": "pm4, lat, alt, t, h, pm10, co2, pm1, lon, pm2, nox, voc,",
    "queryValue": "",
    "skipUrlSync": False,
    "type": "custom",
}
