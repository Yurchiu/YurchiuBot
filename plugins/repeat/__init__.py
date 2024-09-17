import nonebot
from nonebot.plugin import PluginMetadata
from .config import Config
from nonebot.adapters import Event
from nonebot.rule import to_me
import random

from nonebot import require
require("nonebot_plugin_txt2img")
from nonebot_plugin_txt2img import Txt2Img
from nonebot.adapters.onebot.v11 import MessageSegment

__plugin_meta__ = PluginMetadata(
    name="Repeat",
    description="",
    usage="",
    config=Config,
)

config = nonebot.get_plugin_config(Config)




emojis = ['🥺','🥰','😑','😘','😫','🥵','😡','😈','😀']
emojis2 = ['₍˄·͈༝·͈˄*₎◞ ̑̑','(˃ ⌑ ˂ഃ )','(*σ´∀`)σ','✧٩(ˊωˋ*)و✧','( ･_･)ﾉ⌒●~*','(•̀へ •́ ╮ )','(*꒦ິ⌓꒦ີ)','(ﾟ⊿ﾟ)ﾂ','╮( •́ω•̀ )╭']
emojinum = 9
emoji = nonebot.on_command("emoji", block=True)

@emoji.handle()
async def handle_emoji():
    ret = random.randint(0,emojinum-1)
    await emoji.finish(emojis[ret])




help = nonebot.on_command("help", block=True)

@help.handle()
async def handle_help():
    title = "HELP 指令列表"
    text = f"""- 单指令
    /help /emoji /一言 emoji+emoji /cf /nc
    /atc /今日比赛 /占卜 /塔罗牌
- 复杂指令
    /撤回 <num1>[-num2]：撤回 Bot 区间内（倒数，从 0 开始数起，前闭后开）的所有消息
    @ /wordle [-l] [-d]：开始一局 wordle 游戏。-l 指定长度 -d 指定词典 【支持词典：GRE、考研、GMAT、专四、TOEFL、SAT、专八、IELTS、CET4、CET6】
    /calc [num]：开始一局计算器游戏。带参数表示选定第几关，否则为随机。
    /m bind [好友码]：舞萌查分器。绑定舞萌游戏数据
        /m b50：查询 Best 50
        使用舞萌查分器之前请访问 https://github.com/KomoriDev/nonebot-plugin-lxns-maimai/wiki
- 交互指令
    /表情包制作：根据接下来的提示制作表情包
        /表情详情 <表情名/关键词>
        /表情搜索 <关键词>
    /字符画 [图片]：接下来发送图片生成字符画
    @ /text2img：接下来根据提示 文字转图片
- 回复指令：
    /撤回：撤回 Bot 此消息
- 注意
    提及或 at 柚柚子 时 Bot 会回复。
    Bot 2 秒内不会发送同样的信息。
    <> 表示必选参数，[] 表示可选参数。

by 柚初 Yurchiu Rin"""

    font_size = 32
    txt2img = Txt2Img()
    txt2img.set_font_size(font_size)
    pic = txt2img.draw(title, text)
    helpmsg = MessageSegment.image(pic)
    await help.send(helpmsg)
    await help.finish(f"""项目地址：https://github.com/Yurchiu/YurchiuBot
舞萌查分器（第三方）：https://github.com/KomoriDev/nonebot-plugin-lxns-maimai/wiki""")




shelp = nonebot.on_command("shelp",block=True)

@shelp.handle()
async def handle_shelp():
    title = "SHELP 指令列表"
    text = f"""@ /stop|shutdown|停机：停止 Bot 运行，无法重启
@ /restart|reboot|重启：停止运行并重启 Bot
/status|状态：获取 Bot 服务器状态
/清除消息记录：清除插件记录的消息 ID 数据
/提醒比赛：比赛手动定时提醒
/开摆：清除所有定时比赛任务

by 柚初 Yurchiu Rin"""

    font_size = 32
    txt2img = Txt2Img()
    txt2img.set_font_size(font_size)
    pic = txt2img.draw(title, text)
    shelpmsg = MessageSegment.image(pic)
    await shelp.finish(shelpmsg)




'''
atme = nonebot.on_message(rule=to_me(),block=True,priority=9999999)

@atme.handle()
async def handle_atme(args: Event):
    str2 = args.get_plaintext()
    str = args.get_plaintext()
    str = str.replace("我","@#$$#@")
    str = str.replace("你","我")
    str = str.replace("@#$$#@","你")
    str = str.replace("？","！")
    str = str.replace("?","!")
    str = str.replace("吗","")
    str = str.replace("嘛","")
    str = str.replace("说","")
    if random.randint(0,1) == 0:
        str = str.replace("是不是","是")
    else:
        str = str.replace("是不是","不是")
    if  len(str)<=0 or len(str)>=20:
        ret = random.randint(0,emojinum-1)
        await repeat.finish("叫我干嘛"+emojis2[ret])
    else:
        await atme.finish(str)
'''



repeat = nonebot.on_message(priority=10000000,block=True)

rpt = ""
rptcnt = 0
norpt = 0

@repeat.handle()
async def handle_repeat(args: Event):
    global rptcnt
    global rpt
    global norpt

    if rpt == args.get_message():
        rptcnt += 1
    else:
        rptcnt = 0
        rpt = args.get_message()
    if rptcnt >= 2:
        rptcnt = -1
        await repeat.finish(rpt)
    
    issend = random.randint(1,50)
    if issend == 1:
        ret = random.randint(0,emojinum-1)
        await repeat.finish(emojis2[ret])
    else:
        norpt += 1
    
    if norpt >= 75:
        norpt = 0
        ret = random.randint(0,emojinum-1)
        await repeat.finish(emojis2[ret])