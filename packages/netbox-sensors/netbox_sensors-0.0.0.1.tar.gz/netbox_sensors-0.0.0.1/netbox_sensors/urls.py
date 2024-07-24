from django.urls import path
from netbox.views.generic import ObjectChangeLogView

from . import models, views

urlpatterns = [
    # Transducer type
    path(
        "transducer-types/",
        views.TransducerTypeListView.as_view(),
        name="transducertype_list",
    ),
    path(
        "transducer-types/add/",
        views.TransducerTypeEditView.as_view(),
        name="transducertype_add",
    ),
    path(
        "transducer-types/<int:pk>/",
        views.TransducerTypeView.as_view(),
        name="transducertype",
    ),
    path(
        "transducer-types/<int:pk>/edit/",
        views.TransducerTypeEditView.as_view(),
        name="transducertype_edit",
    ),
    path(
        "transducer-types/<int:pk>/delete/",
        views.TransducerTypeDeleteView.as_view(),
        name="transducertype_delete",
    ),
    path(
        "transducer-types/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="transducertype_changelog",
        kwargs={"model": models.TransducerType},
    ),
    path(
        "transducer-types/import/",
        views.TransducerTypeBulkImportView.as_view(),
        name="transducertype_import",
    ),
    # Transducer
    path("transducer/", views.TransducerListView.as_view(), name="transducer_list"),
    path("transducer/add/", views.TransducerEditView.as_view(), name="transducer_add"),
    path("transducer/<int:pk>/", views.TransducerView.as_view(), name="transducer"),
    path(
        "transducer/<int:pk>/edit/",
        views.TransducerEditView.as_view(),
        name="transducer_edit",
    ),
    path(
        "transducer/<int:pk>/delete/",
        views.TransducerDeleteView.as_view(),
        name="transducer_delete",
    ),
    path(
        "transducer/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="transducer_changelog",
        kwargs={"model": models.Transducer},
    ),
    path(
        "transducer/import/",
        views.TransducerBulkImportView.as_view(),
        name="transducer_import",
    ),
    path(
        "transducer/delete/",
        views.TransducerBulkDeleteView.as_view(),
        name="transducer_bulk_delete",
    ),
    # sensor-types
    path("sensor-types/", views.SensorTypeListView.as_view(), name="sensortype_list"),
    path(
        "sensor-types/add/", views.SensorTypeEditView.as_view(), name="sensortype_add"
    ),
    path(
        "sensor-types/import/",
        views.SensorTypeBulkImportView.as_view(),
        name="sensortype_import",
    ),
    path("sensor-types/<int:pk>/", views.SensorTypeView.as_view(), name="sensortype"),
    path(
        "sensor-types/<int:pk>/edit/",
        views.SensorTypeEditView.as_view(),
        name="sensortype_edit",
    ),
    path(
        "sensor-types/<int:pk>/delete/",
        views.SensorTypeDeleteView.as_view(),
        name="sensortype_delete",
    ),
    path(
        "sensor-types/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="sensortype_changelog",
        kwargs={"model": models.SensorType},
    ),
    # Sensor
    path("sensors/", views.SensorListView.as_view(), name="sensor_list"),
    path("sensors/add/", views.SensorEditView.as_view(), name="sensor_add"),
    path("sensors/<int:pk>/", views.SensorView.as_view(), name="sensor"),
    path("sensors/<int:pk>/edit/", views.SensorEditView.as_view(), name="sensor_edit"),
    path(
        "sensors/<int:pk>/delete/",
        views.SensorDeleteView.as_view(),
        name="sensor_delete",
    ),
    path(
        "sensors/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="sensor_changelog",
        kwargs={"model": models.Sensor},
    ),
    path("sensors/import/", views.SensorBulkImportView.as_view(), name="sensor_import"),
    path(
        "sensors/delete/",
        views.SensorBulkDeleteView.as_view(),
        name="sensor_bulk_delete",
    ),
    # Attribute mapping
    path(
        "attributemapping/",
        views.AttributeMappingListView.as_view(),
        name="attributemapping_list",
    ),
    path(
        "attributemapping/add/",
        views.AttributeMappingEditView.as_view(),
        name="attributemapping_add",
    ),
    path(
        "attributemapping/<int:pk>/edit/",
        views.AttributeMappingEditView.as_view(),
        name="attributemapping_edit",
    ),
    path(
        "attributemapping/<int:pk>/delete/",
        views.AttributeMappingDeleteView.as_view(),
        name="attributemapping_delete",
    ),
    path(
        "attributemapping/<int:pk>/",
        views.AttributeMappingView.as_view(),
        name="attributemapping",
    ),
    path(
        "attributemapping/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="attributemapping_changelog",
        kwargs={"model": models.AttributeMapping},
    ),
    # Custom devices
    path(
        "custom-devices-list/",
        views.CustomDevicesListView.as_view(),
        name="custom_devices_list",
    ),
    path(
        "custom-device-updates/",
        views.CustomDeviceUpdatesView.as_view(),
        name="custom_device_updates",
    ),
    path(
        "custom-devices-download-template/",
        views.CustomDevicesDownloadTemplateView.as_view(),
        name="custom_device_download_template",
    ),
    path(
        "custom-action/",
        views.CustomActionView.as_view(),
        name="custom_action",
    ),
    path(
        "custom-devices-duplicate/",
        views.CustomDevicesDuplicateView.as_view(),
        name="custom_devices_duplicate",
    ),
    path(
        "custom-devices-delete/",
        views.CustomDevicesDeleteView.as_view(),
        name="custom_devices_delete",
    ),
    path(
        "device-render-config/<int:pk>/",
        views.CustomDeviceRenderConfigView.as_view(),
        name="device_render_config",
    ),
]
