from abc import ABC, abstractmethod
from typing import Dict


class AbstractApiPlatform(ABC):
    CANONICAL_NAME = "abstract_api_platform"
    _name: str

    def __init__(self, *args, **kwargs) -> None:
        pass

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def get_data(self, *args, **kwargs) -> Dict:
        """
        Method for the operator `get`.

        Returns
        -------
        Dict.
        """
        raise NotImplementedError("`get_data` function not implemented.")

    @abstractmethod
    def post_data(self, *args, **kwargs) -> Dict:
        """
        Method for the operator `post`.

        Returns
        -------
        Dict.
        """
        raise NotImplementedError("`post_data` function not implemented.")

    @abstractmethod
    def put_data(self, *args, **kwargs) -> Dict:
        """
        Method for the operator `put`.

        Returns
        -------
        Dict.
        """
        raise NotImplementedError("`put_data` function not implemented.")

    @abstractmethod
    def delete_data(self, *args, **kwargs) -> bool:
        """
        Method for the operator `delete`.

        Returns
        -------
        bool.
        """
        raise NotImplementedError("`delete_data` function not implemented.")

    @abstractmethod
    def patch_data(self, *args, **kwargs) -> Dict:
        """
        Method for the operator `patch`.

        Returns
        -------
        Dict.
        """
        raise NotImplementedError("`patch_data` function not implemented.")
