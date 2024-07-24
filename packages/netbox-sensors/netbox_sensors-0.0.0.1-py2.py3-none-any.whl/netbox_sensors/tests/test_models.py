import django
from django.db.models import signals
from django.test import TestCase

django.setup()
from dcim.models import Device, DeviceRole, DeviceType, Location, Manufacturer, Site
from sens_platform.models import Sensor, SensorType, Transducer, TransducerType


class TransducerTypeTest(TestCase):
    def test_create_transducer_type(self):
        """Verify the creation of the model and its relationship."""
        sensor_type = SensorType.objects.create(name="Carbon dioxide (CO2)", unit="ppm")

        transducer_type = TransducerType(
            name="CH4",
            sensor_type=sensor_type,
            dash=True,
            unit="ppm",
            max_custom=20,
            max_warning=30,
            max_critical=40,
        )
        transducer_type.save()
        self.assertEqual(transducer_type.name, "CH4")
        self.assertEqual(transducer_type.sensor_type.name, "Carbon dioxide (CO2)")


class TransducerTest(TestCase):
    def test_create_transducer(self):
        """Verify model creation."""
        signals.pre_save.disconnect(sender=Site, dispatch_uid="pre_save_id")
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
        location = Location(site=site_a, name="Location A1", slug="location-a1")
        location.save()
        device = Device.objects.create(
            site=site_a,
            location=location,
            name="Device 1",
            device_type=device_type,
            device_role=device_role,
        )
        sensor_type = SensorType.objects.create(name="Carbon dioxide (CO2)", unit="ppm")
        sensor = Sensor.objects.create(
            name="Methane (CH4)", type=sensor_type, device=device
        )
        transducer_type = TransducerType(
            name="CH4",
            sensor_type=sensor_type,
            dash=True,
            unit="ppm",
            max_custom=20,
            max_warning=30,
            max_critical=40,
        )
        transducer_type.save()
        transducer = Transducer(
            sensor=sensor,
            type=transducer_type,
            name="CH4",
            dash=True,
            latitud=40.714,
            longitud=-74.006,
            elevation=10,
            unit="ppm",
            max_custom=20,
            max_warning=30,
            max_critical=40,
        )
        transducer.save()

        self.assertEqual(transducer.name, "CH4")
