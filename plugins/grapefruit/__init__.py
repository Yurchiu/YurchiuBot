import nonebot
from nonebot.rule import to_me
from nonebot import get_driver
from nonebot.plugin import PluginMetadata
from nonebot_plugin_orm import Model, async_scoped_session
from sqlalchemy.orm import Mapped, mapped_column
from .config import Config
from sqlalchemy import select
from nonebot.adapters import Event
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment
from nonebot.adapters.onebot.v12 import Bot
from nonebot.adapters import Bot
import httpx
import json
from nonebot import get_bot
from nonebot import require
require("nonebot_plugin_alconna")
require("nonebot_plugin_txt2img")
from nonebot_plugin_txt2img import Txt2Img
from nonebot_plugin_alconna import on_alconna, AlconnaMatch, Query, Match, UniMessage, At, AlcResult, AlconnaMatches
from arclet.alconna import Alconna, Args, Option, Arparma, Subcommand
from nonebot_plugin_alconna.uniseg import UniMessage, At, Image
import time
import random
from nonebot import logger
from dotenv import load_dotenv
import os
from nonebot_plugin_userinfo import get_user_info


__plugin_meta__ = PluginMetadata(
    name="grapefruit",
    description="",
    usage="",
    config=Config,
)

global_config = get_driver().config
config = Config.parse_obj(global_config)


async def get_image_data():
    url = 'https://api.miaomc.cn/image/get?type=json'
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        get_dic = json.loads(resp.text)
    data = get_dic["url"]
    return data



class grapefruit(Model):
    userName: Mapped[str] = mapped_column(primary_key=True)
    gfNumber: Mapped[int]
    ifCheck: Mapped[int]
    combo: Mapped[int]
    robNumber: Mapped[int]
    waifu: Mapped[str]
    ifMerried: Mapped[int]
    # junk: Mapped[int]


Grapefruit = on_alconna(
    Alconna(
        "gf",
        Option(
            "签到",
        ),
        Subcommand(
            "查询",
            Args["target;?", At],
        ),
        Option(
            "帮助",
        ),
        Subcommand(
            "抢",
            Args["target", At],
            Args["number", int],
        ),
        Subcommand(
            "赠",
            Args["target", At],
            Args["number", int],
        ),
        Option(
            "排行",
        ),
        Option(
            "二次元图",
        ),
        Subcommand(
            "管理",
            Option(
                "-at",
                Args["at;?", At],
            ),
            Option(
                "-qq",
                Args["qq;?", int],
            ),
            Args["number", int],
        ),
        Option(
            "数据",
        ),
        Subcommand(
            "查看老婆",
            Args["target;?", At],
        ),
        Option(
            "娶群友",
        ),
        Option(
            "换群友",
        ),
        Subcommand(
            "抢群友",
            Args["target", At],
            Args["number", int],
        ),
    )
)


@Grapefruit.handle()
async def handle_grapefruit(bot: Bot, groupevent: GroupMessageEvent, session: async_scoped_session, args: Event, result: Arparma = AlconnaMatches()):
    curUser = args.get_user_id()
    curGroup = groupevent.group_id
    curTime = time.localtime().tm_yday
    data = grapefruit()
    data.userName = curUser
    data.gfNumber = 0
    data.ifCheck = -1
    data.combo = 0
    data.robNumber = 0
    data.waifu = "single"
    data.ifMerried = -1

    data2 = grapefruit()
    data2.userName = "0"
    data2.gfNumber = 0
    data2.ifCheck = -1
    data2.combo = 0
    data2.robNumber = 0
    data2.waifu = "single"
    data2.ifMerried = -1

    if not(await session.get(grapefruit, curUser)):
        session.add(data)
        await session.commit()

    data = await session.get(grapefruit, curUser)

    if result.find("签到"):

        if data.ifCheck != curTime:
            if data.ifCheck + 1 == curTime:
                data.combo += 1
            else:
                data.combo = 1

            numberStart = 50 + data.combo
            getNumber = random.randint(numberStart, numberStart + 50)
            data.gfNumber += getNumber
            data.ifCheck = curTime
            data.robNumber = 0
            await Grapefruit.send(f"签到成功！获得 {getNumber} 个柚子瓣！现在你有 {data.gfNumber} 个柚子瓣哦！连续签到了 {data.combo} 天喵！")
        else:
            await Grapefruit.send(f"你已经签到过了！")

    elif result.find("娶群友"):

        if data.ifMerried != curTime:
            data.ifMerried = curTime
            queryGroup = (await session.execute(select(grapefruit).order_by(grapefruit.userName))).all()
            curGroupUsers = await bot.get_group_member_list(group_id=str(curGroup))
            userList = []
            for i in queryGroup:
                if i.grapefruit.userName == data.userName:
                    continue
                flag = 1
                for j in curGroupUsers:
                    if str(j["user_id"]) == i.grapefruit.userName:
                        flag = 0
                if flag == 1:
                    continue
                userList.append(i.grapefruit.userName)
            userCount = len(userList)

            if userCount == 0:
                data.waifu = "single"
                await Grapefruit.send(f"悲报，娶群友未成功！今日只能换群友/抢群友，或被群友娶。")

            data.waifu = userList[random.randint(0, userCount - 1)]
            data2 = await session.get(grapefruit, data.waifu)

            if data2.ifMerried != curTime or (data2.ifMerried == curTime and data2.waifu == "single"):
                data2.ifMerried = curTime
                data2.waifu = data.userName
                waifuInfo = await get_user_info(bot, args, data.waifu)
                waifuInfo = str(waifuInfo.user_avatar.get_url())
                await Grapefruit.send(f"喜报，娶群友成功！今天你的群老婆是 " + UniMessage(At("user", data.waifu)) + "❤️！" + UniMessage(Image(url=waifuInfo)))
            else:
                data.waifu = "single"
                await Grapefruit.send(f"悲报，娶群友未成功！今日只能换群友/抢群友，或被群友娶。")
        elif data.ifMerried == curTime and data.waifu != "single":
            await Grapefruit.send(f"你已经娶过了或被娶过了！")
        else:
            await Grapefruit.send(f"你貌似被抛弃了🥺！")

    elif result.find("换群友"):

        if data.gfNumber < 300:
            await Grapefruit.finish("你的柚子瓣不够 300 个！")

        queryGroup = (await session.execute(select(grapefruit).order_by(grapefruit.userName))).all()
        curGroupUsers = await bot.get_group_member_list(group_id=str(curGroup))
        userList = []
        for i in queryGroup:
            if i.grapefruit.userName == data.userName:
                continue
            if i.grapefruit.userName == data.waifu:
                continue
            flag = 1
            for j in curGroupUsers:
                if str(j["user_id"]) == i.grapefruit.userName:
                    flag = 0
            if flag == 1:
                continue
            userList.append(i.grapefruit.userName)

        userCount = len(userList)
        if userCount == 0:
            await Grapefruit.send(f"悲报，换群友未成功！退还柚子瓣！")

        if data.ifMerried == curTime and data.waifu != "single":
            dataNTR1 = await session.get(grapefruit, data.waifu)
            dataNTR1.waifu = "single"

        data.ifMerried = curTime
        data.waifu = userList[random.randint(0, userCount - 1)]
        data2 = await session.get(grapefruit, data.waifu)

        if data2.ifMerried == curTime and data2.waifu != "single":
            dataNTR2 = await session.get(grapefruit, data2.waifu)
            dataNTR2.waifu = "single"

        data2.ifMerried = curTime
        data2.waifu = data.userName

        waifuInfo = await get_user_info(bot, args, data.waifu)
        waifuInfo = str(waifuInfo.user_avatar.get_url())
        await Grapefruit.send(f"喜报，换群友成功！今天你的群老婆是 " + UniMessage(At("user", data.waifu)) + "❤️！" + UniMessage(Image(url=waifuInfo)))
        data.gfNumber -= 300

    elif result.find("抢群友"):

        curAt = result.query[At]("抢群友.target").target
        if not(await session.get(grapefruit, curAt)):
            data2.userName = curAt
            session.add(data2)
            session.commit()

        data2 = await session.get(grapefruit, curAt)
        robNumber = result.query[int]("抢群友.number")

        if robNumber > data.gfNumber:
            await Grapefruit.finish("你的柚子瓣不够！")
        if robNumber <= 0:
            await Grapefruit.finish("柚子瓣只能是正数个！")

        data.gfNumber -= robNumber

        checkSuc = random.randint(1,1000)
        if checkSuc <= robNumber:
            if data.ifMerried == curTime and data.waifu != "single":
                dataNTR1 = await session.get(grapefruit, data.waifu)
                dataNTR1.waifu = "single"

            data.ifMerried = curTime
            data.waifu = data2.userName

            if data2.ifMerried == curTime and data2.waifu != "single":
                dataNTR2 = await session.get(grapefruit, data2.waifu)
                dataNTR2.waifu = "single"

            data2.ifMerried = curTime
            data2.waifu = data.userName

            waifuInfo = await get_user_info(bot, args, data.waifu)
            waifuInfo = str(waifuInfo.user_avatar.get_url())
            await Grapefruit.send(f"喜报，抢群友成功！今天你的群老婆是 " + UniMessage(At("user", data.waifu)) + "❤️！" + UniMessage(Image(url=waifuInfo)))
        else:
            await Grapefruit.send(f"悲报，抢群友未成功！柚子瓣扣除 {robNumber}！")



    elif result.find("查询"):

        if result.find("查询.target"):

            curAt = result.query[At]("查询.target").target
            if not(await session.get(grapefruit, curAt)):
                data2.userName = curAt
                session.add(data2)
                session.commit()

            data2 = await session.get(grapefruit, curAt)
            await Grapefruit.send(f"现在 ta 有 {data2.gfNumber} 个柚子瓣哦！连续签到了 {data2.combo} 天喵！今天抢了 {data2.robNumber} 次！")
        else:
            await Grapefruit.send(f"现在你有 {data.gfNumber} 个柚子瓣哦！连续签到了 {data.combo} 天喵！今天抢了 {data.robNumber} 次！")


    elif result.find("抢"):

        curAt = result.query[At]("抢.target").target
        if not(await session.get(grapefruit, curAt)):
            data2.userName = curAt
            session.add(data2)
            session.commit()

        data2 = await session.get(grapefruit, curAt)
        robNumber = result.query[int]("抢.number")
        if data2.gfNumber < robNumber:
            await Grapefruit.send("对方柚子瓣不够！你太贪心了！")
        elif data.gfNumber < robNumber:
            await Grapefruit.send("你的柚子瓣不够！本钱太少了！")
        elif robNumber <= 0:
            await Grapefruit.send("只能抢正数个！")
        else:
            pStart = 50 + data.combo + data2.robNumber*4
            pStart = min(100, pStart)
            pStart -= data.robNumber*4
            pStart = max(20,pStart)
            ret = random.randint(1,100)
            data.robNumber += 1
            if ret<=pStart:
                data.gfNumber += robNumber
                data2.gfNumber -= robNumber
                await Grapefruit.send(f"抢劫成功！你获得了 {robNumber} 个柚子瓣！你现在有 {data.gfNumber} 个柚子瓣！")
            else:
                data.gfNumber -= robNumber
                data2.gfNumber += robNumber
                await Grapefruit.send(f"抢劫失败！你失去了 {robNumber} 个柚子瓣！你现在有 {data.gfNumber} 个柚子瓣！")

    elif result.find("赠"):

        curAt = result.query[At]("赠.target").target
        if not(await session.get(grapefruit, curAt)):
            data2.userName = curAt
            session.add(data2)
            session.commit()

        data2 = await session.get(grapefruit, curAt)
        giveNumber = result.query[int]("赠.number")
        if data.gfNumber < giveNumber:
            await Grapefruit.send("你的柚子瓣不够！")
        elif giveNumber <= 0:
            await Grapefruit.send("只能赠正数个！")
        else:
            data.gfNumber -= giveNumber
            data2.gfNumber += giveNumber
            await Grapefruit.send(f"赠送成功！你失去了 {giveNumber} 个柚子瓣！你现在有 {data.gfNumber} 个柚子瓣！")

    elif result.find("帮助"):

        title = "GRAPEFRUIT 指令列表"
        text = f"""- 指令头：gf
- 基础子指令：
    签到：每日签到
    查询 [@]：查询各项记录
    抢 <@> <num>：抢某人的柚子瓣
    赠 <@> <num>：赠给某人柚子瓣
    帮助：帮助信息
    排行：输出本群柚子瓣数排行榜
- 功能子指令
    二次元图：（花费 25 柚子瓣）发送二次元图
    查看老婆 [@]：查看你或别人的群老婆
    娶群友：娶群友，可能失败。娶得的群友在各群互通，不会娶到其他群的群友。如果你的群老婆是其他群的，只会显示头像
    换群友：（花费 300 柚子瓣）换随机群友，必成功，除非用指令的人太少
    抢群友 <@> <num>：（花费 0 以上的柚子瓣）抢指定群友，花费柚子瓣越多越容易成功，花费 1000 及以上必定成功
    管理 <@/num> <num>：（超级管理员）改柚子瓣数目
    数据：（超级管理员）输出所有人的柚子瓣数目
- 柚子瓣其他用途：
    戳一戳随机赠送
- 注意事项：
    连续签到可以对签到获得、抢成功柚子瓣有增益。签到天数在跨年时归零。多次抢柚子瓣成功概率会降低。相关命令只能在群里使用。戳 Bot 得到的柚子瓣数期望为 -1，所以别戳啦！

by 柚初 Yurchiu Rin"""

        font_size = 41
        txt2img = Txt2Img()
        txt2img.set_font_size(font_size)
        pic = txt2img.draw(title, text)
        ghelpmsg = MessageSegment.image(pic)
        await Grapefruit.send(ghelpmsg)

    elif result.find("二次元图"):

        if data.gfNumber < 25:
            await Grapefruit.finish("你的柚子瓣不够 25 个！")

        msg = await get_image_data()
        await Grapefruit.send(MessageSegment.image(msg))
        data.gfNumber -= 25

    elif result.find("排行"):

        queryGroup = (await session.execute(select(grapefruit).order_by(grapefruit.userName))).all()
        gfDict = {}
        curGroupUsers = await bot.get_group_member_list(group_id=str(curGroup))
        for i in queryGroup:
            gfDict[i.grapefruit.userName] = i.grapefruit.gfNumber
        printList = sorted(gfDict.items(), key=lambda d: d[1], reverse=True)
        count = 1
        title = "柚子瓣数目 前 10 名"
        text = ""
        for i in printList:
            if count > 10:
                break
            flag = 0
            name = ""
            for j in curGroupUsers:
                if str(j["user_id"]) == str(i[0]):
                    flag = 1
                    name = j["nickname"]
                    break
            if flag == 0:
                continue
            text += " " + str(count) + ". "
            text += name + "：" + str(i[1]) + " 个"
            text += "\n"
            count += 1
            
        text += "仅显示使用过命令的用户"

        font_size = 32
        txt2img = Txt2Img()
        txt2img.set_font_size(font_size)
        pic = txt2img.draw(title, text)
        printImg = MessageSegment.image(pic)
        await Grapefruit.send(printImg)


    elif result.find("管理"):

        load_dotenv(".env")
        SUPERUSERS = os.getenv("SUPERUSERS")
        if curUser not in SUPERUSERS:
            await Grapefruit.finish("无权限。")
        
        if result.find("管理.at"):
            curAt = result.query[At]("管理.at.args.at").target
        elif result.find("管理.qq"):
            curAt = str(result.query[int]("管理.qq.args.qq"))
        else:
            await Grapefruit.finish("参数不足。")

        if not(await session.get(grapefruit, curAt)):
            data2.userName = curAt
            session.add(data2)
            session.commit()

        data2 = await session.get(grapefruit, curAt)
        giveNumber = result.query[int]("管理.number")
        data2.gfNumber += giveNumber
        await Grapefruit.send(f"管理员：对方柚子瓣变动 {giveNumber}，目前有 {data2.gfNumber} 个柚子瓣。")


    elif result.find("数据"):

        load_dotenv(".env")
        SUPERUSERS = os.getenv("SUPERUSERS")
        if curUser not in SUPERUSERS:
            await Grapefruit.finish("无权限。")

        queryGroup = (await session.execute(select(grapefruit).order_by(grapefruit.userName))).all()
        gfDict = {}
        for i in queryGroup:
            gfDict[i.grapefruit.userName] = i.grapefruit.gfNumber
        printList = sorted(gfDict.items(), key=lambda d: d[1], reverse=True)
        text = "QQ 号 | 柚子瓣数目"
        for i in printList:
            text += "\n" + str(i[0]) + " " + str(i[1])
        await Grapefruit.send(text)


    elif result.find("查看老婆"):

        if result.find("查看老婆.target"):

            curAt = result.query[At]("查看老婆.target").target
            if not(await session.get(grapefruit, curAt)):
                data2.userName = curAt
                session.add(data2)
                session.commit()

            data2 = await session.get(grapefruit, curAt)

            if data2.ifMerried != curTime:
                await Grapefruit.send(f"今天 ta 还未娶群友！")
            elif data2.ifMerried == curTime and data2.waifu != "single":
                waifuInfo = await get_user_info(bot, args, data2.waifu)
                waifuInfo = str(waifuInfo.user_avatar.get_url())
                await Grapefruit.send(f"今天 ta 的群老婆是 " + UniMessage(At("user", data2.waifu)) + "❤️！" + UniMessage(Image(url=waifuInfo)))
            else:
                await Grapefruit.send(f"ta 貌似被抛弃了🥺！")
        else:
            if data.ifMerried != curTime:
                await Grapefruit.send(f"今天你还未娶群友！")
            elif data.ifMerried == curTime and data.waifu != "single":
                waifuInfo = await get_user_info(bot, args, data.waifu)
                waifuInfo = str(waifuInfo.user_avatar.get_url())
                logger.info(waifuInfo)
                await Grapefruit.send(f"今天你的群老婆是 " + UniMessage(At("user", data.waifu)) + "❤️！" + UniMessage(Image(url=waifuInfo)))
            else:
                await Grapefruit.send(f"你貌似被抛弃了🥺！")


    await session.commit()



poke = nonebot.on_notice(rule=to_me(),block=True,priority=9999999)

@poke.handle()
async def handle_poke(session: async_scoped_session, args: Event):
    if args.get_event_name() == "notice.notify.poke":
        curUser = args.get_user_id()
        ret = random.randint(1,100)
        change = 0
        if 1<=ret<=3:
            await poke.send("CRITICAL PERFECT ❤️ (柚子瓣 +20)")
            change = 20
        elif 4<=ret<=30:
            ret2 = random.randint(1,2)
            if 4<=ret<=10 and ret2==1:
                await poke.send("EARLY PERFECT 🥰 (柚子瓣 +10)")
                change = 10
            elif 11<=ret<=30 and ret2==1:
                await poke.send("EARLY GOOD 😘 (柚子瓣 +5)")
                change = 5
            elif 4<=ret<=10 and ret2==2:
                await poke.send("LATE PERFECT 🥰 (柚子瓣 +10)")
                change = 10
            else:
                await poke.send("LATE GOOD 😘 (柚子瓣 +5)")
                change = 5
        elif 31<=ret<=59:
            await poke.send("BAD 🥺 (柚子瓣 -3)")
            change = -3
        elif ret==60:
            await poke.send("BAD APPLE 🍎🥺 (柚子瓣 -3)")
            change = -3
        else:
            await poke.send("MISS 😡 (柚子瓣 -6)")
            change = -6

        if not(await session.get(grapefruit, curUser)):
            data = grapefruit()
            data.userName = curUser
            data.gfNumber = 0
            data.ifCheck = -1
            data.combo = 0
            data.robNumber = 0
            session.add(data)
            await session.commit()

        data = await session.get(grapefruit, curUser)
        data.gfNumber += change
        data.gfNumber = max(0, data.gfNumber)
        await session.commit()