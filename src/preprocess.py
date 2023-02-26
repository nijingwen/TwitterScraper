import pandas as pd
from os import walk

class PreProcess:
    def __init__(self) -> None:
        # list of status ids
        self.status_ids = list()

    # keep csv files
    def _get_csv_files_only(self, files: list) -> list:
        res = list()
        for file in files:
            if '.csv' in file: res.append(file)
        return res

    # combine dirpath and filename
    def _create_full_paths(self, dirpath: str, filenames: list) -> list:
        res = list()
        for file in filenames:
            filename = dirpath + '/' + file
            res.append(filename)
        return res

    # read all files recursively from provided root directory provided
    def _read_files_from_root(self, root_path: str) -> list:
        res = list()
        for (dirpath, dirnames, filenames) in walk(root_path):
            cur = self._create_full_paths(dirpath, filenames)
            cur = self._get_csv_files_only(cur)
            res.extend(cur)
        return res


    # merge csv files into one table
    def merge_tables(self, root_path: str) -> None:
        paths = self._read_files_from_root(root_path)

        for path in paths:
            df = pd.read_csv(path)
            self.status_ids.extend(df.status_id.values.tolist())

    
    def get_status_ids(self) -> list:
        return self.status_ids