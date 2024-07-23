'''
**Description:** Module to easily create standard repositories with CRUD operations.

Example to use:
```python
from mangust228.utils.repo import AsyncBaseRepo, AsyncBaseRepoFactory

# Note the inheritance in the class! It's important for correct hinting.
class UserRepo(AsyncBaseRepo[UserModel]):
    model = UserModel

class Repository(AsyncBaseRepoFactory):
    session = session_maker
    # CAUTION: Use only annotation
    user: UserRepo 
    another_repo: AnotherRepo

async with Repository() as repo:
    user = await repo.user.add(name="Ivan", surname="Ivanov")
    user_id = user.id 
    await repo.user.count(surname="Ivanov")
    await repo.user.update_by_id(user_id, name="Sergey")
    await repo.user.get_one_or_none(surname="Ivanov")
    ...
```
'''

from .base_async_repo import AsyncBaseRepo
from .factory_async_repo import AsyncBaseRepoFactory
from .base_sync_repo import SyncBaseRepo
from .factory_sync_repo import SyncBaseRepoFactory