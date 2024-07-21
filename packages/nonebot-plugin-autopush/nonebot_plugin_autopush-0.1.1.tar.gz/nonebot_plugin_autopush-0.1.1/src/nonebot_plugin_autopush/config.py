from pydantic import BaseModel
from typing import Optional
from nonebot import get_plugin_config


class ServerConfig(BaseModel):
    url: str
    headers: dict[str, str] = {}
    method: str = "GET"
    data: Optional[str] = None


class Config(BaseModel):
    """Plugin Config Here"""
    autopush_servers: list[str | ServerConfig]
    autopush_proxy: Optional[str] = None
    autopush_success_code: list[int] = [200, 204]
    autopush_push_cron: dict[str, str] = {"minute": "*"}


config = get_plugin_config(Config)
