import traceback

from httpx import AsyncClient
from nonebot import logger

from .config import config, ServerConfig


async def push_to_server(server: ServerConfig) -> bool:
    """
    向服务器推送运行状态
    :param server: 服务器配置
    :return: 执行结果
    """
    async with AsyncClient(proxies=config.autopush_proxy) as client:
        try:
            response = await client.request(server.method, server.url, data=server.data)
        except Exception:
            logger.error(f"向 {server.url} 推送状态时发生错误: {traceback.format_exc()}")
            return False
    if response.status_code not in config.autopush_success_code:
        logger.warning(f"推送到 {server.url} 失败 ({response.status_code}): {response.text}")
        return False
    logger.debug(f"向 {server.url} 推送完成，返回 {response.text} ({response.status_code})")
    return True
