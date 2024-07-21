from .config import ServerConfig, config


def generate_server_list(servers: list[str | ServerConfig]) -> list[ServerConfig]:
    """
    初始化 Server 列表
    :param servers: 含 str 的原始 Server 列表
    :return: 仅 ServerConfig 的详细 Server 列表
    """
    return [ServerConfig(url=server) if isinstance(server, str) else server for server in servers]


server_list = generate_server_list(config.autopush_servers)


def get_server_list() -> list[ServerConfig]:
    """
    获取 Server 列表
    :return: 仅 ServerConfig 的详细 Server 列表
    """
    return server_list
