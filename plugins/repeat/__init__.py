import nonebot
from nonebot.plugin import PluginMetadata
from .config import Config
from nonebot.rule import to_me
import random
import httpx
import json
from nonebot import require
require("nonebot_plugin_txt2img")
require("nonebot_plugin_alconna")
from nonebot_plugin_txt2img import Txt2Img
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageEvent, MessageSegment, Bot
from nonebot.adapters.onebot.v12 import Bot
from nonebot.adapters import Bot, Event, Message
from nonebot import logger
from nonebot_plugin_alconna import on_alconna, AlconnaMatch, Query, Match, UniMessage, At, AlcResult, AlconnaMatches
from arclet.alconna import Alconna, Args, Option, Arparma, Subcommand
from nonebot_plugin_alconna.uniseg import UniMessage, At, Image
import base64
import time
from dotenv import load_dotenv
import os
from nonebot.params import CommandArg
from nonebot_plugin_orm import Model, async_scoped_session
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import select

__plugin_meta__ = PluginMetadata(
    name="Repeat",
    description="",
    usage="",
    config=Config,
)

config = nonebot.get_plugin_config(Config)

class HisMsg(Model):
    msgId: Mapped[str] = mapped_column(primary_key=True)
    userName: Mapped[str]
    userMsg: Mapped[str]
    msgGroup: Mapped[str]
    userId: Mapped[str]
    ifDel: Mapped[str]

async def get_image_data():
    url = 'https://moe.jitsu.top/img/?type=json&sort=setu'
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        get_dic = json.loads(resp.text)
    data = get_dic["pics"][0]
    return data

setu = nonebot.on_command("色图", block=True, aliases={"涩图"})

@setu.handle()
async def handle_setu(bot: Bot, event: Event):
    msg = await get_image_data()
    msg_list =[]
    msg_list.append(
        {
            "type": "node",
            "data": {
                "name": "你们要看的涩图",
                "uin": event.self_id,
                "content": MessageSegment.image(msg)
                }
            }
        )
    await bot.send_group_forward_msg(group_id = event.group_id, messages = msg_list)



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
    /help /emoji /一言 emoji+emoji /色图|涩图
    /cf /nc /atc /今日比赛 /占卜 /塔罗牌
- 复杂指令
    /撤回 <num1>[-num2]：撤回 Bot 区间内（倒数，从 0 开始数起，前闭后开）的所有消息
    @ /wordle [-l] [-d]：开始一局 wordle 游戏。-l 指定长度 -d 指定词典 【支持词典：GRE、考研、GMAT、专四、TOEFL、SAT、专八、IELTS、CET4、CET6】
    /calc [num|帮助|结束|操作方式]：开始一局计算器游戏。带数字参数表示选定第几关，否则为随机
    /m bind [好友码]：舞萌查分器。绑定舞萌游戏数据
        /m b50：查询 Best 50。若长时间没有回复，请重试
        使用舞萌查分器之前请访问下一条消息给出的链接
    柚子瓣相关指令：请使用命令 gf 柚子瓣帮助 查看帮助信息
    /支付宝到账 <num>：发送到账语音
    /pk|PK|对抗 <@> [@]：根据群名片比较两人实力值
    /机器人叫 <str>：修改机器人群名片
    /语录 [@|删除 <num>]：随机输出来自本群的语录。@ 某人获得某人的语录。可删除指定编号语录
- 交互指令
    /表情包制作：根据接下来的提示制作表情包
        /表情详情 <表情名/关键词>
        /表情搜索 <关键词>
    /字符画 [图片]：接下来发送图片生成字符画
    @ /txt2img：接下来根据提示 文字转图片
    /pjsk：接下来根据提示 生成 pjsk 表情包；使用 /pjsk -h 查看帮助
- 回复指令：
    /撤回：撤回 Bot 此消息
    /语录：此消息进入语录库
- 注意
    提及或 at 柚柚子 时 Bot 会回复。
    Bot 2 秒内不会发送同样的信息。
    <> 表示必选参数，[] 表示可选参数。

by 柚初 Yurchiu Rin"""

    font_size = 36
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
gf 管理 <@/num> <num>：修改柚子瓣数目
gf 数据：输出所有人的柚子瓣数目

by 柚初 Yurchiu Rin"""

    font_size = 40
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

    msg = args.get_message()

    if str(msg) == '6':
        await repeat.finish("6")

    if str(msg) == '草':
        await repeat.finish("草")

    if str(msg) == '（）':
        await repeat.finish("（）")

    if str(msg) == '（':
        await repeat.finish("）")

    if str(msg) == '）':
        await repeat.finish("（")

    if str(msg) == '好好好':
        await repeat.send("是是是")
        await repeat.finish("对对对")

    if "柚初" in str(msg):
        await repeat.finish("柚初太可爱了")

    if "楚子莜" in str(msg):
        await repeat.finish("楚子莜太可爱了")

    if "Yurchiu" in str(msg):
        await repeat.finish("Yurchiu 太可爱了")

    if "圆子" in str(msg):
        await repeat.finish("圆子是天才 M，无可置疑！")

    if "小饼子" in str(msg):
        await repeat.finish("小饼子快说话😡")

    if "雪莉" in str(msg):
        await repeat.finish(MessageSegment.image("C:/Users/Administrator/Desktop/YurchiuBot/data/sherry.jpg"))

    if rpt == msg:
        rptcnt += 1
    else:
        rptcnt = 0
        rpt = msg
    if rptcnt >= 2:
        rptcnt = -1
        ifcease = random.randint(0,1)
        if ifcease == 0:
            await repeat.finish(rpt)
        else:
            text = random.randint(1,3)
            if text == 1:
                await repeat.finish("打断复读！😈")
            elif text == 2:
                await repeat.finish("你想按 +1 是吧杂鱼～")
            else:
                await repeat.finish("大家不要复读了喵")
    
    issend = random.randint(1,100)
    if issend == 1:
        ret = random.randint(0,emojinum-1)
        await repeat.finish(emojis2[ret])
    else:
        norpt += 1
    
    if norpt >= 150:
        norpt = 0
        ret = random.randint(0,emojinum-1)
        await repeat.finish(emojis2[ret])


versus = on_alconna(
    Alconna(
        ["/PK", "/pk", "/对抗"],
        Args["at1", At],
        Args["at2;?", At],
    )
)

@versus.handle()
async def handle_versus(groupevent: GroupMessageEvent, args: Event, bot: Bot, result: Arparma = AlconnaMatches()):
    p1 = args.get_user_id()
    p2 = result.query[At]("at1").target
    if result.find("at2"):
        p1 = result.query[At]("at2").target
    name1 = await bot.get_group_member_info(group_id=str(groupevent.group_id), user_id=str(p1))
    name2 = await bot.get_group_member_info(group_id=str(groupevent.group_id), user_id=str(p2))
    if name1["card"] != "":
        name1 = name1["card"]
    else:
        name1 = name1["nickname"]
    if name2["card"] != "":
        name2 = name2["card"]
    else:
        name2 = name2["nickname"]

    tmp1 = list(str(base64.b64encode(name1.encode("utf-8")),'utf-8'))
    tmp2 = list(str(base64.b64encode(name2.encode("utf-8")),'utf-8'))

    ret1 = ret2 = time.localtime().tm_yday
    for i in tmp1:
        ret1 *= ord(i)
        ret1 %= 100000
        ret1 += 1
    for i in tmp2:
        ret2 *= ord(i)
        ret2 %= 100000
        ret2 += 1

    msg = f"{name1} 的实力值为 {ret1}，{name2} 的实力值为 {ret2}。"

    if ret1 > ret2:
        msg += f"{name1} 获胜！\n"
    elif ret1 < ret2:
        msg += f"{name2} 获胜！\n"
    else:
        msg += f"{name1} 与 {name2} 打成平手！\n"

    msg += "可以通过更改自己的群名片来改变实力值。实力值亦会每日更新。"

    await versus.finish(msg)



rename = nonebot.on_command("机器人叫", block=True)

@rename.handle()
async def handle_rename(bot: Bot, groupevent: GroupMessageEvent, args: Message = CommandArg()):
    newname = args.extract_plain_text()
    load_dotenv(".env")
    SELF = str(os.getenv("SELF"))
    await bot.set_group_card(group_id=str(groupevent.group_id), user_id=SELF, card=str(newname))





hisMsg = on_alconna(
    Alconna(
        ["/语录", "/黑历史"],
        Args["at;?", At],
        Option(
            "删除",
            Args["del", int],
        ),
    )
)

@hisMsg.handle()
async def handle_hismsg(msgevent: MessageEvent, event: Event, bot: Bot, session: async_scoped_session, groupevent: GroupMessageEvent, result: Arparma = AlconnaMatches()):
    opt = ""
    curGroup = str(groupevent.group_id)
    curId = str(event.get_user_id())
    queryGroup = (await session.execute(select(HisMsg).order_by(HisMsg.msgId))).all()
    length = len(queryGroup)
    load_dotenv(".env")
    admin = os.getenv("SUPERUSERS")

    if msgevent.reply:
        msg_id = str(msgevent.reply.message_id)
        msg = await bot.get_msg(message_id = msg_id)

        for i in queryGroup:
            if i.HisMsg.msgId == msg_id:
                i.HisMsg.ifDel = ""
                await session.commit()
                await hisMsg.finish("语录已记录")

        data = HisMsg()
        data.msgId = msg_id
        data.userName = str(msg["sender"]["nickname"])
        data.userId = str(msg["sender"]["user_id"])
        data.userMsg = str(msg["raw_message"])
        data.msgGroup = curGroup
        data.ifDel = ""
        session.add(data)
        logger.info(msg)
        await session.commit()
        await hisMsg.finish("语录已记录")

    elif result.find("删除"):
        delId = str(result.query[int]("删除.del"))
        for i in queryGroup:
            if i.HisMsg.msgId == delId:
                if i.HisMsg.userId == curId:
                    await hisMsg.finish("不能删除自己的语录！")
                else:
                    i.HisMsg.ifDel = "deleted"
                    await session.commit()
                    await hisMsg.finish("已删除")
        await hisMsg.finish("未找到语录")

    else:
        if length == 0:
            await hisMsg.finish("无语录")

        ret = queryGroup[random.randint(0, length - 1)]
        count = 0
        if result.find("at"):
            opt = str(result.query[At]("at").target)
        while ret.HisMsg.msgGroup != curGroup or (opt != "" and opt != ret.HisMsg.userId) or ret.HisMsg.ifDel == "deleted":
            ret = queryGroup[random.randint(0, length - 1)]
            count += 1
            if count >= 50000:
                await hisMsg.finish("无语录")

        msg = ret.HisMsg.userMsg + "（#" + ret.HisMsg.msgId + "）"
        msg += "\n——" + ret.HisMsg.userName 
        await hisMsg.finish(msg)