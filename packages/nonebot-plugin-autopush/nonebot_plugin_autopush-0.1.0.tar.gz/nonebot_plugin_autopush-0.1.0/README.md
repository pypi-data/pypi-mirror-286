<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-autopush

_✨ NoneBot 插件简单描述 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/This-is-XiaoDeng/nonebot-plugin-autopush.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-autopush">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-autopush.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>

## 📖 介绍

这里是插件的详细介绍部分

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-autopush

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-autopush
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-autopush
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-autopush
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-autopush
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_autopush"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

|           配置项           |                类型                | 必填  |        默认值        |           说明           |
|:-----------------------:|:--------------------------------:|:---:|:-----------------:|:----------------------:|
|   `AUTOPUSH_SERVERS`    | `list[Union[str, ServerConfig]]` |  是  |         无         |       Server 列表        |
|    `AUTOPUSH_PROXY`     |         `Optional[str]`          |  否  |      `None`       |     请求 URL 时使用的代理      |
| `AUTOPUSH_SUCCESS_CODE` |           `list[int]`            |  否  |   `[200, 204]`    |       推送成功时的状态码        |
|  `AUTOPUSH_PUSH_CRON`   |         `dict[str, str]`         |  否  | `{"minute": "*"}` | 推送间隔（Apscheduler 任务参数） |

### `ServerConfig`

```python
class ServerConfig(BaseModel):
    url: str
    headers: dict[str, str] = {}
    method: str = "GET"
    data: Optional[str] = None
```

## 🎉 使用

无指令和效果图
