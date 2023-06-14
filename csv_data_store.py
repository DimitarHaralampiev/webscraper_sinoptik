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
        """
        Retrieve the data from the CSV file.

        Returns:
                The retrieved data.
        """
        try:
            df = pd.read_csv(self.filename)
            if 'Forecast Day' in df.columns:
                # Forecast weather data
                return df.to_dict('records')
            else:
                # Current weather data
                return df.iloc[0].to_dict()
        except Exception as e:
            print(f'Error retrieving data from CSV: {str(e)}')