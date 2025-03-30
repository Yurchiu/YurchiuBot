from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import require
require("nonebot_plugin_txt2img")
from nonebot_plugin_txt2img import Txt2Img
import nonebot
from .config import Config
from nonebot.adapters.onebot.v11 import MessageSegment

__plugin_meta__ = PluginMetadata(
    name="helper",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

def set_txt2img(title, text, size):
    txt2img = Txt2Img()
    txt2img.set_font_size(size)
    pic = txt2img.draw(title, text)
    return pic

help = nonebot.on_command("help", aliases={"帮助"}, block=True)

@help.handle()
async def handle_help():
    title = "HELP 指令列表"
    text = f"""- 单指令
    /help /一言 /色图|涩图 [emoji]+[emoji]
- 复杂指令
    @ /wordle [-l] [-d]：开始一局 wordle 游戏。-l 指定长度 -d 指定词典 【支持词典：GRE、考研、GMAT、专四、TOEFL、SAT、专八、IELTS、CET4、CET6】
    /calc [int|帮助 [int]|结束]：开始一局计算器游戏。
    /支付宝到账 <int>：发送到账语音
    /改名 <str>：修改机器人群名片
    /run <str1> \\n <str2>：运行代码，代码语言为 str1，代码为 str2
    /帮选|选择|挑一个|帮我选 <list>：以空格分隔，随机选择
    /语录 [合订本] [@|删除 <int>]：随机输出来自本群的语录。@ 某人获得某人的语录。如果未发送语录表示不支持此类语录或图片过期。可删除指定编号语录
    柚子瓣相关：请使用命令 【p 帮助】 查看帮助信息
    舞萌相关：请使用命令 【/帮助maimaiDX】 查看帮助信息
    VV 表情包相关：请使用命令 【/vv -h】 查看帮助信息
    [角色名]说[内容]：AI 语音
        /vocu.list|角色列表：列出角色列表
- 交互指令
    /表情包制作：根据接下来的提示制作表情包
        /表情详情 <表情名/关键词>
        /表情搜索 <关键词>
    /pjsk：接下来根据提示 生成 pjsk 表情包；使用 /pjsk -h 查看帮助
    /音乐解析：接下来根据提示 网易云音乐解析
- 回复指令：
    /撤回|revoke：撤回 Bot 此消息
    /语录：此消息进入语录库
- 注意
    At Bot 时 Bot 会回复。
    Bot 2 秒内不会发送同样的信息。
    <> 表示必选参数，[] 表示可选参数。

by 柚初 Yurchiu Rin"""

    font_size = 36
    pic = set_txt2img(title, text, font_size)
    await help.send(MessageSegment.image(pic))
    await help.finish(f"项目地址：https://github.com/Yurchiu/YurchiuBot")




shelp = nonebot.on_command("shelp", aliases={"管理员帮助"}, block=True)

@shelp.handle()
async def handle_shelp():
    title = "SHELP 指令列表"
    text = f"""/status|状态：获取 Bot 服务器状态
p 管理柚子瓣 <-at/-qq> <num>：修改柚子瓣数目
p 数据：输出所有人的柚子瓣数目

by 柚初 Yurchiu Rin"""

    font_size = 40
    pic = set_txt2img(title, text, font_size)
    await shelp.finish(MessageSegment.image(pic))