
class ExceptionUaRandom(Exception):
    msg = ""

    def __init__(self, msg: str | None = None):
        super().__init__(msg or self.msg)


class ExceptionInstance(ExceptionUaRandom):
    msg = "You couldn't make instance of class "

    def __init__(self, owner_name: str):
        super().__init__(f"{self.msg} {owner_name}")
