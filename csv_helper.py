import pandas as pd


class CSVDataStore:
    """
    A helper class for writing data to CSV files.
    """

    def __init__(self, data, filename):
        self.data = data
        self.filename = filename

    def write_csv(self):
        """
        Writes the data to a CSV file.
        """
        df = pd.DataFrame(self.data)
        df.to_csv(self.filename, index=False)