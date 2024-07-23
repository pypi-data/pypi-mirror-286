from pydantic import BaseModel


class ProxySchema(BaseModel):
    id: int
    server: str
    port: int
    username: str
    password: str
    
    def __str__(self):
        return f"proxy-{self.id}"
    
    @property
    def req_conn(self):
        return {
            "http": f"http://{self.username}:{self.password}@{self.server}:{self.port}",
            "https": f"https://{self.username}:{self.password}@{self.server}:{self.port}"
            }
    
    @property
    def pw_conn(self):
        return {
            "server": f"https://{self.server}:{self.port}",
            "username": self.username,
            "password": self.password
        }
        