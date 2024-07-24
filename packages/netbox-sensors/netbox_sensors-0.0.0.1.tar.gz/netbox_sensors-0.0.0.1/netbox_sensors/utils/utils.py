import logging
from typing import Dict

from dcim.models.devices import Device
from sens_platform.constants import PLUGIN_APPLICATION_NAME
from sens_platform.models import Sensor, Transducer


def link(name):
    return f"plugins:{PLUGIN_APPLICATION_NAME}:{name}"


def api_link(name):
    return f"plugins-api:{PLUGIN_APPLICATION_NAME}-api:{name}"


def clone_models(model_name: str, instance: object, fields: Dict = None) -> object:
    """
    Method to clone models according to your configuration. Clone models
    automatically.

    Parameters
    ----------
    model_name: str
        Model name.
    instance: object
    fields: Dict or None
        Dictionary where the key is the name of the field and the
        value the value to be assigned.
    Returns
    -------
    model: object
    """
    models: Dict = {
        "device": {
            "model": Device,
            "noFields": ["last_updated", "pk", "id", "comments"],
        },
        "sensor": {
            "model": Sensor,
            "noFields": ["last_updated", "pk", "id", "comments"],
        },
        "transducer": {
            "model": Transducer,
            "noFields": ["last_updated", "pk", "id", "comments"],
        },
    }
    logger = logging.getLogger("netbox.sens_solutions.utils")
    cloned_model = models[model_name]["model"]()
    for field in instance._meta.fields:
        if field.name not in models[model_name]["noFields"]:
            if fields and field.name in list(fields.keys()):
                setattr(cloned_model, field.name, fields[field.name])
            else:
                setattr(cloned_model, field.name, getattr(instance, field.name))
    try:
        cloned_model.save()
    except Exception as ex:
        logger.warning(
            f"Error in the function that clones cascade models. "
            f"This error is serious and affects device cloning."
            f"Detail: {ex}"
        )
    return cloned_model
