from django.contrib.auth.models import Group, User
from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from rest_framework import serializers
from sens_platform.models import (
    SENSOR_RANGE_FIELDS,
    AttributeMapping,
    Sensor,
    SensorType,
    Transducer,
    TransducerType,
    UserProfile,
)
from sens_platform.utils.utils import api_link


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")

    class Meta:
        model = UserProfile
        fields = ("username", "web_config")
        depth = 1


class InlineUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("web_config",)
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    userprofile = InlineUserProfileSerializer()

    class Meta:
        model = User
        ref_name = "SensUser"
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_superuser",
            "is_staff",
            "userprofile",
        )


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ("url", "name")


class SensorTypeSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name=api_link("sensortype-detail"))

    class Meta:
        model = SensorType
        fields = ["id", "url", "name", "icon"]


class NestedTransducerTypeSerializer(WritableNestedSerializer):
    class Meta:
        model = TransducerType
        fields = [
            "id",
            "name",
            "dash",
            "unit",
            "min_custom",
            "max_custom",
            "min_warning",
            "max_warning",
            "min_critical",
            "max_critical",
        ]


class NestedSensorTypeSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name=api_link("sensortype-detail"))
    transducer_sensor_type = NestedTransducerTypeSerializer(many=True)

    class Meta:
        model = SensorType
        fields = ["id", "url", "name", "icon", "transducer_sensor_type"]


class NestedTransducerSerializer(WritableNestedSerializer):
    class Meta:
        model = Transducer
        fields = [
            "id",
            "name",
            "dash",
            "unit",
            "longitud",
            "latitud",
            "elevation",
            "min_custom",
            "max_custom",
            "min_warning",
            "max_warning",
            "min_critical",
            "max_critical",
            "icon",
        ]


class NestedAttributeMappingSerializer(WritableNestedSerializer):
    class Meta:
        model = AttributeMapping
        fields = [
            "id",
            "name",
            "type",
            "category",
            "description",
        ]


class SensorSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name=api_link("sensor-detail"))
    type = NestedSensorTypeSerializer(many=True)
    sensor = NestedTransducerSerializer(many=True)
    device_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Sensor
        fields = [
            "id",
            "url",
            "name",
            "icon",
            "type",
            "sensor",
            "device_id",
            "customer_id",
            "serial",
            "custom_fields",
        ]


class TransducerTypeSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name=api_link("transducertype-detail")
    )

    class Meta:
        model = TransducerType
        fields = [
            "id",
            "url",
            "name",
            "sensor_type",
            "dash",
            "unit",
        ] + SENSOR_RANGE_FIELDS


class TransducerSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name=api_link("transducer-detail"))

    class Meta:
        model = Transducer
        fields = [
            "id",
            "url",
            "name",
            "type",
            "sensor",
            "dash",
            "unit",
        ] + SENSOR_RANGE_FIELDS


class AttributeMappingSerializer(NetBoxModelSerializer):
    class Meta:
        model = AttributeMapping
        fields = ["id", "name", "type", "category", "description"]
