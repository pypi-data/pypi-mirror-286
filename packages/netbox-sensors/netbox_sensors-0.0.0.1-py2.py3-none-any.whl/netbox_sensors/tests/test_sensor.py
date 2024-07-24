from dcim.models import Device, DeviceRole, DeviceType, Location, Manufacturer, Site
from django.test import TestCase
from sens_platform.models import Sensor, SensorType


class SensorTestCase(TestCase):
    def setUp(self):
        manufacturer = Manufacturer.objects.create(
            name="Manufacturer 1", slug="manufacturer-1"
        )
        device_type = DeviceType.objects.create(
            manufacturer=manufacturer, model="Device Type 1", slug="device-type-1"
        )
        device_role = DeviceRole.objects.create(
            name="Device Role 1", slug="device-role-1", color="ff0000"
        )

        site_a = Site.objects.create(name="Site A", slug="site-a")

        location_a1 = Location(site=site_a, name="Location A1", slug="location-a1")
        location_a1.save()

        self.device = Device.objects.create(
            site=site_a,
            location=location_a1,
            name="Device 1",
            device_type=device_type,
            device_role=device_role,
        )

        self.co2 = SensorType.objects.create(name="CO2", unit="ppm")
        Sensor.objects.create(name="CO2 Oncology", type=self.co2, device=self.device)

    def test_sensors_exist(self) -> None:
        """Sensors are properly registered"""
        co2 = Sensor.objects.get(name="CO2 Oncology")
        self.assertEqual(co2.name, "CO2 Oncology")

    def test_sensor_delete(self) -> None:
        """Straw."""
        Sensor.objects.create(name="CO2 Cirurgy", type=self.co2, device=self.device)
        sensor = Sensor.objects.get(name="CO2 Cirurgy")
        self.assertEqual(sensor.name, "CO2 Cirurgy")
        sensor.delete()
        self.assertIsNone(sensor.pk)
