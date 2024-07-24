from typing import Dict

from sens_platform.constants import ENTITIES, SENSOR_TYPE_UNIFICATION


class EntityAdapter:
    """
    Created to adapt import csv to model entities.

    Attributes
    ----------
    _entity_guide : Dict
        Relationship of entities with the adaptation dictionary.
    _data : Dict
        The imported data that is going to be transformed.
    _entity_name : ENTITIES
        Entity to transform.

    """

    _entity_name: ENTITIES = None
    _data: Dict = None
    _entity_guide: Dict = {
        ENTITIES.SENSOR_TYPE: SENSOR_TYPE_UNIFICATION,
        ENTITIES.SENSOR: None,
        ENTITIES.TRANSDUCER_TYPE: None,
        ENTITIES.TRANSDUCER: None,
    }

    def __init__(self, entity_name: ENTITIES, data: Dict) -> None:
        self._data = data
        self._entity_name = entity_name

    def transformation(self) -> Dict:
        alteration: Dict = {}
        for key, value in self._data.items():
            if key in self._entity_guide[self._entity_name]:
                model_key = self._entity_guide[self._entity_name][key]
                alteration[model_key] = value
        return alteration
