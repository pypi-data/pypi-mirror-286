from typing import Dict

import django
from dotenv import load_dotenv

load_dotenv()
django.setup()

from sens_platform.models import Transducer


def auto_max_min():
    # guia: Dict = {
    #     "co2": {"min_critical": 0, "max_critical": 0},
    #     "nox": {"min_critical": 0, "max_critical": 0},
    #     "pm1": {"min_critical": 0, "max_critical": 0},
    #     "pm10": {"min_critical": 0, "max_critical": 0},
    #     "pm2": {"min_critical": 0, "max_critical": 0},
    #     "pm4": {"min_critical": 0, "max_critical": 0},
    #     "h": {"min_critical": 0, "max_critical": 0},
    #     "t": {"min_critical": 0, "max_critical": 0},
    #     "voc": {"min_critical": 0, "max_critical": 0},
    # }
    guia: Dict = {
        "t": {"min_critical": -10, "max_critical": 70},
    }
    control_transducers = list(guia)
    transducers = Transducer.objects.all()
    for transducer in transducers:
        if transducer.name in control_transducers:
            transducer.min_critical = guia[transducer.name]["min_critical"]
            transducer.max_critical = guia[transducer.name]["max_critical"]
            transducer.save()
    pass


if __name__ == "__main__":
    auto_max_min()
