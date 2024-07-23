from types import TracebackType
from typing import Any, Optional
from sqlalchemy.orm import Session, sessionmaker
from ._logger import get_logger
from .exceptions import NotInitializedRepo

class _LazyRepo:
    def __init__(self, repo_class: type):
        '''
        Descriptor class for lazy initialization of repositories.
        '''
        self.repo_class = repo_class

    def __set_name__(self, owner: type["SyncBaseRepoFactory"], name: str):
        self.attr_name = name

    def __get__(self, instance: "SyncBaseRepoFactory", owner: type["SyncBaseRepoFactory"]):
        if instance is None:
            raise NotInitializedRepo
        if self.attr_name not in instance.__dict__:
            instance.__dict__[self.attr_name] = self.repo_class(instance._session)
        return instance.__dict__[self.attr_name]

class _FactoryMeta(type):
    '''
    Metaclass to automatically initialize _LazyRepo descriptors based on class annotations.
    '''
    def __new__(cls, name: str, bases: tuple[type, ...], dct: dict):
        annotations: dict = dct.get("__annotations__", {})
        if annotations:
            repos = {k: v for k, v in annotations.items()}
            for repo_name, repo_class in repos.items():
                dct[repo_name] = _LazyRepo(repo_class)
        return super().__new__(cls, name, bases, dct)

class SyncBaseRepoFactory(metaclass=_FactoryMeta):
    '''
    Factory base class to manage repository instances and transactions.
    Example usage:
    ```python
    from connection import session
    class Repo(SyncBaseRepoFactory):
        session = session
        user: UserRepo
    with Repo() as repo:
        repo.user.add(data)
    with Repo(commit=False) as repo:
        user = repo.user.find({"id": 1})
    ```
    '''
    session: sessionmaker[Session]

    def __init__(self, commit: bool = True, debug: bool = False, **kwargs: Any):
        '''
        Initialize the factory with a session and optional commit control.
        :param commit: Whether to commit changes automatically (default: True).
        :param debug: Enable debug logging (default: False).
        :param kwargs: Additional arguments for session configuration.
        '''
        self._session = self.session(**kwargs)
        self.commit = commit
        self.logger = get_logger(self.__class__.__name__, debug)

    def __enter__(self):
        return self

    def __exit__(
            self,
            exc_type: Optional[type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType]) -> Optional[bool]:
        try:
            if not exc_type:
                if self.commit:
                    self._session.commit()
                    self.logger.debug("changes commit")
            else:
                self._session.rollback()
                self.logger.exception("Exception occurred")
        finally:
            self._session.close()
        return None