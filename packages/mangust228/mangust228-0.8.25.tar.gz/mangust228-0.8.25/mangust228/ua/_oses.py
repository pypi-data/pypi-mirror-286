import random

from ._descriptor import BaseDescriptor

OS_VERSIONS = {
    "chrome": [
        ("Windows NT 10.0; Win64; x64", .5),
        ("Windows NT 10.0", .3),
        ("Windows NT 6.1", .2),
        ("Macintosh; Intel Mac OS X 10_15_7", .2),
        ("X11; Ubuntu; Linux x86_64", .1),
        ("Windows NT 6.1; WOW64; Trident/7.0; AS", .3)
    ],
    "firefox": [
        ("Windows NT 10.0; Win64; x64", .3),
        ("Windows NT 10.0", .2),
        ("Windows NT 6.1", .3),
        ("X11; Ubuntu; Linux x86_64", .4),
        ("Windows NT 6.1; WOW64; Trident/7.0; AS", .3),
    ],
    "safari": [
        ("Macintosh; Intel Mac OS X 10_15_7", .5),
        ("Macintosh; Intel Mac OS X 10.15", .5)
    ]

}


class _BaseOs(BaseDescriptor):
    lst = []
    weight = []

    def __get__(self, instance: None, owner: type):
        super().__get__(instance, owner)
        return random.choices(self.lst, weights=self.weight)[0]


class _ChromeOs(_BaseOs):
    name = "chrome"
    lst = [i[0] for i in OS_VERSIONS["chrome"]]
    weight = [i[1] for i in OS_VERSIONS["chrome"]]


class _FirefoxOs(_BaseOs):
    name = "firefox"
    lst = [i[0] for i in OS_VERSIONS["firefox"]]
    weight = [i[1] for i in OS_VERSIONS["firefox"]]


class _SafariOs(_BaseOs):
    name = "safari"
    lst = [i[0] for i in OS_VERSIONS["safari"]]
    weight = [i[1] for i in OS_VERSIONS["safari"]]


class Oses:
    chrome = _ChromeOs()
    firefox = _FirefoxOs()
    safari = _SafariOs()
