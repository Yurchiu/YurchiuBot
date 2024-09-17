from nonebot import get_driver
from nonebot.plugin import PluginMetadata
from .config import Config
from nonebot import require
require("nonebot_plugin_txt2img")
from nonebot_plugin_txt2img import Txt2Img
from nonebot.plugin import on_command, on_message
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters import Event
from nonebot.adapters import Message
from nonebot.params import CommandArg
import random
import re
from nonebot import logger

__plugin_meta__ = PluginMetadata(
    name="calc",
    description="",
    usage="",
    config=Config,
)

global_config = get_driver().config
config = Config.parse_obj(global_config)

calcData = (
    ("curId", "curTar", "curStep", "curNum"),
    (1, 8, 3, 0, "+2", "+3"),
    (2, 200, 4, 0, "+10", "*4"),
    (3, 24, 3, 2, "*2", "*3"),
    (4, 4, 4, 125, "<<", "*2"),
    (5, 5, 4, 125, "<<", "*2"),
    (6, 95, 3, 25, "push5", "+4", "/5"),
    (7, 59, 3, 25, "push5", "+4", "/5"),
    (8, 32, 4, 155, "push2", "*2", "<<"),
    (9, 24, 4, 155, "push2", "*2", "<<"),
    (10, 144, 3, 11, "push2", "*12", "<<"),
    (11, 3, 4, 15, "push6", "+5", "<<", "/7"),
    (12, 96, 4, 200, "push1", "+12", "*3", "<<"),
    (13, 63, 3, 200, "push1", "+12", "*3", "<<"),
    (14, 33, 4, 200, "push1", "+12", "*3", "<<"),
    (15, 62, 3, 550, "+6", "1=>2", "<<"),
    (16, 321, 4, 123, "2=>3", "13=>21"),
    (17, 1970, 3, 1985, "sort>", "*2", "<<"),
    (18, 1234, 3, 16, "sort>", "*2", "push7"),
    (19, 333, 4321, 4, "sort<", "2=>3", "1=>3", "<<"),
    (20, 275, 4, 97231, "sort<", "<<", "9=>5"),
    (21, 19, 3, 303, "sort<", "+1", "*3"),
    (22, 100, 3, 303, "sort<", "+1", "*3"),
    (23, 111, 4, 423, "sort<", "/2", "<<", "push1"),
    (24, 123, 4, 423, "sort<", "/2", "<<", "push1"),
    (25, 963, 4, 30, "sort>", "/5", "+6", "push3"),
    (26, 321, 4, 30, "sort>", "/5", "+6", "push3"),
    (27, 4, 3, 3, "+4", "*4", "/4"),
    (28, 5, 3, 4, "+3", "*3", "/3"),
    (29, 9, 4, 50, "/5", "*3", "<<"),
    (30, 100, 3, 99, "-8", "*11", "<<"),
    (31, 23, 4, 171, "*2", "-9", "<<"),
    (32, 24, 6, 0, "+5", "*3", "*5", "<<"),
    (33, 2, 5, 0, "+4", "*9", "<<"),
    (34, 9, 4, 0, "+2", "/3", "push1"),
    (35, 10, 4, 15, "push0", "+2", "/5"),
    (36, 93, 4, 0, "+6", "*7", "6=>9"),
    (37, 2321, 6, 0, "push1", "push2", "1=>2", "2=>3"),
    (38, 24, 5, 0, "+9", "*2", "8=>4"),
    (39, 29, 5, 11, "/2", "+3", "1=>2", "2=>9"),
    (40, 20, 5, 36, "+3", "/3", "1=>2")
)
totalData = 40

helpMsg = f"""通过给出的操作方式由当前数字达到计算目标。分步直接发送“操作方式”中的单引号内内容。
+?, -?, *?, /?：加减乘除操作。
<<： 删除最后一位数。
push?：末尾放上数字。
?=>?：数字中的子串替换。
sort>, sort<：分别为数码从大到小，从小到大排序。"""

global CUROPT
global NOTGAME
global curNum
global curTar
global curStep

CUROPT = ()

NOTGAME = True
__ERR__ = -1
__ADD__ = 1
__MNS__ = 2
__MUL__ = 3
__DIV__ = 4
__DED__ = 5
__PUH__ = 6
__REP__ = 7
__SOT__ = 8

def judgeType(text):
    if type(text) != str:
        return __ERR__
    elif text[0] == "+":
        return __ADD__
    elif text[0] == "-":
        return __MNS__
    elif text[0] == "*":
        return __MUL__
    elif text[0] == "/":
        return __DIV__
    elif text == "<<":
        return __DED__
    elif "push" in text:
        return __PUH__
    elif "=>" in text:
        return __REP__
    elif "sort" in text:
        return __SOT__

def sendPic(text):
    font_size = 60
    txt2img = Txt2Img()
    txt2img.set_font_size(font_size)
    pic = txt2img.draw("", text)
    return MessageSegment.image(pic)

def is_notInGame():
    return NOTGAME

def checkOpt(event: Event) -> bool:
    return (event.get_plaintext() in CUROPT) & (not is_notInGame())

def getNumber(string):
    a = []
    a = re.findall("\d+\.?\d*", string)
    a = list(map(int,a))
    return a


Calc = on_command("calc", block=True)

@Calc.handle()
async def _(args: Message = CommandArg()):
    global CUROPT
    global NOTGAME
    global curNum
    global curTar
    global curStep

    if not is_notInGame():
        await Calc.finish("存在进行中的游戏！")

    NOTGAME = False
    userChoice = getNumber(args.extract_plain_text())

    logger.info(userChoice)

    if userChoice == []:
        choice = calcData[random.randint(1, totalData)]
    elif 1 <= userChoice[0] <= totalData:
        choice = calcData[userChoice[0]]
    else:
        NOTGAME = True
        await Calc.finish(f"谜题编号不在 1~{totalData} 内！")


    curId = choice[0]
    curTar = choice[1]
    curStep = choice[2]
    curNum = choice[3]
    CUROPT = choice[4:]
    initMsg = f"谜题编号：#{curId}\n目前数字：{curNum}\n计算目标：{curTar}\n剩余步数：{curStep}\n操作方式：{CUROPT}"
    initMsg += "\n\n" + helpMsg
    await Calc.send(sendPic(initMsg))


userOpt = on_message(rule=checkOpt, block=True)

@userOpt.handle()
async def handleOpt(event: Event):
    global CUROPT
    global NOTGAME
    global curNum
    global curTar
    global curStep

    opt = event.get_plaintext()
    if opt in CUROPT:
        curStep -= 1
        optType = judgeType(opt)
        NumInOpt = getNumber(opt)


        if optType == __ADD__:
            curNum += NumInOpt[0]
        elif optType == __MNS__:
            curNum -= NumInOpt[0]
        elif optType == __MUL__:
            curNum *= NumInOpt[0]
        elif optType == __DIV__:
            curNum //= NumInOpt[0]
        elif optType == __DED__:
            curNum //= 10
        elif optType == __PUH__:
            curNum = str(curNum) + str(NumInOpt[0])
            curNum = int(curNum)
        elif optType == __REP__:
            curNum = str(curNum).replace(str(NumInOpt[0]), str(NumInOpt[1]))
            curNum = int(curNum)
        elif optType == __SOT__:
            if opt == "sort<":
                curNum = ''.join(sorted(str(curNum)))
            else:
                curNum = ''.join(sorted(str(curNum), reverse=True))
            curNum = int(curNum)



        await Calc.send(sendPic(f"目前数字：{curNum}\n计算目标：{curTar}\n剩余步数：{curStep}\n操作方式：{CUROPT}"))

        if curNum == curTar:
            NOTGAME = True
            await Calc.finish("游戏成功！")
        if curStep <= 0:
            NOTGAME = True
            await Calc.finish("游戏失败！")
    else:
        pass
