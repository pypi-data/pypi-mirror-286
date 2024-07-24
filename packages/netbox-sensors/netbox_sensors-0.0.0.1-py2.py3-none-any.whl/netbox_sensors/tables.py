import django_tables2 as tables
from dcim.models.devices import Device
from netbox.tables import NetBoxTable
from sens_platform.columns import CustomActionsColumn

from .models import (
    SENSOR_RANGE_FIELDS,
    AttributeMapping,
    Sensor,
    SensorType,
    Transducer,
    TransducerType,
)


class SensorTypeTable(NetBoxTable):
    name = tables.Column(linkify=True)
    nb_sensors = tables.Column()

    class Meta(NetBoxTable.Meta):
        model = SensorType
        fields = ["pk", "id", "name", "nb_sensors"]
        default_columns = fields[2:]


class SensorTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = Sensor
        fields = [
            "pk",
            "id",
            "name",
            "type",
            "device",
            "customer_id",
            "serial",
        ]
        default_columns = fields[2:]


class TransducerTypeTable(NetBoxTable):
    name = tables.Column(linkify=True)
    nb_transducers = tables.Column()

    class Meta(NetBoxTable.Meta):
        model = TransducerType
        fields = [
            "pk",
            "id",
            "name",
            "sensor_type",
            "dash",
            "unit",
        ] + SENSOR_RANGE_FIELDS
        default_columns = fields[2:]


class TransducerTable(NetBoxTable):
    name = tables.Column(linkify=True)
    sensor__device = tables.Column(linkify=True)
    sensor__serial = tables.Column()

    class Meta(NetBoxTable.Meta):
        model = Transducer
        fields = [
            "pk",
            "id",
            "name",
            "type",
            "sensor",
            "sensor__serial",
            "sensor__device",
            "dash",
            "unit",
        ]
        default_columns = fields[2:]


class AttributeMappingTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = AttributeMapping
        fields = ["pk", "id", "name", "category", "type", "description"]
        default_columns = fields[1:]


DEVICE_LINK = """
{{ value|default:'<span class="badge bg-info">Unnamed device</span>' }}
"""


class CustomDevicesTable(NetBoxTable):
    name = tables.TemplateColumn(
        order_by=("_name",), template_code=DEVICE_LINK, linkify=True
    )
    serial = tables.Column(verbose_name="Serial")
    device_type = tables.Column(linkify=True, verbose_name="Type")
    site = tables.Column(linkify=True)

    actions = CustomActionsColumn()

    class Meta(NetBoxTable.Meta):
        model = Device
        fields = ["pk" "id", "name", "serial", "device_type", "site", "actions"]
        default_columns = fields[1:]
