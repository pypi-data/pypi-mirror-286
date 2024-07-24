import json
import logging
import time
from typing import Dict

from dcim.models.devices import Device
from dcim.models.sites import Site
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Model
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from sens_platform.constants import (
    IMPORT_AUTO_DEVICE,
    IMPORT_AUTO_SENSOR,
    IMPORT_AUTO_TRANSDUCER,
)
from sens_platform.models import Sensor, Transducer, UserProfile
from sens_platform.platforms.grafana import GrafanaCli
from sens_platform.platforms.influxdb.influxdb import InfluxManagement
from sens_platform.utils.utils import clone_models
from users.models import ObjectPermission


@receiver(pre_save, sender=Site, dispatch_uid="pre_save_id")
def manage_site_in_influxdb(sender: Model, instance: Site, **kwargs: Dict):
    """
    Method that is executed before saving a Site.
    Its function is to manage the association between netbox and influxdb.
    """
    logger = logging.getLogger("netbox.sens_platform")
    try:
        grafana = GrafanaCli()
        _ = grafana.create_grafana(org_name=instance.slug)
    except Exception as ex:
        logger.warning(f"Error creating a new organization in Grafana. Err: {ex}")

    influx = InfluxManagement()
    organization = influx.search_site_organization(instance.slug)
    if organization is None:
        organization = influx.create_organization_in_influx(
            organization=instance.slug, description=instance.description
        )

    if "name" not in organization:
        raise Exception(
            f"Organization has not been created, check connection with influxdb. "
            f"Response: {organization}"
        )

    bucket_data = influx.search_bucket(
        organization=organization["name"], bucket_name="data"
    )
    if bucket_data is None:
        bucket_data = influx.create_bucket_in_organization(
            organization_id=organization["id"], bucket_name="data"
        )

    bucket_status = influx.search_bucket(
        organization=organization["name"], bucket_name="status"
    )
    if bucket_status is None:
        _ = influx.create_bucket_in_organization(
            organization_id=organization["id"], bucket_name="status"
        )
    authorizations = influx.get_authorizations(organization=organization["name"])
    if len(authorizations) > 0:
        for authorization in authorizations:
            if authorization["description"] == f"Authorization: {organization['name']}":
                _ = influx.delete_authorization(authorization["id"])

    authorization = influx.create_an_authorization(
        organization_id=organization["id"],
        organization=instance.slug,
        bucket_id=bucket_data["id"],
    )

    instance.custom_field_data["influxdb_token"] = authorization["token"]

    all_users = UserProfile.objects.all()
    if all_users:
        for user in all_users:
            try:
                web_config = json.loads(user.web_config)
            except json.decoder.JSONDecodeError as e:
                web_config = {}
            if "influx" in web_config:
                if instance.slug in web_config["influx"]:
                    web_config["influx"][instance.slug] = authorization["token"]
                    user.web_config = json.dumps(web_config)
                    user.save()


@receiver(pre_delete, sender=Site, dispatch_uid="pre_delete_site_id")
def manage_site_delete(sender, instance, **kwargs):
    """
    When a site is deleted:
    - User access to site data in influxdb must be deleted.
    - Django permissions to the site must be deleted.
    """
    try:
        with transaction.atomic():
            all_users = UserProfile.objects.all()
            if all_users:
                for user in all_users:
                    try:
                        web_config = json.loads(user.web_config)
                    except json.decoder.JSONDecodeError as e:
                        web_config = {}
                    if "influx" in web_config:
                        if instance.slug in web_config["influx"]:
                            web_config["influx"].pop(instance.slug, None)
                            user.web_config = json.dumps(web_config)
                            user.save()
                    site_permission = ObjectPermission.objects.get(
                        constraints={"site__slug": instance.slug},
                    )
                    if site_permission:
                        user.user.object_permissions.remove(site_permission)
    except Exception as ex:
        print(f"Error deleting the site '{instance.slug}': {ex}")


@receiver(post_save, sender=Site)
def custom_code_after_saving(sender, instance, created, **kwargs):
    if created:
        print("A new Site object was created.")
    else:
        print("An existing Site object was updated.")


@receiver(post_save, sender=Device)
def device_import_handler(sender, instance, created, **kwargs) -> None:
    """
    The import action for the Device model is captured.
    The creation of entities related to the device is automated.
    """

    def _validate_device_structure() -> str | Dict | None:
        """
        This method validates that the device to be used has the correct
        structure to replicate new devices.
        The advantage of prior validation is that there is no need to
        check for possible errors.

        Notes
        -----
        Characteristics of the validation of a device.

        - The device must have at least one sensor.
        - A sensor must have at least one transducer.
        - If a device does not have sensors it does not duplicate the new device.
        - If a sensor does not have a transducer, the new device is not duplicated.

        Returns
        -------
        structure: Dict
            Validated device, contains complete structure.
        void: None
            No device of the specified type was found.
        err: err_device_0
            _.
        err: err_sensor_0
            _.
        err: err_transductor_0
            _.
        err : ObjectDoesNotExist
            Device object doest not exist.
        err : Exception
            Device object doest not exist, None.
        """
        try:
            status: str = ""
            devices_to_validate = Device.objects.filter(
                device_type_id=instance.device_type.id
            )
            if len(devices_to_validate) == 0:
                return "err_device_0"
            for device_to_validate in devices_to_validate:
                sensors_to_validate = Sensor.objects.filter(
                    device_id=device_to_validate.id
                )
                total_sensors = len(sensors_to_validate)
                count_sensors = 0
                backup_transducers = []
                for sensor_to_validate in sensors_to_validate:
                    transducers_to_validate = Transducer.objects.filter(
                        sensor_id=sensor_to_validate.id
                    )
                    if len(transducers_to_validate) > 0:
                        backup_transducers.extend(transducers_to_validate)
                        count_sensors += 1
                    else:
                        status = "err_transductor_0"
                        break
                if total_sensors != 0 and total_sensors == count_sensors:
                    return {
                        "device": device_to_validate,
                        "sensors": sensors_to_validate,
                        "transducers": backup_transducers,
                    }

                else:
                    status = "err_sensor_0"
                    continue
        except ObjectDoesNotExist as _ex:
            return None
        except Exception as _ex:
            return None
        return status

    logger = logging.getLogger("netbox.sens_platform")
    if created:
        structure = _validate_device_structure()
        if structure is None:
            # raise ValueError(_(IMPORT_AUTO_DEVICE))
            logger.debug(IMPORT_AUTO_DEVICE)
        elif structure == "err_device_0":
            # raise ValueError(_(IMPORT_AUTO_DEVICE))
            logger.debug(IMPORT_AUTO_DEVICE)
        elif structure == "err_sensor_0":
            # raise ValueError(_(IMPORT_AUTO_SENSOR))
            logger.debug(IMPORT_AUTO_SENSOR)
        elif structure == "err_transductor_0":
            # raise ValueError(_(IMPORT_AUTO_TRANSDUCER))
            logger.debug(IMPORT_AUTO_TRANSDUCER)
        if isinstance(structure, Dict):
            sensors = Sensor.objects.filter(device_id=structure["device"].id)
            for idx, sensor in enumerate(sensors):
                cloned_sensor = clone_models(
                    model_name="sensor",
                    instance=sensor,
                    fields={
                        "serial": f"CLONED-{time.time()}".replace(".", ""),
                        "device": instance,
                    },
                )
                transducers = Transducer.objects.filter(sensor_id=sensor.id)
                for idy, transducer in enumerate(transducers):
                    transducers_cloned = clone_models(
                        model_name="transducer",
                        instance=transducer,
                        fields={
                            "sensor": cloned_sensor,
                        },
                    )
