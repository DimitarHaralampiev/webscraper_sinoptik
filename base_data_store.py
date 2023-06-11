from abc import ABC, abstractmethod


class BaseDataStore(ABC):
    """
    Abstract base class for data storage operations.
    """

    @abstractmethod
    def write(self):
        """
        Write data to the storage.
        """
        pass

    @abstractmethod
    def get(self):
        """
        Retrieve data from the storage.
        """
        pass

    def put(self, data):
        """
        Store data in memory.
        """
        pass
