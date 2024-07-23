import httpx

from ._base import BaseProxyManager
from ._schemas import ProxySchema


class SyncProxyManager(BaseProxyManager):
    def start(self): 
        self.client = httpx.Client(
            base_url=self.settings.url,
            headers={
                "X-API-KEY": self.settings.api_key
            })
        self.logger.info("session is opened")
    
    def close(self):
        self.client.close()
        self.logger.info("session is closed")
    
    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get(self) -> ProxySchema:
        response = self.client.get("/proxies/rotations/one", params=self.params)
        self._raise_if_not_200(response)
        return self._new_proxy(response)

    def free(self, proxy: ProxySchema) -> None:
        response = self.client.get(f"/proxies/rotations/free/{proxy.id}")
        self._raise_if_not_200(response)
        self.logger.info(f'{proxy} is free')

    def change_without_error(self, proxy: ProxySchema) -> ProxySchema:
        data = self.data
        data["proxy_id"] = proxy.id
        response = self.client.put(f"/proxies/rotations", json=data)
        self._raise_if_not_200(response)
        self.logger.info(f'{proxy} changed without error')
        return self._new_proxy(response)

    def change_with_error(self, proxy: ProxySchema, reason: str) -> ProxySchema:
        data = self.data
        data["proxy_id"] = proxy.id
        data["reason"] = reason
        response = self.client.patch("/proxies/rotations", json=data)
        self._raise_if_not_200(response)
        self.logger.info(f'{proxy} changed with error')
        return self._new_proxy(response)
