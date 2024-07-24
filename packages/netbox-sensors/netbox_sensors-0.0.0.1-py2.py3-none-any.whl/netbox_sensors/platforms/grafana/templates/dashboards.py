from typing import Dict

__all__ = (
    "db_base",
    "db_base_1",
)


db_base: Dict = {
    "dashboard": {
        "title": "Production Overview",
        "tags": ["templated"],
        "timezone": "browser",
        "rows": [{}],
        "schemaVersion": 6,
        "version": 0,
    },
    "overwrite": False,
}

db_base_1: Dict = {
    "dashboard": {
        "id": None,
        "title": "DASHBOARD",
        "tags": ["templated"],
        "timezone": "browser",
        "panels": [
            {
                "datasource": {
                    "type": "marcusolsson-json-datasource",
                    "uid": "db8f349f-59ba-42aa-8c97-d3161894a772",
                },
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "thresholds"},
                        "custom": {
                            "align": "auto",
                            "cellOptions": {"type": "auto"},
                            "filterable": True,
                            "inspect": True,
                        },
                        "mappings": [],
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [
                                {"color": "green", "value": None},
                                {"color": "red", "value": 80},
                            ],
                        },
                    },
                    "overrides": [],
                },
                "gridPos": {"h": 14, "w": 18, "x": 0, "y": 0},
                "id": 25,
                "options": {
                    "cellHeight": "md",
                    "footer": {
                        "countRows": False,
                        "enablePagination": True,
                        "fields": "",
                        "reducer": ["sum"],
                        "show": False,
                    },
                    "showHeader": True,
                    "sortBy": [{"desc": False, "displayName": "Measurement"}],
                },
                "pluginVersion": "9.5.3",
                "targets": [
                    {
                        "body": '{\n  "name": "all_data",\n  "settings": {\n    "slug": "$slug",\n    "location": "$location",\n    "device": "$device",\n    "transducer": "$measurement",\n    "dates": {"start": "$__isoFrom()", "end": "$__isoTo()"}\n  }\n}',
                        "cacheDurationSeconds": 300,
                        "datasource": {
                            "type": "marcusolsson-json-datasource",
                            "uid": "db8f349f-59ba-42aa-8c97-d3161894a772",
                        },
                        "fields": [
                            {
                                "jsonPath": "$.all_data[*].time",
                                "language": "jsonpath",
                                "name": "Date",
                            },
                            {
                                "jsonPath": "$.all_data[*].device",
                                "language": "jsonpath",
                                "name": "Device",
                            },
                            {
                                "jsonPath": "$.all_data[*].sensor_name",
                                "language": "jsonpath",
                                "name": "Sensor",
                            },
                            {
                                "jsonPath": "$.all_data[*].name",
                                "language": "jsonpath",
                                "name": "Measurement",
                            },
                            {
                                "jsonPath": "$.all_data[*].value",
                                "language": "jsonpath",
                                "name": "Value",
                            },
                            {
                                "jsonPath": "$.all_data[*].unit",
                                "language": "jsonpath",
                                "name": "Unit",
                            },
                        ],
                        "method": "POST",
                        "queryParams": "",
                        "refId": "A",
                        "urlPath": "/api/plugins/sens-platform/modules/",
                    }
                ],
                "title": "Measurement",
                "type": "table",
            },
            {
                "datasource": {
                    "type": "postgres",
                    "uid": "f6c71ba7-66b1-40e6-a56a-530a4a6900db",
                },
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "thresholds"},
                        "custom": {
                            "align": "center",
                            "cellOptions": {"type": "auto"},
                            "filterable": True,
                            "inspect": False,
                        },
                        "mappings": [],
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [
                                {"color": "green", "value": None},
                                {"color": "red", "value": 80},
                            ],
                        },
                    },
                    "overrides": [
                        {
                            "matcher": {"id": "byName", "options": "Device name"},
                            "properties": [{"id": "custom.width", "value": 188}],
                        }
                    ],
                },
                "gridPos": {"h": 14, "w": 6, "x": 18, "y": 0},
                "id": 16,
                "options": {
                    "cellHeight": "sm",
                    "footer": {
                        "countRows": False,
                        "enablePagination": True,
                        "fields": "",
                        "reducer": ["sum"],
                        "show": False,
                    },
                    "showHeader": True,
                    "sortBy": [],
                },
                "pluginVersion": "9.5.3",
                "targets": [
                    {
                        "datasource": {
                            "type": "postgres",
                            "uid": "f6c71ba7-66b1-40e6-a56a-530a4a6900db",
                        },
                        "editorMode": "code",
                        "format": "table",
                        "hide": False,
                        "rawQuery": True,
                        "rawSql": "SELECT dd.name as \"Devices\"\nFROM dcim_device dd\nJOIN dcim_site ds ON dd.site_id = ds.id\nWHERE ds.slug = 'inchildhealth';",
                        "refId": "A",
                        "sql": {
                            "columns": [],
                            "groupBy": [
                                {"property": {"type": "string"}, "type": "groupBy"}
                            ],
                            "limit": 50,
                        },
                    }
                ],
                "title": "List devices",
                "type": "table",
            },
            {
                "datasource": {
                    "type": "marcusolsson-json-datasource",
                    "uid": "db8f349f-59ba-42aa-8c97-d3161894a772",
                },
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "palette-classic"},
                        "custom": {
                            "axisCenteredZero": False,
                            "axisColorMode": "series",
                            "axisLabel": "",
                            "axisPlacement": "auto",
                            "barAlignment": 0,
                            "drawStyle": "line",
                            "fillOpacity": 0,
                            "gradientMode": "none",
                            "hideFrom": {
                                "legend": False,
                                "tooltip": False,
                                "viz": False,
                            },
                            "lineInterpolation": "smooth",
                            "lineWidth": 1,
                            "pointSize": 5,
                            "scaleDistribution": {"type": "linear"},
                            "showPoints": "auto",
                            "spanNulls": False,
                            "stacking": {"group": "A", "mode": "none"},
                            "thresholdsStyle": {"mode": "off"},
                        },
                        "mappings": [],
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [
                                {"color": "green", "value": None},
                                {"color": "red", "value": 80},
                            ],
                        },
                    },
                    "overrides": [],
                },
                "gridPos": {"h": 15, "w": 14, "x": 0, "y": 14},
                "id": 26,
                "options": {
                    "legend": {
                        "calcs": [],
                        "displayMode": "table",
                        "placement": "right",
                        "showLegend": True,
                    },
                    "tooltip": {"mode": "multi", "sort": "asc"},
                },
                "pluginVersion": "9.5.3",
                "targets": [
                    {
                        "body": '{\n  "name": "all_data",\n  "settings": {\n    "slug": "$slug",\n    "location": "$location",\n    "device": "$device",\n    "transducer": "$measurement",\n    "dates": {"start": "$__isoFrom()", "end": "$__isoTo()"}\n  }\n}',
                        "cacheDurationSeconds": 300,
                        "datasource": {
                            "type": "marcusolsson-json-datasource",
                            "uid": "db8f349f-59ba-42aa-8c97-d3161894a772",
                        },
                        "fields": [
                            {
                                "jsonPath": "$.all_data[*].time",
                                "language": "jsonpath",
                                "name": "Date",
                            },
                            {
                                "jsonPath": "$.all_data[*].device",
                                "language": "jsonpath",
                                "name": "Device",
                            },
                            {
                                "jsonPath": "$.all_data[*].name",
                                "language": "jsonpath",
                                "name": "Measurement",
                            },
                            {
                                "jsonPath": "$.all_data[*].value",
                                "language": "jsonpath",
                                "name": "Value",
                            },
                        ],
                        "method": "POST",
                        "queryParams": "",
                        "refId": "A",
                        "urlPath": "/api/plugins/sens-platform/modules/",
                    }
                ],
                "title": "Measurement",
                "type": "timeseries",
            },
            {
                "datasource": {
                    "type": "marcusolsson-json-datasource",
                    "uid": "da6d186c-0081-4e02-9ad9-25f54362e631",
                },
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "thresholds"},
                        "custom": {
                            "hideFrom": {
                                "legend": False,
                                "tooltip": False,
                                "viz": False,
                            }
                        },
                        "mappings": [],
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [
                                {"color": "green", "value": None},
                                {"color": "red", "value": 80},
                            ],
                        },
                    },
                    "overrides": [],
                },
                "gridPos": {"h": 15, "w": 10, "x": 14, "y": 14},
                "id": 23,
                "options": {
                    "basemap": {"config": {}, "name": "Layer 0", "type": "default"},
                    "controls": {
                        "mouseWheelZoom": True,
                        "showAttribution": True,
                        "showDebug": False,
                        "showMeasure": False,
                        "showScale": False,
                        "showZoom": True,
                    },
                    "layers": [
                        {
                            "config": {
                                "showLegend": True,
                                "style": {
                                    "color": {"fixed": "dark-green"},
                                    "opacity": 0.4,
                                    "rotation": {
                                        "fixed": 0,
                                        "max": 360,
                                        "min": -360,
                                        "mode": "mod",
                                    },
                                    "size": {"fixed": 5, "max": 15, "min": 2},
                                    "symbol": {
                                        "fixed": "img/icons/marker/circle.svg",
                                        "mode": "fixed",
                                    },
                                    "textConfig": {
                                        "fontSize": 12,
                                        "offsetX": 0,
                                        "offsetY": 0,
                                        "textAlign": "center",
                                        "textBaseline": "middle",
                                    },
                                },
                            },
                            "location": {"mode": "auto"},
                            "name": "Devices",
                            "tooltip": True,
                            "type": "markers",
                        }
                    ],
                    "tooltip": {"mode": "details"},
                    "view": {
                        "allLayers": True,
                        "id": "europe",
                        "lat": 46,
                        "lon": 14,
                        "shared": False,
                        "zoom": 4,
                    },
                },
                "pluginVersion": "9.5.3",
                "targets": [
                    {
                        "body": '{\n  "name": "device_location",\n  "settings": {\n    "slug": "inchildhealth",\n    "dates": {"start": "$__isoFrom()", "end": "$__isoTo()"}\n  }\n}',
                        "cacheDurationSeconds": 300,
                        "datasource": {
                            "type": "marcusolsson-json-datasource",
                            "uid": "da6d186c-0081-4e02-9ad9-25f54362e631",
                        },
                        "fields": [
                            {
                                "jsonPath": "$.device_location[*].latitude",
                                "name": "lat",
                            },
                            {
                                "jsonPath": "$.device_location[*].longitude",
                                "language": "jsonpath",
                                "name": "lon",
                            },
                            {
                                "jsonPath": "$.device_location[*].tooltip",
                                "language": "jsonpath",
                                "name": "tooltip",
                            },
                        ],
                        "method": "POST",
                        "queryParams": "",
                        "refId": "A",
                        "urlPath": "/api/plugins/sens-platform/modules/",
                    }
                ],
                "title": "Device location",
                "type": "geomap",
            },
        ],
        "templating": {"list": []},
        "schemaVersion": 6,
        "version": 0,
    },
    "overwrite": False,
}
