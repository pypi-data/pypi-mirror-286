from typing import List

from django import forms
from django.forms import CharField, IntegerField, ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from netbox.forms import NetBoxModelForm, NetBoxModelImportForm

from .constants import (
    CATEGORIES_NAME_CHOICES,
    DATATYPE_NAME_CHOICES,
    TRANSDUCERS_NAME_CHOICES,
)
from .models import (
    SENSOR_RANGE_FIELDS,
    AttributeMapping,
    Sensor,
    SensorType,
    Transducer,
    TransducerType,
)


class SensorTypeForm(NetBoxModelForm):
    class Meta:
        model = SensorType
        fields = ["name", "icon", "comments"]


class SensorForm(NetBoxModelForm):
    class Meta:
        model = Sensor
        fields = [
            "name",
            "type",
            "icon",
            "device",
            "customer_id",
            "serial",
            "sensitivity_code",
            "comments",
        ]


class TransducerTypeForm(NetBoxModelForm):
    class Meta:
        model = TransducerType
        fields = [
            "name",
            "sensor_type",
            "dash",
            "unit",
            "safety",
            "description",
        ] + SENSOR_RANGE_FIELDS


class TransducerForm(NetBoxModelForm):
    name = forms.ModelChoiceField(
        queryset=AttributeMapping.objects.filter(category="transducer_type"),
        to_field_name="name",
    )

    class Meta:
        model = Transducer
        fields = [
            "name",
            "type",
            "sensor",
            "icon",
            "dash",
            "unit",
            "safety",
            "longitud",
            "latitud",
            "elevation",
        ] + SENSOR_RANGE_FIELDS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["name"].initial = self.instance.name


class SensorTypeImportForm(NetBoxModelImportForm):
    class Meta:
        model = SensorType
        fields = ("name", "comments")
        help_texts = {
            "time_zone": mark_safe(
                _(
                    'Time zone (<a href="https://en.wikipedia.org/wiki/List'
                    '_of_tz_database_time_zones">available options</a>)'
                )
            )
        }


class TransducerTypeImportForm(NetBoxModelImportForm):
    def clean_name(self):
        """_."""
        name = self.cleaned_data["name"]
        return name

    class Meta:
        model = TransducerType
        fields = (
            "name",
            "dash",
            "unit",
            "safety",
            "description",
            "min_custom",
            "max_custom",
            "min_warning",
            "max_warning",
            "min_critical",
            "max_critical",
        )
        help_texts = {
            "time_zone": mark_safe(
                _(
                    'Time zone (<a href="https://en.wikipedia.org/wiki/List'
                    '_of_tz_database_time_zones">available options</a>)'
                )
            )
        }


class TransducerImportForm(NetBoxModelImportForm):
    type = CharField(
        required=True,
        help_text=_("The name of the transducer type is assigned."),
    )

    sensor = IntegerField(
        required=True,
        help_text=_("The sensor id is assigned."),
    )

    class Meta:
        model = Transducer
        fields = (
            "name",
            "sensor",
            "type",
            "customer_id",
            "dash",
            "longitud",
            "latitud",
            "elevation",
            "unit",
            "safety",
            "min_custom",
            "max_custom",
            "min_warning",
            "max_warning",
            "min_critical",
            "max_critical",
        )
        help_texts = {
            "time_zone": mark_safe(
                _(
                    'Time zone (<a href="https://en.wikipedia.org/wiki/List'
                    '_of_tz_database_time_zones">available options</a>)'
                )
            )
        }

    def clean_type(self) -> List:
        """
        It is validated if the csv transducer types exist.

        Returns
        -------
        existing_types : List
            List of the types of sensors that exist.
        """
        types = self.cleaned_data.get("type", "").strip()
        if "," in types:
            raise ValidationError(
                f"Only one transducer type is allowed to be assigned to a transducer."
            )
        # Validate that the types exist in the database
        existing_types = TransducerType.objects.get(name=types)
        if existing_types:
            return existing_types
        else:
            raise ValidationError(f"Transducer type do not exist: {existing_types}")

    def clean_sensor(self) -> List:
        """
        It is validated if the csv sensor types exist.

        Returns
        -------
        existing_types : List
            List of the types of sensors that exist.
        """
        sensor = self.cleaned_data.get("sensor", "")
        # Validates that no more than one sensor is required for a transducer.
        if "," in str(sensor):
            raise ValidationError(
                f"Only one sensor is allowed to be assigned to one transducer."
            )
        # Validate that the sensor exist in the database
        existing_sensors = Sensor.objects.get(id=sensor)
        if existing_sensors:
            return existing_sensors
        else:
            raise ValidationError(f"Sensor do not exist: {sensor}")

    def save(self, commit=True) -> Sensor:
        """
        It is executed for each row of the csv. If the id exists, it is
        updated, otherwise a new sensor is inserted.

        Parameters
        ----------
        commit : bool

        Returns
        -------
         transducer : Transducer
            Returns the transducer that has been acted upon.
        """
        transducer_id = self.cleaned_data.get("id")
        if transducer_id:
            # If an ID exists, try to get the existing sensor
            transducer = Transducer.objects.filter(id=transducer_id).first()

            if not transducer:
                raise ValidationError(
                    f"Transducer with ID {transducer_id} does not exist."
                )

            for field in self.Meta.fields:
                if field != "id":
                    setattr(
                        transducer,
                        field,
                        self.cleaned_data.get(field, getattr(transducer, field)),
                    )

            if commit:
                transducer.save()

            # Update ManyToMany 'typeTransducer' relationship
            if "type" in self.cleaned_data:
                Transducer.type.set(self.cleaned_data["type"])

            # Update ManyToMany 'Sensor' relationship
            if "sensor" in self.cleaned_data:
                Transducer.sensor.set(self.cleaned_data["sensor"])

        else:
            # If there is no ID, create a new sensor
            transducer = super().save(commit=False)
            if commit:
                transducer.save()

        return transducer


class SensorImportForm(NetBoxModelImportForm):
    type = CharField(
        required=True,
        help_text="Sensor types (comma-separated).",
    )

    class Meta:
        model = Sensor
        fields = (
            "name",
            "type",
            "device",
            "customer_id",
            "serial",
            "icon",
            "comments",
        )

    def clean_type(self) -> List:
        """
        It is validated if the csv sensor types exist.

        Returns
        -------
        existing_types : List
            List of the types of sensors that exist.
        """
        types_csv = self.cleaned_data.get("type", "")
        types = [t.strip() for t in types_csv.split(",") if t.strip()]
        # Validate that the types exist in the database
        existing_types = SensorType.objects.filter(name__in=types)
        non_existing_types = set(types) - set(
            existing_types.values_list("name", flat=True)
        )
        if non_existing_types:
            raise ValidationError(
                f"Sensor types do not exist: {', '.join(non_existing_types)}"
            )
        return existing_types

    def save(self, commit=True) -> Sensor:
        """
        It is executed for each row of the csv. If the id exists, it is
        updated, otherwise a new sensor is inserted.

        Parameters
        ----------
        commit : bool

        Returns
        -------
         sensor : Sensor
            Returns the sensor that has been acted upon.
        """
        sensor_id = self.cleaned_data.get("id")
        if sensor_id:
            # If an ID exists, try to get the existing sensor
            sensor = Sensor.objects.filter(id=sensor_id).first()

            if not sensor:
                raise ValidationError(f"Sensor with ID {sensor_id} does not exist.")

            for field in self.Meta.fields:
                if field != "id":
                    setattr(
                        sensor,
                        field,
                        self.cleaned_data.get(field, getattr(sensor, field)),
                    )

            if commit:
                sensor.save()

            # Update ManyToMany 'type' relationship
            if "type" in self.cleaned_data:
                sensor.type.set(self.cleaned_data["type"])

        else:
            # If there is no ID, create a new sensor
            sensor = super().save(commit=False)
            if commit:
                sensor.save()
            if "type" in self.cleaned_data:
                sensor.type.set(self.cleaned_data["type"])
            if commit:
                sensor.save()

        return sensor


class AttributeMappingForm(NetBoxModelForm):
    type = forms.ChoiceField(choices=DATATYPE_NAME_CHOICES)
    category = forms.ChoiceField(choices=CATEGORIES_NAME_CHOICES)

    class Meta:
        model = AttributeMapping
        fields = ["name", "category", "type", "description"]
