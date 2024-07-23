import random


class Browsers:
    @classmethod
    def safari(cls, version):
        return f"Safari/{version}.{random.randint(1, 15)}"

    @classmethod
    def chrome(cls, version):
        return f"Chrome/{version}.0.9999.{random.randint(0, 999)}"

    @classmethod
    def firefox(cls, version):
        return f"Firefox/{version}.0"
