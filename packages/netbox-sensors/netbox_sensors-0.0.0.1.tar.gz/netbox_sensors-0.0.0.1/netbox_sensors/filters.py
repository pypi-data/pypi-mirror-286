from dcim.models import Device, DeviceType, Site
from django.db.models import Q
from django.utils.translation import gettext as _
from netbox.filtersets import NetBoxModelFilterSet
from sens_platform.models import (
    AttributeMapping,
    Sensor,
    SensorType,
    Transducer,
    TransducerType,
)
from utilities.filters import TreeNodeMultipleChoiceFilter


class SensorTypeFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = SensorType
        fields = ("id", "name")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value)
        return queryset.filter(qs_filter).distinct()


class SensorFilterSet(NetBoxModelFilterSet):
    device = TreeNodeMultipleChoiceFilter(
        queryset=Device.objects.all(),
        lookup_expr="in",
        field_name="device__name",
        to_field_name="device",
        label=_("Device (name)"),
    )

    type = TreeNodeMultipleChoiceFilter(
        queryset=SensorType.objects.all(),
        lookup_expr="in",
        field_name="type__name",
        to_field_name="type",
        label=_("Sensor type (name)"),
    )

    class Meta:
        model = Sensor
        fields = ("id", "name", "device", "type", "serial", "customer_id")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(device__name__icontains=value)
            | Q(type__name__icontains=value)
            | Q(serial__icontains=value)
            | Q(customer_id__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()


class TransducerTypeFilterSet(NetBoxModelFilterSet):
    sensor_type = TreeNodeMultipleChoiceFilter(
        queryset=SensorType.objects.all(),
        lookup_expr="in",
        field_name="sensor_type__name",
        to_field_name="sensor_type",
        label=_("Sensor type (name)"),
    )

    class Meta:
        model = TransducerType
        fields = ("id", "name", "sensor_type", "unit")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(sensor_type__name__icontains=value)
            | Q(unit__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()


class TransducerFilterSet(NetBoxModelFilterSet):
    sensor = TreeNodeMultipleChoiceFilter(
        queryset=Sensor.objects.all(),
        lookup_expr="in",
        field_name="sensor__name",
        to_field_name="sensor",
        label=_("Sensor (name)"),
    )

    type = TreeNodeMultipleChoiceFilter(
        queryset=TransducerType.objects.all(),
        lookup_expr="in",
        field_name="type__name",
        to_field_name="type",
        label=_("Transducer type (name)"),
    )

    class Meta:
        model = Transducer
        fields = (
            "id",
            "name",
            "sensor",
            "type",
            "unit",
            "customer_id",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(sensor__name__icontains=value)
            | Q(type__name__icontains=value)
            | Q(unit__icontains=value)
            | Q(customer_id__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()


class AttributeMappingFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = AttributeMapping
        fields = ("id", "name", "category", "type", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(type__icontains=value)
            | Q(category__icontains=value)
            | Q(description__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()


class DeviceToolFilterSet(NetBoxModelFilterSet):
    site = TreeNodeMultipleChoiceFilter(
        queryset=Site.objects.all(),
        lookup_expr="in",
        field_name="site__name",
        to_field_name="site",
        label=_("Site (name)"),
    )

    device_type = TreeNodeMultipleChoiceFilter(
        queryset=DeviceType.objects.all(),
        lookup_expr="in",
        field_name="device_type__model",
        to_field_name="device_type",
        label=_("Device type (name)"),
    )

    class Meta:
        model = Device
        fields = ("id", "name", "serial", "device_type", "site")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(device_type__model__icontains=value)
            | Q(site__name__icontains=value)
            | Q(serial__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()
