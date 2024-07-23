from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PROXY_SERVICE_")
    url: str
    api_key: str
    service_name: str
    service_id: int
    lock_time: int
    logic: Literal["linear", "sum_history"] = 'linear'
    logic_base_time: int | None = None
    location_id: int | None = None
    type_id: int | None = None
    ignore_hours: int | None = None
