from nonebot_plugin_apscheduler import scheduler
from nonebot.log import logger
from .push import push_to_server
from .config import config
from .servers import get_server_list


@scheduler.scheduled_job("cron", **config.autopush_push_cron)
async def push_status_to_servers():
    servers = get_server_list()
    fail_count = 0
    for server in servers:
        if not await push_to_server(server):
            fail_count += 1
    logger.info(f"向 {len(servers)} 推送状态完成，成功 {len(servers) - fail_count}，失败 {fail_count} ")
