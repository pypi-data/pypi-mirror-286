from httpx import Response as HttpxResponse

from ._config import Settings
from ._exceptions import ProxyManagerHttpException
from ._logger import get_logger
from ._schemas import ProxySchema


class BaseProxyManager:
    '''How to use: 
    '''
    def __init__(self, debug:bool=False, **config):
        '''
        Could be next variables in kwargs: 
            url: str
            api_key: str
            service_name: str 
            service_id: int 
            lock_time: int 
            logic: Literal["linear", "sum_history"]
            type_id: int 
            location_id: int 
            ignore_hours: int 
        '''
        self.settings = Settings(**config)
        self.logger = get_logger(self.__class__.__name__, debug)
        self._create_params()
        self._create_data()

    def _create_params(self):
        self._params = {
            "parsed_service": self.settings.service_name,
            "parsed_service_id": self.settings.service_id,
            "lock_time": self.settings.lock_time,
        }
        if (item := self.settings.location_id):
            self._params["location_id"] = item
        if (item := self.settings.type_id):
            self._params["type_id"] = item

    def _create_data(self):
        self._data = self.params
        if (item := self.settings.logic):
            self._data["logic"] = item
        if (item := self.settings.lock_time):
            self._data["lock_time"] = item
        if (item := self.settings.ignore_hours):
            self._data["ignore_hours"] = item
    
    @staticmethod
    def _raise_if_not_200(response: HttpxResponse) -> None:
        try:
            response.raise_for_status()
        except: 
            raise ProxyManagerHttpException(response.json())


    @property
    def params(self) -> dict:
        return self._params.copy()

    @property
    def data(self) -> dict:
        return self._data.copy()

    def _new_proxy(self, response: HttpxResponse) -> ProxySchema:
        data = response.json()
        proxy = ProxySchema(**data)
        self.logger.debug(f"get new {proxy}")
        return proxy
