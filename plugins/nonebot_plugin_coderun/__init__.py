from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import MessageEvent, Message, Bot, GroupMessageEvent
import re
from .runcode import code
from nonebot import logger

runcode = code()
command = on_command("run", aliases={"code", "运行"}, priority=5, block=False)


@command.handle()
async def main(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    code = args.extract_plain_text()
    if not code:
        await command.finish(
            "请输入运行语言和代码...\n目前支持的语言有:\nkotlin/java/lua/nodejs/go/swift/rust/ruby/c#/c++/c/python/php/bash/groovy/asm/R/vb/typescript/pascal\n编译错误等不会回复")
    split = code.split(maxsplit = 1)
    logger.info(split[0])
    logger.info(split[1])
    try:
        await command.finish(await runcode.run(split[0],split[1]))
    except IndexError:
        await command.finish("格式错误\n目前仅支持\nkotlin/java/lua/nodejs/go/swift/rust/ruby/c#/c++/c/python/php/bash/groovy/asm/R/vb/typescript/pascal\n请输入全称")