from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
import nonebot
from .config import Config
from nonebot.rule import to_me
import random
import httpx
import json
from nonebot import require
require("nonebot_plugin_txt2img")
from nonebot_plugin_txt2img import Txt2Img
from io import BytesIO
require("nonebot_plugin_alconna")
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
from .config import Config
import emoji

__plugin_meta__ = PluginMetadata(
    name="tools",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

class HisMsg(Model):
    msgId: Mapped[str] = mapped_column(primary_key=True)
    userName: Mapped[str]
    userMsg: Mapped[str]
    msgGroup: Mapped[str]
    userId: Mapped[str]
    ifDel: Mapped[str]

async def get_image_data():
    url = 'https://image.anosu.top/pixiv/json?r18=0'
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        get_dic = json.loads(resp.text)
    data = get_dic[0]["url"]
    return data

setu = nonebot.on_command("色图", block=True, aliases={"涩图"})

@setu.handle()
async def handle_setu(bot: Bot, event: Event):
    msg = await get_image_data()
    msg_list = []
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

repeat = nonebot.on_message(priority=10000000)
emojis = ['🥺','🥰','😑','😘','😫','🥵','😡','😈','₍˄·͈༝·͈˄*₎◞ ̑̑','(˃ ⌑ ˂ഃ )','(*σ´∀`)σ','✧٩(ˊωˋ*)و✧','( ･_･)ﾉ⌒●~*','(•̀へ •́ ╮ )','(*꒦ິ⌓꒦ີ)','(ﾟ⊿ﾟ)ﾂ','╮( •́ω•̀ )╭']
rptcnt1 = rptcnt2 = rptcnt3 = 0
norpt = 0
rptnum = 0
rpt1 = rpt2 = rpt3 = ""

@repeat.handle()
async def handle_repeat(args: Event, bot: Bot, event: MessageEvent):
    global rptcnt1
    global rpt1
    global rptcnt2
    global rpt2
    global rptcnt3
    global rpt3
    global norpt
    global rptnum

    msg = args.get_message()
    msg2 = str(msg)

    if "赞" in msg2:
        await bot.set_msg_emoji_like(message_id=event.message_id, emoji_id="76")
    if "收到" in msg2:
        await bot.set_msg_emoji_like(message_id=event.message_id, emoji_id="428")
    if "🥵" in msg2:
        await bot.set_msg_emoji_like(message_id=event.message_id, emoji_id="339")
    if "👀" in msg2:
        await bot.set_msg_emoji_like(message_id=event.message_id, emoji_id="289")
    if "奶龙" in msg2 or "唐" in msg2:
        await bot.set_msg_emoji_like(message_id=event.message_id, emoji_id="147")
    if "草" in msg2 or "艹" in msg2:
        await bot.set_msg_emoji_like(message_id=event.message_id, emoji_id="41")
    if "喵" in msg2:
        await bot.set_msg_emoji_like(message_id=event.message_id, emoji_id="183")
    if "羡慕" in msg2:
        await bot.set_msg_emoji_like(message_id=event.message_id, emoji_id="273")

    if rpt1 == msg:
        rptcnt1 += 1
        rptnum = 1
    elif rpt2 == msg and rpt1 != msg and rptnum >= 1:
        rptcnt2 += 1
        rptnum = 2
    elif rpt3 == msg and rpt2 != msg and rpt1 != msg and rptnum >= 2:
        rptcnt3 += 1
        rptnum = 3
    else:
        rptcnt1 = rptcnt2 = rptcnt3 = 0

    if rptcnt1 >= 2 or rptcnt2 >= 2 or rptcnt3 >= 3:
        ifcease = random.randint(0,2)
        if ifcease != 0 and rptcnt1 >= 2:
            rptcnt1 = -1
            await repeat.send(rpt1)
        elif ifcease != 0 and rptcnt2 >= 2:
            rptcnt2 = -1
            await repeat.send(rpt1)
            await repeat.send(rpt2)
        elif ifcease != 0 and rptcnt3 >= 3:
            rptcnt3 = -1
            await repeat.send(rpt2)
            await repeat.send(rpt1)
            await repeat.send(rpt3)
        else:
            rptcnt1 = rptcnt2 = rptcnt3 = -1
            text = random.randint(1,3)
            if text == 1:
                await repeat.send("打断复读！😈")
            elif text == 2:
                await repeat.send("你想按 +1 是吧杂鱼～")
            else:
                await repeat.send("大家不要复读了喵")

    rpt3 = rpt2
    rpt2 = rpt1
    rpt1 = msg
    
    issend = random.randint(1,100)
    if issend == 1:
        ret = random.randint(0, len(emojis) - 1)
        await repeat.finish(emojis[ret])
    else:
        norpt += 1
    
    if norpt >= 150:
        norpt = 0
        ret = random.randint(0, len(emojis) - 1)
        await repeat.finish(emojis[ret])

rename = nonebot.on_command("改名", block=True)

@rename.handle()
async def handle_rename(bot: Bot, groupevent: GroupMessageEvent, args: Message = CommandArg()):
    newname = args.extract_plain_text()
    load_dotenv(".env")
    SELF = str(os.getenv("SELF"))
    await bot.set_group_card(group_id=str(groupevent.group_id), user_id=SELF, card=str(newname))

choice = nonebot.on_command("帮选", aliases={"选择","挑一个","帮我选"}, block=True)

@choice.handle()
async def handle_choice(args: Message = CommandArg()):
    clist = args.extract_plain_text().split()
    clen = len(clist)
    ch = random.randint(0, clen - 1)
    await choice.finish(f"命运为你挑选：{clist[ch]}")

hisMsg = on_alconna(
    Alconna(
        ["/语录", "/黑历史", "/野史"],
        Args["at;?", At],
        Option(
            "删除",
            Args["del", int],
        ),
        Option(
            "合订本",
            Args["at;?", At],
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
    admin = (os.getenv("SUPERUSERS"))

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
        data.userName = str(msg["sender"]["card"]) + "（" + str(msg["sender"]["nickname"]) + "）"
        if str(msg["sender"]["card"]) == "":
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
                if i.HisMsg.userId == curId and not(curId in admin):
                    await hisMsg.finish("不能删除自己的语录！")
                else:
                    i.HisMsg.ifDel = "deleted"
                    await session.commit()
                    await hisMsg.finish("已删除")
        await hisMsg.finish("未找到语录")

    elif result.find("合订本"):
        at = 0
        if result.find("合订本.at"):
            at = str(result.query[At]("合订本.at").target)
        msg_list = []
        flag = 0

        for i in queryGroup:
            if (i.HisMsg.userId == at or at == 0) and i.HisMsg.msgGroup == curGroup and i.HisMsg.ifDel != "deleted":
                msg_list.append(
                    {
                        "type": "node",
                        "data": {
                            "name": "你们要看的合订本",
                            "uin": i.HisMsg.userId,
                            "content": i.HisMsg.userMsg + "\n↑ 语录编号：" + i.HisMsg.msgId + "\n↑ 发送者：" + i.HisMsg.userName
                        }
                    }
                )
                flag = 1

        if flag == 1:
            await bot.send_group_forward_msg(group_id = curGroup, messages = msg_list)
        else:
            await hisMsg.finish("无语录")

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

        msg = ret.HisMsg.userMsg + "\n↑ 语录编号：" + ret.HisMsg.msgId + "\n↑ 发送者：" + ret.HisMsg.userName
        await bot.send_group_msg(group_id = curGroup, message = msg)