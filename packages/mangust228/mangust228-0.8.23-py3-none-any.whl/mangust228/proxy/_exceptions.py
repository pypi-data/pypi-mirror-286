

class _ProxyManagerException(Exception):
    msg = ""
    def __init__(self, msg:str|None = None):
        super().__init__(msg or self.msg)
                 
class ProxyManagerHttpException(_ProxyManagerException):
    msg = "Proxies exist, but none are available"  
    