from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from playwright.async_api import async_playwright
from .config import Config
import nonebot
from nonebot.adapters import Message
from nonebot.params import CommandArg
import re
from playwright.async_api import Playwright, async_playwright, expect
from nonebot_plugin_alconna.uniseg import File, UniMessage, MsgTarget, Target
from nonebot.params import ArgPlainText
from nonebot import logger
from nonebot.matcher import Matcher
from nonebot_plugin_alconna import on_alconna
from arclet.alconna import Alconna
import os

__plugin_meta__ = PluginMetadata(
    name="neteasemusic",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

qualityOption = {
    1: "标准音质",
    2: "极高音质",
    3: "无损音质",
    4: "高解析度无损",
    5: "高清环绕声",
    6: "沉浸环绕声",
    7: "超清母带"
}

nemusic = on_alconna(
    Alconna(
        "/音乐解析",
    )
 )

@nemusic.got("url", prompt="请输入网易云音乐链接（仅支持单曲）")
async def _(matcher: Matcher, url: str = ArgPlainText()):
    matcher.set_arg("url", url)

@nemusic.got("url")
@nemusic.got("quality", prompt="请输入数字。注：数字越大文件越大，上传时间越久。\n1.标准音质 2.极高音质 3.无损音质 4.高解析度无损 5.高清环绕声 6.沉浸环绕声 7.超清母带")
async def _(target: MsgTarget, url: str = ArgPlainText(), quality: str = ArgPlainText()):
    try:
        quality = int(quality)
        assert 1 <= quality <= 7
        await nemusic.send("下载中……")
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(channel = "msedge")
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto("https://api.toubiec.cn/wyapi.html")
            await page.wait_for_load_state("networkidle")
            await page.get_by_role("textbox", name="解析地址").click()
            await page.get_by_role("textbox", name="解析地址").fill(url)
            await page.get_by_text("请选择音质").click()
            await page.get_by_text(qualityOption[quality]).click()
            await page.locator("div").filter(has_text=re.compile(r"^请选择类型$")).nth(4).click()
            await page.get_by_role("option", name="单曲").click()
            await page.get_by_role("button", name="立即解析").click()
            await page.get_by_role("button", name="确认").click()
            await page.wait_for_load_state("networkidle")
            async with page.expect_download() as download_info:
                await page.get_by_role("button", name="点击下载").click()
            download = await download_info.value
            path = str(await download.path())
            newpath = path.replace(os.path.basename(path), "music.mp3")
            os.renames(path, newpath)
            await nemusic.send("发送文件中……")
            await UniMessage(File(path=newpath)).send(target=target)
            await context.close()
            await browser.close()
    except:
        await nemusic.send("发生错误。")