import logging
from typing import Dict

from django.core.management.base import BaseCommand
from sens_platform.models import Transducer


class Command(BaseCommand):
    def __init__(self):
        super().__init__()

    def add_arguments(self, parser):
        parser.add_argument("--local_execution", required=False, help="Local execute.")

    def handle(self, *args, **options):
        """_."""
        try:
            logging.getLogger().setLevel(logging.INFO)
            self._run_normalization()
            logging.info("Normalization completed...")
        except Exception as exc:
            logging.exception(exc)

    @staticmethod
    def _run_normalization():
        guia: Dict = {
            "Altitude": "alt",
            "CO₂": "co2",
            "Latitude": "lat",
            "Longitude": "lon",
            "NOx": "nox",
            "P00013-Altitude": "alt",
            "P00013-PM1": "pm1",
            "P00013-PM2.5": "pm2",
            "P00013-PM4": "pm4",
            "P00014-Altitude": "alt",
            "P00014-PM1": "pm1",
            "P00014PM2.5": "pm2",
            "P00014-PM4": "pm4",
            "P00015-PM2.5": "pm2",
            "P00015-PM4": "pm4",
            "PM1": "pm1",
            "PM10": "pm10",
            "PM2.5": "pm2",
            "PM4": "pm4",
            "Relative humidity": "h",
            "Temperature": "t",
            "VOC": "voc",
        }

        transducers = Transducer.objects.all()
        for transducer in transducers:
            if transducer.name in list(guia):
                guia_key = transducer.name
                transducer.name = guia[guia_key]
                transducer.alias = guia_key
                transducer.save()
