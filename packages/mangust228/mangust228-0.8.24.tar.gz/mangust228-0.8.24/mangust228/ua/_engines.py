import random
from typing import Type

from ._descriptor import BaseDescriptor


class _Chrome(BaseDescriptor):
    name = "chrome"

    def __get__(self, instance: None, owner: Type):
        super().__get__(instance, owner)
        version = random.randint(99, 125)
        return version, f"AppleWebKit/537.{random.randint(11, 75)} (KHTML, like Gecko)"


class _Safari(BaseDescriptor):
    name = "safari"

    def __get__(self, instance: None, owner: Type):
        super().__get__(instance, owner)
        version = random.randint(10, 16)
        return version, f"AppleWebKit/{random.randint(601, 605)}/{random.randint(1, 8)}/{random.randint(1, 50)} (KHTML, like Gecko)"


class _Firefox(BaseDescriptor):
    name = "firefox"

    def __get__(self, instance: None, owner: Type):
        super().__get__(instance, owner)
        version = random.randint(99, 120)
        if random.choice([True, False]):
            return version, "Gecko/20100101"
        return version, f"Gecko/{version}"


class Engines:
    chrome = _Chrome()
    safari = _Safari()
    firefox = _Firefox()
