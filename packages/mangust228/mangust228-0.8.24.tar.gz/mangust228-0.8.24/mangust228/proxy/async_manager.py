from httpx import AsyncClient

from ._base import BaseProxyManager
from ._schemas import ProxySchema


class AsyncProxyManager(BaseProxyManager):
    async def start(self): 
        self.client = AsyncClient(
            base_url=self.settings.url,
            headers={
                "X-API-KEY": self.settings.api_key
            })
        self.logger.info("session is opened")
    
    async def close(self):
        await self.client.aclose()
        self.logger.info("session is closed")
    
    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def get(self) -> ProxySchema:
        response = await self.client.get("/proxies/rotations/one", params=self.params)
        self._raise_if_not_200(response)
        return self._new_proxy(response)

    async def free(self, proxy: ProxySchema) -> None:
        response = await self.client.get(f"/proxies/rotations/free/{proxy.id}")
        self._raise_if_not_200(response)
        self.logger.info(f'{proxy} is free')

    async def change_without_error(self, proxy: ProxySchema) -> ProxySchema:
        data = self.data
        data["proxy_id"] = proxy.id
        response = await self.client.put(f"/proxies/rotations", json=data)
        self._raise_if_not_200(response)
        self.logger.info(f'{proxy} changed without error')
        return self._new_proxy(response)

    async def change_with_error(self, proxy: ProxySchema, reason: str) -> ProxySchema:
        data = self.data
        data["proxy_id"] = proxy.id
        data["reason"] = reason
        response = await self.client.patch("/proxies/rotations", json=data)
        self._raise_if_not_200(response)
        self.logger.info(f'{proxy} changed with error')
        return self._new_proxy(response)
