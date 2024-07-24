import json
import logging
from typing import Dict

from dcim.models.devices import Device
from dcim.models.sites import Site
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from netbox.models import NetBoxModel
from sens_platform.constants import ICON_TYPES, PLUGIN_APPLICATION_NAME
from sens_platform.users import ManagementUserGrafana

User = settings.AUTH_USER_MODEL


def link(name: str):
    """
    This method and other model functionality must be implemented in
    models.py or model_utilities.py. model_utilities.py does not exist.
    It is important to avoid cyclic redundancy.

    Parameters
    ----------
    name: str
        Endpoint.
    Returns
    -------
    path: str
        Complete path.
    """
    return f"plugins:{PLUGIN_APPLICATION_NAME}:{name}"


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, related_name="userprofile", on_delete=models.CASCADE
    )
    web_config = models.TextField(
        default="",
        editable=False,
        help_text="Custom user web configuration (dashboards, etc)",
    )

    def __str__(self):
        return str(self.user)

    @staticmethod
    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        def _get_permissions() -> Dict:
            """
            Method designed to obtain the influx tokens assigned to the sites.

            Returns
            -------
            Dict.
                Tokens are influxdb.
            """
            permissions: Dict = {}
            try:
                permissions_site = instance.object_permissions.all()
                for permission in permissions_site:
                    if permission.constraints is not None:
                        if "slug" in permission.constraints:
                            permissions[
                                permission.constraints["slug"]
                            ] = Site.objects.get(
                                slug=permission.constraints["slug"]
                            ).custom_field_data[
                                "influxdb_token"
                            ]
            # except instance.object_permissions.DoesNotExist:
            #     logger = logging.getLogger("netbox.sens_platform")
            #     logger.error(
            #         f"Error obtaining influx token: object_permissions.DoesNotExist"
            #     )
            except Exception as ex:
                logger = logging.getLogger("netbox.sens_platform")
                logger.error(f"Error obtaining influx token: {ex}")
            return permissions

        if created:
            UserProfile.objects.create(user=instance)

        access = _get_permissions()

        try:
            _ = ManagementUserGrafana(
                access=access,
                user={
                    "name": instance.username,
                    "email": instance.email,
                    "login": instance.username,
                    "password": instance.password,
                },
            ).management()
        except Exception as ex:
            logger = logging.getLogger("netbox.sens_platform.models")
            logger.error(
                f"Error creating user in Grafana. Detail: {ex}. User: {instance.username}"
            )

        try:
            web_config = json.loads(instance.userprofile.web_config)
        except json.decoder.JSONDecodeError as e:
            web_config = {}

        web_config["influx"] = access
        instance.userprofile.web_config = json.dumps(web_config)
        instance.userprofile.save()


def RangeValue(verbose_name=None):
    return models.DecimalField(
        verbose_name, max_digits=12, decimal_places=5, blank=True, null=True
    )


SENSOR_RANGE_FIELDS = [
    "min_warning",
    "max_warning",
    "min_critical",
    "max_critical",
    "min_custom",
    "max_custom",
]


class SensorType(NetBoxModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Name", max_length=100, unique=True)
    comments = models.TextField("Comments", blank=True)
    icon = models.CharField(max_length=20, choices=ICON_TYPES, default="device_hub")

    clone_fields = ["name", "icon"]

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(link("sensortype"), args=[self.pk])


class CustomDevice(Device):
    """
    Extend detail of the name of a device, the reason is to be able to
    manage large numbers of devices.
    """

    class Meta:
        proxy = True

    def __str__(self):
        super().__str__()
        return f"{self.name} - ({self.serial} - {self.site.name})"


class Sensor(NetBoxModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Name", max_length=64, blank=False)
    type = models.ManyToManyField(
        to=SensorType,
        related_name="sensor_type",
        blank=False,
    )
    device = models.ForeignKey(
        to=CustomDevice, on_delete=models.PROTECT, help_text="Device ID."
    )
    customer_id = models.CharField(
        "Customer ID", max_length=64, help_text="Identifier that can be repeated."
    )
    serial = models.CharField("Serial nb.", max_length=100, unique=True)
    comments = models.TextField("Comments", blank=True)
    icon = models.CharField(
        max_length=20,
        choices=ICON_TYPES,
        default="device_hub",
        help_text="By default put 'device_hub'.",
    )
    sensitivity_code = models.DecimalField(
        "Sensitivity code",
        max_digits=12,
        decimal_places=5,
        blank=True,
        null=True,
    )

    clone_fields = ["name", "type", "device"]

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.name} ({self.serial} / {self.device.name})"

    def get_absolute_url(self):
        return reverse(link("sensor"), args=[self.pk])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        is_new = not bool(self.pk)
        # on creation, fill empty values with values from sensor type
        if is_new:
            pass


class TransducerType(NetBoxModel):
    name = models.CharField("Name", blank=False, max_length=100, unique=True)
    sensor_type = models.ManyToManyField(
        "SensorType",
        related_name="transducer_sensor_type",
        blank=True,
        default=None,
    )
    dash = models.BooleanField("Dash", default=True, blank=True)
    unit = models.CharField("Unit", max_length=64, blank=True)
    safety = models.CharField("Safety", max_length=64, blank=True)
    description = models.TextField("Description", blank=True)
    min_custom = RangeValue("Min. custom")
    max_custom = RangeValue("Max. custom")
    min_warning = RangeValue("Min. warning")
    max_warning = RangeValue("Max. warning")
    min_critical = RangeValue("Min. critical")
    max_critical = RangeValue("Max. critical")

    clone_fields = ["name", "sensor_type", "unit", "description"] + SENSOR_RANGE_FIELDS

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(link("transducertype"), args=[self.pk])


class Transducer(NetBoxModel):
    name = models.CharField("Name", max_length=64, blank=False)
    sensor = models.ForeignKey(
        "Sensor", on_delete=models.PROTECT, related_name="sensor"
    )
    type = models.ForeignKey(
        "TransducerType",
        default=None,
        on_delete=models.PROTECT,
        related_name="transducer_type",
        help_text="The name of the transducer type is assigned.",
    )
    customer_id = models.CharField(
        "Customer ID", max_length=64, help_text="Customer ID.", blank=True
    )
    alias = models.CharField("Alias", blank=True, max_length=100, default="_")
    dash = models.BooleanField("Dash", default=True)
    longitud = models.DecimalField(
        "longitud", default=0.0, max_digits=9, decimal_places=6, blank=True
    )
    latitud = models.DecimalField(
        "Latitud", default=0.0, max_digits=9, decimal_places=6, blank=True
    )
    elevation = models.DecimalField(
        "Elevation", default=0.0, max_digits=9, decimal_places=2, blank=True
    )
    unit = models.CharField("Unit", max_length=64, blank=True)
    safety = models.CharField("Safety", max_length=64, blank=True)
    min_custom = RangeValue("Min. custom")
    max_custom = RangeValue("Max. custom")
    min_warning = RangeValue("Min. warning")
    max_warning = RangeValue("Max. warning")
    min_critical = RangeValue("Min. critical")
    max_critical = RangeValue("Max. critical")
    icon = models.CharField(max_length=20, choices=ICON_TYPES, default="device_hub")

    class Meta:
        ordering = ("name", "type", "sensor")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(link("transducer"), args=[self.pk])


class DeviceConfiguration(NetBoxModel):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(blank=True, null=True, help_text="Creation date.")
    update_password = models.BooleanField(default=False)
    update_date = models.DateField(blank=True, null=True, help_text="Update date.")
    device = models.ForeignKey(to=CustomDevice, on_delete=models.PROTECT)
    configuration = models.JSONField("Configuration", blank=True, null=True)

    class Meta:
        ordering = ("creation_date",)


class AttributeMapping(NetBoxModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Name", blank=False, max_length=100, unique=True)
    category = models.CharField(
        "Category",
        blank=False,
        default="General",
        max_length=100,
        help_text="Category to classify the attribute.",
    )
    type = models.CharField("Type", blank=False, max_length=30, help_text="Datatype.")
    description = models.TextField("Description", blank=True)

    class Meta:
        ordering = ("name",)
        # permissions = [
        #     ("manage_attributemapping", "Can manage AttributeMapping"),
        # ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(link("attributemapping"), args=[self.pk])
