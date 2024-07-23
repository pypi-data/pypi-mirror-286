import csv 
import os 
from ._logger import get_logger

class _BaseSyncFileDesciptor:
    def __init__(self, path: str, fields_name: list[str], debug: bool=False):
        self.path = path
        self.fields_name = fields_name
        self._created = False 
        self._data: set[str] = set()
        self.logger = get_logger(self.__class__.__name__, debug)

    def _create_folder(self):
        if not self._created:
            folder_path = "/".join(self.path.split("/")[:-1])
            os.makedirs(folder_path, exist_ok=True)
            if not os.path.exists(self.path):
                with open(self.path, "w") as afp:
                    writer = csv.DictWriter(afp, self.fields_name)
                    writer.writeheader()
        self._created = True 
        self._get_history_from_file()

    def _get_history_from_file(self):
        with open(self.path, "r") as afp: 
            reader = csv.DictReader(afp, self.fields_name)
            afp.readline()
            for row in reader: 
                self._data.add(row["path"])
                
    def is_exist(self, path):
        return path in self._data
    
    def _write_data(self, data):
        if not self._created:
            self._create_folder()
        with open(self.path, "a+") as afp:
            writer = csv.DictWriter(afp, self.fields_name)
            writer.writerow(data)
        self._data.add(data["path"])


class _SuccessSyncFileDesciptor(_BaseSyncFileDesciptor):
    def add(self, path: str):
        data = {self.fields_name[0]:path}
        self._write_data(data)
        self.logger.debug(f'add success path/url: {path}')

class _WrongSyncFileDesciptor(_BaseSyncFileDesciptor):
    def add(self, path: str, exc: str):
        data = {self.fields_name[0]:path, self.fields_name[1]:exc}
        self._write_data(data)
        self.logger.warning(f'add wrong path/url: {path}')


class SyncParsedManager:
    wrong = _WrongSyncFileDesciptor("data/wrong.csv", ["path", "exc"])
    success = _SuccessSyncFileDesciptor("data/success.csv", ["path"])