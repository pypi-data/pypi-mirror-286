'''
### Example:

```python
from proxy_manager import SyncProxyManager, AsyncProxyManager

# Sync version:
with SyncProxyManager() as pm:
    proxy_1: ProxySchema = pm.get()
    proxy_2: ProxySchema = pm.change_with_error(new_proxy, reason="just a test")
    proxy_3: ProxySchema = pm.change_without_error(new_proxy)
    pm.free(proxy_3)  # Free proxy on the server

# Async version:
async with AsyncProxyManager() as pm:
    proxy_1: ProxySchema = await pm.get()
    proxy_2: ProxySchema = await pm.change_with_error(new_proxy, reason="just a test")
    proxy_3: ProxySchema = await pm.change_without_error(new_proxy)
    await pm.free(proxy_3)  # Free proxy on the server
```

### How to use response with different libraries:

```
# 1. For use with requests `req_conn`
response = requests.get("http://example.com", proxies=proxy.req_conn)

# 2. For use with httpx `httpx_conn`
response = httpx.get("http://example.com", proxies=proxy.httpx_conn)

# 3. For use with playwright `pw_conn`
context = await browser.new_context(proxy=proxy.pw_conn)

```

### .env EXAMPLE

```bash 
# required
PROXY_SERVICE_URL=http://255.255.255.255:8000
PROXY_SERVICE_API_KEY=XXXXXXXXXXXXXX
PROXY_SERVICE_SERVICE_NAME=test
PROXY_SERVICE_SERVICE_ID=1 
PROXY_SERVICE_LOCK_TIME=5

# not required
PROXY_SERVICE_LOGIC=linear
PROXY_SERVICE_LOGIC_BASE_TIME=10 
PROXY_SERVICE_IGNORE_HOURS=24
PROXY_SERVICE_TYPE_ID=1 
PROXY_SERVICE_LOCATION_ID=1
```

'''
from ._schemas import ProxySchema
from .async_manager import AsyncProxyManager
from .sync_manager import SyncProxyManager
