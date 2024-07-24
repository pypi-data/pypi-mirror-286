from abc import ABC, abstractmethod

from pandas import DataFrame


class AbstractClientPlatform(ABC):
    CANONICAL_NAME = "abstract_cli_platform"
    _name: str

    def __init__(self, *args, **kwargs) -> None:
        pass

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def _connect(self, *args, **kwargs) -> None:
        """
        Connection to platform.

        Returns
        -------
        Void.
        """
        raise NotImplementedError("`_connect` function not implemented.")

    @abstractmethod
    def execute_query(self, *args, **kwargs) -> DataFrame:
        """
        Run the queries and convert the dataset to a pandas dataFrame.

        Returns
        -------
        DataFrame.
        """
        raise NotImplementedError("`execute_query` function not implemented.")
