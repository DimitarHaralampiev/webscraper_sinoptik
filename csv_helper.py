import pandas as pd

from base_data_store import BaseDataStore


class CSVDataStore(BaseDataStore):
    """
    A helper class for writing data to CSV files.
    """

    def __init__(self, filename):
        self.filename = filename

    def write(self, data):
        """
        Writes the data to a CSV file.
        """
        df = pd.DataFrame(data)
        df.to_csv(self.filename, index=False)

    def get(self):
        pass