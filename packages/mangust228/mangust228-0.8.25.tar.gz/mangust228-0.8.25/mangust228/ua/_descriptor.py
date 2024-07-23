from ._exceptions import ExceptionInstance


class BaseDescriptor:
    name = "base"

    def __set__(self, instance: None, owner: type):
        if instance is not None:
            raise ExceptionInstance(owner.__class__.__name__)
        owner.__dict__[self.name] = self  # type: ignore

    def __get__(self, instance: None, owner: type):
        if instance is not None:
            raise ExceptionInstance(owner.__class__.__name__)
