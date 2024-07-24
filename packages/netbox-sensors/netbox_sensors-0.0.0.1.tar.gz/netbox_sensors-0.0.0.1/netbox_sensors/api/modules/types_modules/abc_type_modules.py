import re
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Union


class AbstractTypeModules(ABC):
    CANONICAL_NAME = "abstract_modules"
    _name: str
    _location: str
    _dates: Dict
    _setting: Dict
    _dimension: str
    _slug: str
    _time_window: Union[str, int, bool]
    _device: Union[List[str], None]
    _transducer: Union[List[str], None]

    def __init__(
        self,
        slug: str,
        location: str,
        dates: Dict,
        time_window: Union[str, int, bool] = 15,
        device: List[str] = None,
        transducer: List[str] = None,
        dimension: str = None,
    ) -> None:
        self._slug = slug
        self._dates = dates
        self._dimension = dimension
        self._location = (
            location if location is not None and location != "Null" else None
        )
        self._device = device if device is not None and device != "Null" else None
        self._device = self._adapt_multi_selection(device)
        self._transducer = (
            transducer if transducer is not None and transducer != "Null" else None
        )
        self._transducer = self._adapt_multi_selection(transducer)
        self._add_gps_to_transducers()
        if time_window == "0" or time_window == 0:
            self._time_window = False
        else:
            self._time_window = time_window if time_window else 15

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def execute(self, *args, **kwargs) -> Union[List[Dict], Dict]:
        raise NotImplementedError("`execute` function not implemented.")

    @abstractmethod
    def _generate_settings(self, *args, **kwargs) -> None:
        """
        It generates the necessary configuration, according to the slug
        of the site.

        Returns
        -------
        Void.
        """
        raise NotImplementedError("`_generate_settings` function not implemented.")

    @abstractmethod
    def _to_dict(self, *args, **kwargs) -> Union[List[Dict], Dict]:
        """
        Converts the dataframe to the structure that the
        dashboard expects.

        Parameters
        ----------
        data: DataFrame
            Result of processing.

        Returns
        -------
        Union[Dict, LIst]
            Transformed data structure.
        """
        raise NotImplementedError("`_to_dict` function not implemented.")

    @abstractmethod
    def _generate_data(self, *args, **kwargs) -> Union[List[Dict], Dict]:
        """
        Processes the data according to the generated configuration.

        Returns
        -------
        data: List[Dict]
        """
        raise NotImplementedError("`_generate_data` function not implemented.")

    @staticmethod
    def _adapter_date(dates: Dict):
        formatted_start = datetime.strptime(
            dates["start"], "%Y-%m-%dT%H:%M:%S.%fZ"
        ).strftime("%Y-%m-%dT%H:%M:%SZ")
        formatted_end = datetime.strptime(
            dates["end"], "%Y-%m-%dT%H:%M:%S.%fZ"
        ).strftime("%Y-%m-%dT%H:%M:%SZ")
        return f"start: {formatted_start}, stop: {formatted_end}"

    @staticmethod
    def _adapt_multi_selection(selected) -> Union[List, None]:
        """Method to adapt multiselection in grafana to the abstraction of the models."""
        if isinstance(selected, str):
            if selected == "Null":
                return None
            else:
                patron = r"^\{[^}]+\}$"
                if re.match(patron, selected):
                    return [item.strip() for item in selected[1:-1].split(",")]
                else:
                    return [selected]
        return None

    def _add_gps_to_transducers(self) -> None:
        if isinstance(self._transducer, List):
            self._transducer.append("lat")
            self._transducer.append("lon")
