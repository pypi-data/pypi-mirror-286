

class _BaseSaverException(Exception):
    msg = ""

    def __init__(self, msg: str | None = None):
        super().__init__(msg or self.msg)


class ExcExpectedNamesArguments(_BaseSaverException):
    msg = "Expected names for file, got nothing"
