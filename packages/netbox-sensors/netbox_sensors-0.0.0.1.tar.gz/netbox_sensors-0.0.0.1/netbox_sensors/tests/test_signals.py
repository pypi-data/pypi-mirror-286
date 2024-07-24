import json
from typing import Dict
from unittest.mock import patch

import django
from django.db import transaction
from django.test import TestCase

django.setup()

from dcim.models.devices import Device, DeviceRole, DeviceType, Manufacturer
from dcim.models.sites import Location, Site
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from sens_platform.models import DeviceConfiguration, UserProfile
from users.models import ObjectPermission


class TestSignals(TestCase):
    def setUp(self) -> None:
        super().setUp()

    @classmethod
    def setUpTestData(cls):
        pass

    def test_device_handler_ok(self):
        """Relationship verification with signals."""
        with transaction.atomic():
            manufacturer = Manufacturer.objects.create(
                name="Manufacturer X", slug="manufacturer-x"
            )
            device_type = DeviceType.objects.create(
                manufacturer=manufacturer, model="Device Type X", slug="device-type-X"
            )
            device_role = DeviceRole.objects.create(
                name="Device Role X", slug="device-role-x", color="ff0000"
            )

            site_x = Site.objects.create(name="Site X", slug="site-x")

            location_x1 = Location(site=site_x, name="Location AX", slug="location-ax")
            location_x1.save()

            device1 = Device.objects.create(
                name="Device 1",
                site=site_x,
                location=location_x1,
                device_type=device_type,
                device_role=device_role,
            )
            device1.delete()
            location_x1.delete()
            site_x.delete()
            device_role.delete()
            device_type.delete()
            manufacturer.delete()

    def test_device_handler_with_configuration(self):
        """Relationship verification with signals and configurations."""
        with transaction.atomic():
            manufacturer = Manufacturer.objects.create(
                name="Manufacturer X", slug="manufacturer-x"
            )
            device_type = DeviceType.objects.create(
                manufacturer=manufacturer, model="Device Type X", slug="device-type-X"
            )
            device_role = DeviceRole.objects.create(
                name="Device Role X", slug="device-role-x", color="ff0000"
            )

            site_x = Site.objects.create(name="Site X", slug="site-x")

            location_x1 = Location(site=site_x, name="Location AX", slug="location-ax")
            location_x1.save()

            device1 = Device.objects.create(
                name="Device 1",
                site=site_x,
                location=location_x1,
                device_type=device_type,
                device_role=device_role,
            )
            assert DeviceConfiguration.objects.filter(device=device1.id) is not None
            assert len(DeviceConfiguration.objects.filter(device=device1.id)) == 1

            DeviceConfiguration.objects.filter(device=device1.id).delete()
            device1.delete()
            location_x1.delete()
            site_x.delete()
            device_role.delete()
            device_type.delete()
            manufacturer.delete()

    @patch("sens_platform.signals.UserProfile.save")
    @patch("sens_platform.signals.UserProfile.objects.all")
    def test_manage_site_delete(self, mock_up, _) -> None:
        """Verify the complete pre-delete event of a site."""
        unique_id = 1001
        result_fake = {"influx": {}}
        site_fake = Site.objects.create(name="Site FAKE", slug="site-fake")
        user_fake = User.objects.create(
            username="user fake",
            first_name="Test",
            last_name="Test",
            email="user@fake.com",
            id=unique_id,
        )
        user_profile = UserProfile(
            id=unique_id,
            user=user_fake,
            web_config=json.dumps({"influx": {"site-fake": "fd6g5fd6g"}}),
        )

        site_permission, create = ObjectPermission.objects.get_or_create(
            name=f"Permiso para ver {site_fake.name}",
            actions=["view"],
            constraints={"site__slug": site_fake.slug},
        )

        content_type = ContentType.objects.get_for_model(Site)
        permission = Permission.objects.get(
            content_type=content_type, codename="view_site"
        )
        user_fake.user_permissions.add(permission)
        user_fake.object_permissions.add(site_permission)
        mock_up.return_value = [user_profile]
        _ = site_fake.delete()
        self.assertIsInstance(json.loads(user_profile.web_config), Dict)
        self.assertEqual(json.loads(user_profile.web_config), result_fake)
        self.assertEqual(len(user_fake.object_permissions.all()), 0)
