import pandas as pd

class PreProcess:
    def __init__(self) -> None:
        # list of status ids
        self.status_ids = list()

    # merge csv files into one table
    def merge_tables(self, paths: list) -> None:
        for path in paths:
            df = pd.read_csv(path)
            self.status_ids.extend(df.status_id.values.tolist())
            print(len(self.status_ids))

    
    def get_status_ids(self) -> list:
        return self.status_ids