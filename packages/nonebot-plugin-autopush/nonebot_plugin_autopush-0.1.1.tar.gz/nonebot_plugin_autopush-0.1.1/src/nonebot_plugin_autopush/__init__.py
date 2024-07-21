from nonebot.plugin import PluginMetadata
from nonebot import require
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-autopush",
    description="NoneBot2 自动状态推送",
    usage="向指定服务器推送 NoneBot2 状态",
    config=Config,
    type="application",
    homepage="https://github.com/This-is-XiaoDeng/nonebot-plugin-autopush",
    supported_adapters=None
)

require("nonebot_plugin_apscheduler")

from . import __main__
