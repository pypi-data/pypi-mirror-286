import asyncio

import aiocsv
import aiofiles
import aiofiles.os as aos
from ._logger import get_logger

class _BaseAsyncFileDesciptor:
    def __init__(self, path: str, fields_name: list[str], debug:bool=False):
        self.path = path
        self.logger = get_logger(self.__class__.__name__, debug)
        self.fields_name = fields_name
        self._created = False 
        self._lock = asyncio.Lock()
        self._data: set[str] = set()

    async def _create_folder(self):
        async with self._lock:
            if not self._created:
                folder_path = "/".join(self.path.split("/")[:-1])
                await aos.makedirs(folder_path, exist_ok=True)
                if not await aos.path.exists(self.path):
                    async with aiofiles.open(self.path, "w") as afp:
                        writer = aiocsv.AsyncDictWriter(afp, self.fields_name)
                        await writer.writeheader()
            self._created = True 
            await self._get_history_from_file()

    async def _get_history_from_file(self):
        async with aiofiles.open(self.path, "r") as afp: 
            reader = aiocsv.AsyncDictReader(afp, self.fields_name)
            await afp.readline()
            async for row in reader: 
                self._data.add(row["path"])
                
    def is_exist(self, path):
        return path in self._data
    
    async def _write_data(self, data):
        if not self._created:
            await self._create_folder()
        async with aiofiles.open(self.path, "a+") as afp:
            writer = aiocsv.AsyncDictWriter(afp, self.fields_name)
            await writer.writerow(data)
        path = data["path"]
        self._data.add(path)
        return path 


class _SuccessAsyncFileDesciptor(_BaseAsyncFileDesciptor):
    async def add(self, path: str):
        data = {self.fields_name[0]:path}
        path = await self._write_data(data)
        self.logger.debug(f'add success path/url: {path}')

class _WrongAsyncFileDesciptor(_BaseAsyncFileDesciptor):
    async def add(self, path: str, exc: str):
        data = {self.fields_name[0]:path, self.fields_name[1]:exc}
        path = await self._write_data(data)
        self.logger.warning(f'add wrong path/url: {path}')

class AsyncParsedManager:
    wrong = _WrongAsyncFileDesciptor("data/wrong.csv", ["path", "exc"])
    success = _SuccessAsyncFileDesciptor("data/success.csv", ["path"])