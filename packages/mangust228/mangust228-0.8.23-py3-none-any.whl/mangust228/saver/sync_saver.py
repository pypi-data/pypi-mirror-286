import json
import lzma
import os
from typing import Any

from ._base import BaseSaveManager


class SyncSaveManager(BaseSaveManager):
    '''
    File saver

    Example usage:
    ```python
    saver = SyncSaveManager(add_uuid=True)
    path = saver.save_json({"hello": "world"}, 5, 3, "daily")
    print(path)  # "data/2024/05/29/22/5_3_daily.json"
    ```

    Parameters
    ----------
    base_path : str, optional
        The base folder where all files will be saved, by default "data"
    add_uuid : bool, optional
        Option to add a UUID at the end of the file name to ensure unique file names, by default False
    compress : bool, optional
        Option to compress files using lzma when enabled, by default False
    debug : bool, optional
        Enable debug logging, by default False
    '''
    def _save_sync_file(self, content: str, path: str):
        if not self.compress:
            with open(path, "w") as fp:
                fp.write(content)
        else:  # lzma
            compressed_data = lzma.compress(content.encode())
            with open(path, "wb") as compress_fp:
                compress_fp.write(compressed_data)

    def save_json(self, data: dict, *names: Any):
        file_name = self._get_json_file_name(names)
        folder_path = self.folder_path
        os.makedirs(folder_path, exist_ok=True)
        path = folder_path + file_name
        content = json.dumps(data, ensure_ascii=False)
        self._save_sync_file(content, path)
        self.logger.debug(f"success saved: {path}")
        return path

    def save_html(self, content: str, *names: Any):
        file_name = self._get_html_file_name(names)
        folder_path = self.folder_path
        os.makedirs(folder_path, exist_ok=True)
        path = folder_path + file_name
        self._save_sync_file(content, path)
        self.logger.debug(f"success saved: {path}")
        return path
