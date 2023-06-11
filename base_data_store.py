from abc import ABC, abstractmethod


class BaseDataStore(ABC):
    """
    Abstract base class for data storage operations.
    """

    @abstractmethod
    def write(self, data):
        """
        Write the data to the data store.

        Args:
            data: The data to be written.
        """
        pass

    @abstractmethod
    def get(self):
        """
        Retrieve the data from the data store.

        Returns:
            The retrieved data.
        """
        pass
