import django
from django.test import TestCase

django.setup()
from sens_platform.models import SensorType


class SensorTypeTestCase(TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self) -> None:
        pass

    def test_sensor_types_exist(self) -> None:
        """Sensor types are properly registered."""
        SensorType.objects.create(name="CO2 TEMP")
        co2 = SensorType.objects.get(name="CO2 TEMP")
        self.assertEqual(co2.name, "CO2 TEMP")
        SensorType.objects.get(name="CO2 TEMP").delete()

        SensorType.objects.create(name="PM01 TEMP")
        pm01 = SensorType.objects.get(name="PM01 TEMP")
        self.assertEqual(pm01.name, "PM01 TEMP")
        SensorType.objects.get(name="PM01 TEMP").delete()

    def test_sensor_type_delete(self) -> None:
        """Straw."""
        SensorType.objects.create(name="Humidity TEMP")
        sensor_type = SensorType.objects.get(name="Humidity TEMP")
        self.assertEqual(sensor_type.name, "Humidity TEMP")
        sensor_type.delete()
        self.assertIsNone(sensor_type.pk)
