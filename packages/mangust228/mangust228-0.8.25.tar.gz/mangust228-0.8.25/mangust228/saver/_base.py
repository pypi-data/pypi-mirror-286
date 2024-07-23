from datetime import datetime
from nanoid import non_secure_generate

from ._exceptions import ExcExpectedNamesArguments
from ._logger import get_logger


class BaseSaveManager:
    def __init__(self, base_path: str = "data", add_uuid: bool = False, compress: bool = False, debug: bool= False):
        base_path = base_path.rstrip("/")
        self.base_path = base_path
        self.add_uuid = add_uuid
        self.compress = compress
        self.logger = get_logger(self.__class__.__name__, debug)

    @property
    def date_path(self):
        return datetime.now().strftime("/%Y/%m/%d/%H/")

    @property
    def folder_path(self):
        return self.base_path + self.date_path

    @property
    def uuid(self):
        if self.add_uuid:
            return "_" + str(non_secure_generate(size=10))
        return ''

    def _get_json_file_name(self, names: tuple):
        path = self._get_name_from_name(names) + ".json"
        return f"{path}.xz" if self.compress else path

    def _get_html_file_name(self, names: tuple):
        path = self._get_name_from_name(names) + ".html"
        return f"{path}.xz" if self.compress else path

    def _get_name_from_name(self, names: tuple):
        if len(names) == 0:
            raise ExcExpectedNamesArguments
        return "_".join([str(n) for n in names]) + self.uuid
