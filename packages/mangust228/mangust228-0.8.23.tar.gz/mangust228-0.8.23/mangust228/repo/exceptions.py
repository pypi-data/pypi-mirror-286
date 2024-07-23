class _FactoryException(Exception):
    msg = ""
    def __init__(self):
        super().__init__(self.msg)


class NotInitializedRepo(_FactoryException):
    msg = "\n\nYou need to initialize the repo, like:\n\nasync with Repo() as repo:\n    repo.some_repo.add(data)\n"


class NotInitializedSession(_FactoryException):
    msg = "\n\nForgot to add async_session in Repo:\n\n class Repo(FactoryRepoBase):\n    __session = async_session\n\nProbably, __session is not async_sessionmaker"