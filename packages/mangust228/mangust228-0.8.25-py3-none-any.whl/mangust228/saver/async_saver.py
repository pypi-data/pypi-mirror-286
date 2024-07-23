import json
import lzma
from typing import Any

import aiofiles
import aiofiles.os as aos

from ._base import BaseSaveManager


class AsyncSaveManager(BaseSaveManager):
    '''
    File saver

    Example usage:
    ```python
    saver = AsyncSaveManager(base_path="example", compress=True)
    path = await saver.save_html("this is content", "seller_id", 4, 5)
    print(path)  # "example/2024/05/29/22/seller_id_4_5.html.xz"
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
    async def _save_async_file(self, content: str, path: str):
        if not self.compress:
            async with aiofiles.open(path, "w") as fp:
                await fp.write(content)
        else:  # lzma
            compressed_data = lzma.compress(content.encode())
            async with aiofiles.open(path, "wb") as compress_fp:
                await compress_fp.write(compressed_data)

    async def save_json(self, data: dict, *names: Any) -> str:
        file_name = self._get_json_file_name(names)
        content = json.dumps(data, ensure_ascii=False)
        folder_path = self.folder_path
        await aos.makedirs(folder_path, exist_ok=True)
        path = folder_path + file_name
        await self._save_async_file(content, path)
        self.logger.debug(f"success saved: {path}")
        return path

    async def save_html(self, content, *names: Any) -> str:
        file_name = self._get_html_file_name(names)
        folder_path = self.folder_path
        await aos.makedirs(folder_path, exist_ok=True)
        path = folder_path + file_name
        await self._save_async_file(content, path)
        self.logger.debug(f"success saved: {path}")
        return path



