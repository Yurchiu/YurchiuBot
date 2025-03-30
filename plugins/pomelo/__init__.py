import nonebot
from nonebot.rule import to_me
from nonebot import get_plugin_config
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
from nonebot import get_bot
from nonebot import require
require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import on_alconna, AlconnaMatch, Query, Match, UniMessage, At, AlcResult, AlconnaMatches
from arclet.alconna import Alconna, Args, Option, Arparma, Subcommand
from nonebot_plugin_alconna.uniseg import UniMessage, At, Image
import time
import random
from nonebot import logger
from dotenv import load_dotenv
import os
from nonebot_plugin_userinfo import get_user_info
require("nonebot_plugin_txt2img")
from nonebot_plugin_txt2img import Txt2Img
from io import BytesIO
import base64

# Need nonebot_plugin_txt2img

__plugin_meta__ = PluginMetadata(
    name="pomelo",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

sincereWords = [
    "你最大的遗憾是什么？",
    "你最尴尬的时刻是什么？",
    "你最后一次撒谎是什么？",
    "你最尴尬的习惯是什么？",
    "你最害怕的是什么？",
    "你上次哭是什么时候？",
    "你最引以为豪的是自己的哪一点？",
    "你收到过的最好的建议是什么？",
    "你收到过的最糟糕的建议是什么？",
    "有没有关于你的谣言流传过？",
    "你搜索的最后一个东西是什么？",
    "你最喜欢的电影是哪一部？",
    "你还和毛绒玩具一起睡觉吗？",
    "你曾经最怕的是什么？",
    "你觉得什么品质最吸引人？",
    "你最反感的是什么？",
    "你有什么秘密吗？",
    "你曾经在考试中作弊吗？",
    "你最幻想的是什么？",
    "你有隐藏的天赋吗？",
    "你经历过的最糟糕的争论是什么？",
    "你害怕变老吗？",
    "你的生活中有什么想改变的吗？",
    "你喜欢的最奇怪的食物组合是什么？",
    "你最大的烦恼是什么？",
    "哪些歌曲构成了你人生的配乐？",
    "你在学校做过最糟糕的事是什么？",
    "你遇到过的最大的麻烦是什么？",
    "你做过最恶心的事是什么？",
    "你做过的最奇怪的梦是什么？",
    "你后悔撒谎的事情是什么？",
    "你认为人们对你有什么误解？",
    "你早上醒来做的第一件事是什么？",
    "你最大的成就是什么？",
    "你花在什么 APP 上的时间最多？",
    "你认为自己 10 年后会怎样？",
    "你给过别人第二次机会吗？",
    "如果你可以和某个群友交换生命，你会选择谁？",
    "你梦想的职业是什么？",
    "在 1-10 分的范围内，你如何描述你的时尚感？",
    "你会如何用三个词描述自己？",
    "在友谊中你最看重什么？",
    "如果群主退群，你认为谁会接任？"
]

bigAdventure = [
    "请 @ 群中的某三个人",
    "用方言发一句歌词语音",
    "发一张自己的丑照",
    "发一张手绘自画像",
    "发语音模仿 QQ 特别关心音效",
    "发一条说说，内容为“我最可爱”",
    "发送自己最早的 QQ 头像",
    "发送自己最早的 QQ 个性签名",
    "截图前年二月一号之后第一个说说并发送",
    "立刻拍照发送自己的床铺照片",
    "拍照发送自己手正面的照片",
    "拍照发送自己宿舍桌面的照片",
    "唱一段儿歌",
    "模仿一位名人的台词",
    "用夹子音随便说一句话",
    "将自己所有柚子瓣的一半赠给某人",
    "将自己所有柚子瓣进行打赌操作",
    "任意抢固定某个人柚子瓣三次",
    "读一遍自己的今日运势内容",
    "在群聊历史记录中搜索自己含有“喵”的发言记录并截图发送",
    "拍机器人两下",
    "闭眼盲打随意一句话，完成后不能修改立即发送",
    "以上一句群友发言作为关键词，连续输入输入法第一个候选词 10 次并发送"
]

fortune = ["大吉", "中吉", "小吉", "中平", "凶", "大凶"]

things = [
            ["去商场", "收获满满", "没有满意的东西"],
            ["宅家", "享受自由时光", "无聊无事可做"],
            ["装弱", "谦虚使人进步", "被骂凡尔赛"],
            ["女装", "浅尝辄止", "只有零次或无数次"],
            ["团建", "增进关系", "搞砸了"],
            ["睡觉", "养足精力，明日再战", "翻来覆去睡不着"],
            ["吃小零食", "真好吃", "又胖五斤"],
            ["做作业", "领先同学一步", "毫无动力"],
            ["写代码", "既对又快", "全是 bug"],
            ["群内辩论", "最佳辩手", "会被禁言"],
            ["照镜子", "你真好看", "你不好看"],
            ["拍照", "留住美好瞬间", "发现没对好焦"],
            ["复读", "人类的本质", "被打断"],
            ["开车", "车技惊人", "会堵车"],
            ["玩其他机器人", "还是别的机器人好玩", "本机器人生气了"],
            ["做饭", "口味甚佳", "盐放多了"],
            ["水群", "忙里偷闲", "无话可聊"],
            ["骂学校", "解气", "被导员发现"],
            ["翘课", "真爽", "那节课点名"],
            ["做实验", "一次成功", "误差过大"],
            ["复习", "知识更牢固了", "发现啥也不会"],
            ["考试", "必不挂科", "小心挂科"],
            ["抢柚子瓣", "成为柚子瓣富豪", "反被抢光"],
            ["扶老奶奶过马路", "增加人品", "被讹"],
            ["吃饭", "人是铁饭是钢", "小心变胖"],
            ["搞基", "友谊地久天长", "会被掰弯"],
            ["处对象", "说不定可以牵手", "一定会被拒绝"],
            ["写作业", "都会写，写的全对", "上课讲了这些了吗"],
            ["开电脑", "电脑的状态也很好", "意外的死机故障不可避"],
            ["重构代码", "代码质量明显提高", "越改越乱"],
            ["装逼", "获得众人敬仰", "被识破"],
            ["纳财", "要到好多 Money", "然而今天并没有财运"],
            ["玩网游", "犹如神助", "匹配到一群猪队友"],
            ["熬夜", "事情终究可以完成的", "爆肝"],
            ["体育锻炼", "身体棒棒哒", "消耗的能量全吃回来了"],
            ['刷B站', '承包一天笑点', '视频加载不出来'],
            ['打游戏', '杀疯了', '送人头'],
            ['摸鱼', '摸鱼不被发现', '摸鱼被发现'],
            ['玩原神', '抽卡全金', '抽卡九蓝一紫'],
            ['玩mc', '进下界遇到远古残骸', '家被苦力怕炸'],
            ['看电影', '找到一部超好看的电影', '电影很无聊'],
            ['学习新技能', '轻松掌握新知识', '学不会新知识'],
            ['做家务', '家里变得超级干净', '越做越乱'],
            ['做饭', '做出美味佳肴', '糊锅了'],
            ['运动', '状态非常好', '受伤了'],
            ['阅读', '读到一本好书', '看不进去书'],
            ['听音乐', '发现一首新歌', '耳机坏了'],
            ['购物', '买到物美价廉的东西', '买到假货'],
            ['散步', '心情舒畅', '迷路了'],
            ['画画', '画出满意的作品', '画得一团糟'],
            ['写作', '灵感涌现', '毫无灵感'],
            ['编程', '顺利解决难题', '遇到奇怪的bug'],
            ['学习外语', '进步明显', '记不住单词'],
            ['做瑜伽', '身心放松', '拉伤肌肉'],
            ['摄影', '拍到美丽的风景', '相机没电'],
            ['烹饪', '尝试新菜谱成功', '味道奇怪'],
            ['看直播', '遇到有趣的主播', '网络卡顿'],
            ['聚会', '度过愉快的时光', '气氛尴尬'],
            ['健身', '锻炼效果显著', '肌肉酸痛'],
            ['阅读新闻', '了解新资讯', '全是负面消息'],
            ['看纪录片', '增长见识', '枯燥乏味'],
            ['练习乐器', '进步飞快', '音准不准'],
            ['打扫房间', '焕然一新', '灰尘满天'],
            ['做手工', '完成一件作品', '失败多次'],
            ['看电影', '感动落泪', '剧情无聊'],
            ['旅行', '体验不同的文化', '遇到恶劣天气'],
            ['听讲座', '收获满满', '听不懂'],
            ['参加比赛', '获得好成绩', '表现不佳'],
            ['看书', '学到新知识', '看不懂'],
            ['练字', '字体变漂亮', '字迹潦草'],
            ['做甜品', '美味可口', '烤焦了'],
            ['看动漫', '追完一季', '断更了'],
            ['看小说', '一口气看完', '没时间看完'],
            ['做PPT', '顺利完成', '格式错误'],
            ['玩Linux','[OK]','Kernel Panic!!!'],
         ]

def set_txt2img(title, text, size):
    txt2img = Txt2Img()
    txt2img.set_font_size(size)
    pic = txt2img.draw(title, text)
    return pic

def get_value(name):
    if name["card"] != "":
        name = name["card"]
    else:
        name = name["nickname"]
    tmp = list(str(base64.b64encode(name.encode("utf-8")),'utf-8'))
    ret = time.localtime().tm_yday
    for i in tmp:
        ret *= ord(i)
        ret %= 100000
        ret += 1
    return ret


class PomeloData(Model):
    userName: Mapped[str] = mapped_column(primary_key=True)
    userPomelo: Mapped[int]
    userValue: Mapped[int]
    checkDays: Mapped[int]
    robNumber: Mapped[int]
    todayWaifu: Mapped[str]
    todayLuck: Mapped[str]
    ifMerried: Mapped[int]
    ifChecked: Mapped[int]

    def __init__(self, userName):
        self.userName = userName
        self.userPomelo = 0
        self.userValue = 0
        self.ifChecked = -1
        self.checkDays = 0
        self.robNumber = 0
        self.todayWaifu = "single"
        self.ifMerried = -1
        self.todayLuck = ""


Pomelo = on_alconna(
    Alconna(
        "p",
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
            "抢柚子瓣",
            Args["target", At],
            Args["number", int],
        ),
        Subcommand(
            "偷柚子瓣",
            Args["number", int],
        ),
        Subcommand(
            "赠柚子瓣",
            Args["target", At],
            Args["number", int],
        ),
        Option(
            "排行",
        ),
        Subcommand(
            "管理柚子瓣",
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
        Option(
            "娶群友",
        ),
        Option(
            "换群友",
        ),
        Subcommand(
            "抢群友",
            Args["target", At],
        ),
        Subcommand(
            "打赌",
            Args["asset", int],
        ),
        Subcommand(
            "真心话",
            Args["target", At],
        ),
        Subcommand(
            "大冒险",
            Args["target", At],
        ),
    )
)


@Pomelo.handle()
async def _(bot: Bot, groupevent: GroupMessageEvent, session: async_scoped_session, args: Event, result: Arparma = AlconnaMatches()):

    load_dotenv(".env")
    POMELO_ENABLE = os.getenv("POMELO_ENABLE")
    SUPERUSERS = os.getenv("SUPERUSERS")

    if str(groupevent.group_id) not in POMELO_ENABLE:
        return

    curUser = args.get_user_id()
    curGroup = groupevent.group_id
    curTime = time.localtime().tm_yday
    ifSuper = 0

    if curUser in SUPERUSERS:
        ifSuper = 1

    data = PomeloData(curUser)
    data2 = PomeloData("0")

    if not(await session.get(PomeloData, curUser)):
        session.add(data)
        await session.commit()

    data = await session.get(PomeloData, curUser)

    temp = await bot.get_group_member_info(group_id=str(groupevent.group_id), user_id=data.userName)
    data.userValue = get_value(temp)

    if data.ifChecked != curTime:
        data.todayWaifu = "single"
        data.ifMerried = -1
        data.todayLuck = ""
        data.robNumber = 0

    if result.find("签到"):

        if data.ifChecked != curTime:
            if data.ifChecked + 1 == curTime:
                data.checkDays += 1
            else:
                data.checkDays = 1

            numberStart = 50 + data.checkDays*2
            getNumber = random.randint(numberStart, numberStart + 50)
            data.userPomelo += getNumber
            data.ifChecked = curTime

            fortuneLen = len(fortune)
            thingsLen = len(things)

            todayFortune = fortune[random.randint(0,fortuneLen - 1)]

            data.todayLuck = "你的今日运势：" + todayFortune + "\n\n"

            numRand = numThing = ["", "", "", "", ""]
            numRand[1] = numRand[2] = numRand[3] = numRand[4] = random.randint(0, thingsLen - 1)

            while numRand[1] == numRand[2]:
                numRand[2] = random.randint(0, thingsLen - 1)

            while numRand[1] == numRand[3] or numRand[2] == numRand[3]:
                numRand[3] = random.randint(0, thingsLen - 1)

            while numRand[1] == numRand[4] or numRand[2] == numRand[4] or numRand[3] == numRand[4]:
                numRand[4] = random.randint(0, thingsLen - 1)

            numThing[1] = "▪️ " + things[numRand[1]][0] + "（" + things[numRand[1]][1] + "）"
            numThing[2] = "▪️ " + things[numRand[2]][0] + "（" + things[numRand[2]][2] + "）"
            numThing[3] = "▪️ " + things[numRand[3]][0] + "（" + things[numRand[3]][1] + "）"
            numThing[4] = "▪️ " + things[numRand[4]][0] + "（" + things[numRand[4]][2] + "）"

            if todayFortune == "大吉":
                numThing[1] = numThing[2] = numThing[3] = numThing[4] = "▪️ 万事皆宜"
            elif todayFortune == "大凶":
                numThing[1] = numThing[2] = numThing[3] = numThing[4] = "▪️ 万事皆忌"

            data.todayLuck += "宜：\n" + numThing[1] + "\n" + numThing[3] + "\n忌：\n" + numThing[2] + "\n" + numThing[4]

            await Pomelo.send(f"签到成功！获得 {getNumber} 个柚子瓣！现在你有 {data.userPomelo} 个柚子瓣哦！连续签到了 {data.checkDays} 天喵！")
            await Pomelo.send(data.todayLuck)

        else:
            await Pomelo.send("你已经签到过了！")


    elif result.find("娶群友"):

        if data.ifMerried != curTime:
            data.ifMerried = curTime
            queryGroup = (await session.execute(select(PomeloData).order_by(PomeloData.userName))).all()
            curGroupUsers = await bot.get_group_member_list(group_id=str(curGroup))
            userList = []
            for i in queryGroup:
                if i.PomeloData.userName == data.userName:
                    continue
                flag = 1
                for j in curGroupUsers:
                    if str(j["user_id"]) == i.PomeloData.userName:
                        flag = 0
                if flag == 1:
                    continue
                userList.append(i.PomeloData.userName)
            userCount = len(userList)

            if userCount == 0:
                data.todayWaifu = "single"
                await Pomelo.send(f"悲报，娶群友未成功！今日只能换群友/抢群友，或被群友娶。")

            data.todayWaifu = userList[random.randint(0, userCount - 1)]
            data2 = await session.get(PomeloData, data.todayWaifu)

            if data2.ifMerried != curTime or (data2.ifMerried == curTime and data2.todayWaifu == "single"):
                data2.ifMerried = curTime
                data2.todayWaifu = data.userName
                todayWaifuInfo = await get_user_info(bot, args, data.todayWaifu)
                todayWaifuInfo = str(todayWaifuInfo.user_avatar.get_url())
                await Pomelo.send(f"喜报，娶群友成功！今天你的群老婆是 " + UniMessage(At("user", data.todayWaifu)) + "❤️！" + UniMessage(Image(url=todayWaifuInfo)))
            else:
                data.todayWaifu = "single"
                await Pomelo.send("悲报，娶群友未成功！今日只能换群友/抢群友，或被群友娶。")
        elif data.ifMerried == curTime and data.todayWaifu != "single":
            await Pomelo.send("你已经娶过了或已经是某个人的老婆了！")
        else:
            await Pomelo.send("你貌似被某个人抛弃了或娶群友未成功🥺！")

    elif result.find("换群友"):

        if data.userPomelo < 300:
            await Pomelo.finish("你的柚子瓣不够 300 个！")

        queryGroup = (await session.execute(select(PomeloData).order_by(PomeloData.userName))).all()
        curGroupUsers = await bot.get_group_member_list(group_id=str(curGroup))
        userList = []
        for i in queryGroup:
            if i.PomeloData.userName == data.userName:
                continue
            if i.PomeloData.userName == data.todayWaifu:
                continue
            flag = 1
            for j in curGroupUsers:
                if str(j["user_id"]) == i.PomeloData.userName:
                    flag = 0
            if flag == 1:
                continue
            userList.append(i.PomeloData.userName)

        userCount = len(userList)
        if userCount == 0:
            await Pomelo.send(f"悲报，换群友未成功！退还柚子瓣 300！")

        if data.ifMerried == curTime and data.todayWaifu != "single":
            dataNTR1 = await session.get(PomeloData, data.todayWaifu)
            dataNTR1.todayWaifu = "single"

        data.ifMerried = curTime
        data.todayWaifu = userList[random.randint(0, userCount - 1)]
        data2 = await session.get(PomeloData, data.todayWaifu)

        if data2.ifMerried == curTime and data2.todayWaifu != "single":
            dataNTR2 = await session.get(PomeloData, data2.todayWaifu)
            dataNTR2.todayWaifu = "single"

        data2.ifMerried = curTime
        data2.todayWaifu = data.userName

        todayWaifuInfo = await get_user_info(bot, args, data.todayWaifu)
        todayWaifuInfo = str(todayWaifuInfo.user_avatar.get_url())
        await Pomelo.send(f"喜报，换群友成功！扣除柚子瓣 300！今天你的群老婆是 " + UniMessage(At("user", data.todayWaifu)) + "❤️！" + UniMessage(Image(url=todayWaifuInfo)))
        data.userPomelo -= 300

    elif result.find("抢群友"):

        if data.userPomelo < 300:
            await Pomelo.finish("你的柚子瓣不够 300 个！")

        curAt = result.query[At]("抢群友.target").target
        if not(await session.get(PomeloData, curAt)):
            data2.userName = curAt
            session.add(data2)
            session.commit()
        data2 = await session.get(PomeloData, curAt)

        data.userPomelo -= 300

        temp = await bot.get_group_member_info(group_id=str(groupevent.group_id), user_id=data2.userName)
        data2.userValue = get_value(temp)
        winValue = 50 + (data.userValue - data2.userValue) / 2000
        winValue += data.checkDays * 5 + data2.robNumber * 20
        winValue = min(100, winValue)
        winValue -= data.robNumber * 20
        winValue = max(0, winValue)

        if winValue > random.randint(0, 100):
            if data.ifMerried == curTime and data.todayWaifu != "single":
                dataNTR1 = await session.get(PomeloData, data.todayWaifu)
                dataNTR1.todayWaifu = "single"

            data.ifMerried = curTime
            data.todayWaifu = data2.userName

            if data2.ifMerried == curTime and data2.todayWaifu != "single":
                dataNTR2 = await session.get(PomeloData, data2.todayWaifu)
                dataNTR2.todayWaifu = "single"

            data2.ifMerried = curTime
            data2.todayWaifu = data.userName

            todayWaifuInfo = await get_user_info(bot, args, data.todayWaifu)
            todayWaifuInfo = str(todayWaifuInfo.user_avatar.get_url())
            await Pomelo.send(f"喜报，抢群友成功！柚子瓣扣除 300！今天你的群老婆是 " + UniMessage(At("user", data.todayWaifu)) + "❤️！" + UniMessage(Image(url=todayWaifuInfo)))
        else:
            await Pomelo.send(f"悲报，抢群友未成功！柚子瓣扣除 300！")



    elif result.find("查询"):

        if result.find("查询.target"):
            curAt = result.query[At]("查询.target").target
            if not(await session.get(PomeloData, curAt)):
                data2.userName = curAt
                session.add(data2)
                session.commit()
            data2 = await session.get(PomeloData, curAt)
            await Pomelo.send(f"现在 ta 有 {data2.userPomelo} 个柚子瓣哦！")

        else:
            await Pomelo.send(f"现在你有 {data.userPomelo} 个柚子瓣哦！连续签到了 {data.checkDays} 天喵！今天抢了 {data.robNumber} 次！你目前的实力值是 {data.userValue}！")
            await Pomelo.send(data.todayLuck)
            if data.ifMerried != curTime:
                pass
            elif data.ifMerried == curTime and data.todayWaifu != "single":
                todayWaifuInfo = await get_user_info(bot, args, data.todayWaifu)
                todayWaifuInfo = str(todayWaifuInfo.user_avatar.get_url())
                logger.info(todayWaifuInfo)
                await Pomelo.send(f"今天你的群老婆是 " + UniMessage(At("user", data.todayWaifu)) + "❤️！" + UniMessage(Image(url=todayWaifuInfo)))
            else:
                await Pomelo.send(f"你貌似被某个人抛弃了或娶群友未成功🥺！")


    elif result.find("抢柚子瓣"):

        curAt = result.query[At]("抢柚子瓣.target").target
        if not(await session.get(PomeloData, curAt)):
            data2.userName = curAt
            session.add(data2)
            session.commit()

        data2 = await session.get(PomeloData, curAt)
        robNumber = result.query[int]("抢柚子瓣.number")
        if data2.userPomelo < robNumber:
            await Pomelo.send("对方柚子瓣不够！你太贪心了！")
        elif data.userPomelo < robNumber:
            await Pomelo.send("你的柚子瓣不够！本钱太少了！")
        elif robNumber <= 0:
            await Pomelo.send("只能抢正数个！")
        else:
            temp = await bot.get_group_member_info(group_id=str(groupevent.group_id), user_id=data2.userName)
            data2.userValue = get_value(temp)
            winValue = 50 + (data.userValue - data2.userValue) / 2000
            winValue += data.checkDays * 5 + data2.robNumber * 20
            winValue = min(100, winValue)
            winValue -= data.robNumber * 20
            winValue = max(0, winValue)
            data.robNumber += 1
            if winValue > random.randint(0, 100):
                data.userPomelo += robNumber
                data2.userPomelo -= robNumber
                await Pomelo.send(f"你的实力值为 {data.userValue}，对方的实力值为 {data2.userValue}，成功把握为 {winValue}%。\n抢劫成功！你获得了 {robNumber} 个柚子瓣！你现在有 {data.userPomelo} 个柚子瓣！")
            else:
                data.userPomelo -= robNumber
                data2.userPomelo += robNumber
                await Pomelo.send(f"你的实力值为 {data.userValue}，对方的实力值为 {data2.userValue}，成功把握为 {winValue}%。\n抢劫失败！你被对方拿走了 {robNumber} 个柚子瓣！你现在有 {data.userPomelo} 个柚子瓣！")
            
            if data.robNumber - data2.robNumber > 4:
                await Pomelo.send(f"你现在偷/抢了 {data.robNumber} 次之多，处于疲惫状态，偷/抢柚子瓣不易成功，建议明天再来喵！")


    elif result.find("偷柚子瓣"):

        queryGroup = (await session.execute(select(PomeloData).order_by(PomeloData.userName))).all()
        gfDict = {}
        for i in queryGroup:
            gfDict[i.PomeloData.userName] = i.PomeloData.userPomelo
        theftList = sorted(gfDict.items(), key=lambda d: d[1], reverse=True)
        curAt = theftList[random.randint(0, len(theftList)-1)][0]

        if not(await session.get(PomeloData, curAt)):
            data2.userName = curAt
            session.add(data2)
            session.commit()

        data2 = await session.get(PomeloData, curAt)

        await Pomelo.send("尝试偷某个群友的柚子瓣……")

        robNumber = result.query[int]("偷柚子瓣.number")
        if data2.userPomelo < robNumber:
            await Pomelo.send("对方柚子瓣不够！")
        elif data.userPomelo < robNumber:
            await Pomelo.send("你的柚子瓣不够！本钱太少了！")
        elif robNumber <= 0:
            await Pomelo.send("只能偷正数个！")
        else:
            temp = await bot.get_group_member_info(group_id=str(groupevent.group_id), user_id=data2.userName)
            data2.userValue = get_value(temp)
            winValue = 50 + (data.userValue - data2.userValue) / 2000
            winValue += data.checkDays * 5 + data2.robNumber * 20
            winValue = min(100, winValue)
            winValue -= data.robNumber * 20
            winValue = max(0, winValue)
            data.robNumber += 1
            if winValue > random.randint(0, 100):
                data.userPomelo += robNumber
                data2.userPomelo -= robNumber
                await Pomelo.send(f"你的实力值为 {data.userValue}，成功把握为 {winValue}%。\n偷窃成功！你获得了 {robNumber} 个柚子瓣！你现在有 {data.userPomelo} 个柚子瓣！")
            else:
                data.userPomelo -= robNumber
                data2.userPomelo += robNumber
                await Pomelo.send(f"你的实力值为 {data.userValue}，成功把握为 {winValue}%。\n偷窃过程中被对方发现！你被对方拿走了 {robNumber} 个柚子瓣！你现在有 {data.userPomelo} 个柚子瓣！")
            
            if data.robNumber - data2.robNumber > 4:
                await Pomelo.send(f"你现在偷/抢了 {data.robNumber} 次之多，处于疲惫状态，偷/抢柚子瓣不易成功，建议明天再来喵！")


    elif result.find("赠柚子瓣"):

        curAt = result.query[At]("赠柚子瓣.target").target
        if not(await session.get(PomeloData, curAt)):
            data2.userName = curAt
            session.add(data2)
            session.commit()

        data2 = await session.get(PomeloData, curAt)
        giveNumber = result.query[int]("赠柚子瓣.number")
        if data.userPomelo < giveNumber:
            await Pomelo.send("你的柚子瓣不够！")
        elif giveNumber <= 0:
            await Pomelo.send("只能赠正数个！")
        else:
            data.userPomelo -= giveNumber
            data2.userPomelo += giveNumber
            await Pomelo.send(f"赠送成功！你失去了 {giveNumber} 个柚子瓣！你现在有 {data.userPomelo} 个柚子瓣！")

    elif result.find("帮助"):

        title = "POMELO 指令列表"
        text = f"""- 指令头：p
- 基础子指令：
    签到：每日签到，获得柚子瓣、运势。另外，戳一戳也可随机获得柚子瓣
    查询 [@]：查询各项记录
    抢柚子瓣 <@> <num>：抢某人的柚子瓣
    赠柚子瓣 <@> <num>：赠给某人柚子瓣
    偷柚子瓣 <num>：偷随机一个人柚子瓣
    帮助：帮助信息
    排行：输出本群柚子瓣数排行榜
- 功能子指令
    娶群友：娶群友，可能失败。娶得的群友在各群互通，不会娶到其他群的群友。如果你的群老婆是其他群的，只会显示头像
    换群友：花费 300 柚子瓣，换随机群友，必成功，除非用指令的人太少
    抢群友 <@>：花费 300 柚子瓣，抢指定群友，可能失败
    打赌 <num>：下注 num 进行打赌，随机获得或扣除柚子瓣
    真心话/大冒险 <@>：花费 300 柚子瓣，指定某个群友完成任务
- 备注
    实力值影响抢/偷柚子瓣以及抢群友成功率，它与群名片有关，并每日刷新

by 柚初 Yurchiu Rin"""

        font_size = 41
        pic = set_txt2img(title, text, font_size)
        ghelpmsg = MessageSegment.image(pic)
        await Pomelo.send(ghelpmsg)

    elif result.find("排行"):

        queryGroup = (await session.execute(select(PomeloData).order_by(PomeloData.userName))).all()
        gfDict = {}
        curGroupUsers = await bot.get_group_member_list(group_id=str(curGroup))
        for i in queryGroup:
            gfDict[i.PomeloData.userName] = i.PomeloData.userPomelo
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
        pic = set_txt2img(title, text, font_size)
        printImg = MessageSegment.image(pic)
        await Pomelo.send(printImg)


    elif result.find("管理柚子瓣"):

        if ifSuper == 0:
            await Pomelo.finish("无权限。")
        
        if result.find("管理柚子瓣.at"):
            curAt = result.query[At]("管理柚子瓣.at.args.at").target
        elif result.find("管理柚子瓣.qq"):
            curAt = str(result.query[int]("管理柚子瓣.qq.args.qq"))
        else:
            await Pomelo.finish("参数不足。")

        if not(await session.get(PomeloData, curAt)):
            data2.userName = curAt
            session.add(data2)
            session.commit()

        data2 = await session.get(PomeloData, curAt)
        giveNumber = result.query[int]("管理柚子瓣.number")
        data2.userPomelo += giveNumber
        await Pomelo.send(f"对方柚子瓣变动 {giveNumber}，目前有 {data2.userPomelo} 个柚子瓣。")


    elif result.find("数据"):

        if ifSuper == 0:
            await Pomelo.finish("无权限。")

        queryGroup = (await session.execute(select(PomeloData).order_by(PomeloData.userName))).all()
        gfDict = {}
        for i in queryGroup:
            gfDict[i.PomeloData.userName] = i.PomeloData.userPomelo
        printList = sorted(gfDict.items(), key=lambda d: d[1], reverse=True)
        text = "QQ 号 | 柚子瓣数目"
        for i in printList:
            text += "\n" + str(i[0]) + " " + str(i[1])
        await Pomelo.send(text)


    elif result.find("打赌"):

        asset = result.query[int]("打赌.asset")
        param = random.randint(1, 100)
        if asset > data.userPomelo:
            await session.commit()
            await Pomelo.finish("你的柚子瓣不够！")

        data.userPomelo -= asset
        win_prob = param / 100.0
        if asset <= 0:
            win_prob = 114514

        if random.random() < win_prob:
            multiplier = 95.0 / param
            data.userPomelo += int(asset * multiplier)
            await Pomelo.send(f"赌局成功！你现在有 {data.userPomelo} 个柚子瓣！")
        else:
            asset = 0
            await Pomelo.send(f"赌局失败！你现在有 {data.userPomelo} 个柚子瓣！")


    elif result.find("真心话"):

        if data.userPomelo < 300:
            await Pomelo.finish("你的柚子瓣不够 300 个！")
        data.userPomelo -= 300

        curAt = result.query[At]("真心话.target").target
        if not(await session.get(PomeloData, curAt)):
            data2.userName = curAt
            session.add(data2)
            session.commit()

        data2 = await session.get(PomeloData, curAt)
        queryCnt = len(sincereWords)
        querySelect = random.randint(0, queryCnt - 1)
        queryText = sincereWords[querySelect]
        await Pomelo.send("[#" + str(querySelect) + "] 请 " + (MessageSegment.at(curAt)) + " 回答真心话：\n" + queryText)


    elif result.find("大冒险"):

        if data.userPomelo < 300:
            await Pomelo.finish("你的柚子瓣不够 300 个！")
        data.userPomelo -= 300
        
        curAt = result.query[At]("大冒险.target").target
        if not(await session.get(PomeloData, curAt)):
            data2.userName = curAt
            session.add(data2)
            session.commit()

        data2 = await session.get(PomeloData, curAt)
        queryCnt = len(bigAdventure)
        querySelect = random.randint(0, queryCnt - 1)
        queryText = bigAdventure[querySelect]
        await Pomelo.send("[#" + str(querySelect) + "] 请 " + (MessageSegment.at(curAt)) + " 完成大冒险：\n" + queryText)


    await session.commit()



poke = nonebot.on_notice(rule=to_me(),block=True,priority=9999999)

@poke.handle()
async def handle_poke(session: async_scoped_session, args: Event):
    if args.get_event_name() == "notice.notify.poke":
        curUser = args.get_user_id()
        ret = random.randint(1, 100)
        change = 0
        prefix = "EARLY "
        if random.randint(0, 1) == 1:
            prefix = "LATE "

        if 1 <= ret <= 1:
            await poke.send("CRITICAL PERFECT ❤️ (+100)")
            change = 100
        elif 2 <= ret <= 10:
            await poke.send(prefix + "PERFECT 🥰 (+50)")
            change = 50
        elif 11 <= ret <= 25:
            await poke.send(prefix + "GREAT 😘 (+25)")
            change = 25
        elif 26 <= ret <= 45:
            await poke.send(prefix + "GOOD 😊 (+10)")
            change = 10
        elif 46 <= ret <= 70:
            await poke.send("BAD 😥 (-10)")
            change = -10
        else:
            await poke.send("MISS 😡 (-30)")
            change = -30

        if not(await session.get(PomeloData, curUser)):
            data = PomeloData(curUser)
            session.add(data)
            await session.commit()

        data = await session.get(PomeloData, curUser)
        data.userPomelo += change
        data.userPomelo = max(0, data.userPomelo)
        await session.commit()