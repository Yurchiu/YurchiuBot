from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna, AlconnaMatch, Query, Match, UniMessage, At, AlcResult, AlconnaMatches
from arclet.alconna import Alconna, Args, Option, Arparma, Subcommand
from nonebot_plugin_alconna.uniseg import UniMessage, At, Image
from nonebot import require
require("nonebot_plugin_alconna")
import httpx
from dotenv import load_dotenv
import os
import json
from nonebot import logger
from playwright.async_api import async_playwright
from . import mapping
from nonebot.params import ArgPlainText
from nonebot.adapters import Event
from fake_useragent import UserAgent

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-vv",
    description="在 QQ 群聊中使用 vv 表情包",
    usage="/vv <str> [-r <float>] [-s <float>] []",
    config="",
)

async def getResult(paramR, paramS, paramQ):
    url = "https://vvapi.cicada000.work/search"
    headers = {
        "user-agent": UserAgent().random
    }
    params = {
        "query": str(paramQ),
        "min_ratio": str(int(paramR * 100)),
        "min_similarity": str(paramS),
        "max_results": "20"
    }
    async with httpx.AsyncClient() as client:
        raw = await client.get(url, headers = headers, params = params)
        raw = "[" + raw.text.replace("\n", ",") + "]"
        result = json.loads(raw)
    return result

async def getProhibit(text):
    url = "https://api.nsmao.net/api/sen/query"
    load_dotenv(".env")
    sensitive_key = str(os.getenv("sensitive_key"))
    headers = {
        "user-agent": UserAgent().random
    }
    params = {
        "key": str(sensitive_key),
        "text": str(text)
    }
    async with httpx.AsyncClient() as client:
        raw = await client.get(url, headers = headers, params = params)
        raw = json.loads(raw.text)
    if int(raw["code"]) == 200:
        return raw["data"]["text"]
    else:
        return text
    
async def getVideo(EP):
    url = "https://api.bilibili.com/pgc/player/web/playurl/html5"
    headers = {
        "user-agent": UserAgent().random
    }
    params = {
        "ep_id": str(EP).replace("ep", ""),
    }
    async with httpx.AsyncClient() as client:
        raw = await client.get(url, headers = headers, params = params)
        result = json.loads(raw.text)
        result = result["result"]["durl"][0]["url"]
    return result

vvResult = ""
vvWordsCnt = 0

vv = on_alconna(
    Alconna(
        "/vv",
        Args["query#搜索关键词", str],
        Subcommand(
            "-r",
            Args["r#搜索文本匹配度（[0,1] 范围的实数，默认为 0.65）", float],
        ),
        Subcommand(
            "-s",
            Args["s#人脸相似度（[0,1] 范围的实数，默认为 0.5）", float],
        ),
    )
)

@vv.handle()
async def _(event: Event, result: Arparma = AlconnaMatches()):
    global vvWordsCnt
    global vvResult

    paramR = 0.65
    paramS = 0.5
    paramQ = "测试"
    if result.find("query"):
        paramQ = result.query[str]("query")
    if result.find("-r"):
        paramR = result.query[float]("-r.r")
    if result.find("-s"):
        paramR = result.query[float]("-s.s")

    try:
        vvResult = await getResult(paramR, paramS, paramQ)
    except:
        await vv.finish("在获取搜索结果过程中发生错误，请稍后再试。")

    vvWordsCnt = 0

    words = ""
    temp = ""
    index = -1

    try:
        for item in vvResult:
            temp += f"{str(item['text'])}[]"
    except:
        await vv.finish("没有匹配的搜索结果。")

    logger.success("Successfully got the lines of vv.")

    try:
        temp = (await getProhibit(temp)).split("[]")
    except:
        await vv.finish("在过滤敏感词时发生错误，请稍后再试。")
        
    for item in temp:
        index += 1
        if "*" in item or item == "":
            continue
        vvWordsCnt += 1
        words += f"{vvWordsCnt}. {item}\n"
        vvResult[vvWordsCnt - 1] = vvResult[index]

    words += "请输入数字以返回相应图片。（截取视频截图需要时间，请耐心等待）。回复其他任意消息以停止交互。"

    if vvWordsCnt == 0:
        await vv.finish("返回结果均含有敏感词汇或不合法。")

    logger.success(f"Successfully filtered sensitive words and got {vvWordsCnt} lines.")

    await vv.send(words)

@vv.got("picNumber")
async def _(picNumber: str = ArgPlainText()):
    global vvWordsCnt
    global vvResult

    try:
        picNumber = int(picNumber)
        assert 1 <= picNumber <= vvWordsCnt
    except:
        await vv.finish("用户未输入相应数字，已退出交互。")

    if picNumber == 0:
        await vv.finish("已退出交互。")

    data = vvResult[picNumber - 1]
    EP, TM = mapping.getEPTM(str(data["filename"]).replace(".json",""), str(data["timestamp"]))
    logger.info(f"{EP} {TM}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(channel = "msedge")
        page = await browser.new_page()
        try:
            url = await getVideo(EP)
        except:
            vv.finish("获取链接时发生错误，请稍后再试。")
        src = mapping.getVideoUrl(str(data["filename"]).replace(".json",""), str(data["timestamp"]))
        await vv.send("已获取视频链接，正在截图……")
        await page.goto(url)
        logger.info(url)
        
        await page.evaluate("var v = document.querySelector('video'); v.pause(); v.currentTime=" + TM + ";")
        await page.wait_for_load_state("networkidle")

        async with page.expect_download() as download_info:
            await page.evaluate("v.addEventListener('timeupdate', function() {var myCanvas = new OffscreenCanvas(v.videoWidth,v.videoHeight); var ctx = myCanvas.getContext('2d'); ctx.drawImage(v, 0, 0, v.videoWidth, v.videoHeight); myCanvas.convertToBlob().then(blob => { const fileName = 'screenshot.png'; const d = document.createElement('a'); d.href = window.URL.createObjectURL(blob); d.download = fileName; d.style.display = 'none'; document.body.appendChild(d); d.click(); document.body.removeChild(d); window.URL.revokeObjectURL(d.href); }, 1000);});")
        
        download = await download_info.value
        path = await download.path()
        await vv.send(await UniMessage(Image(path=path)).export())
        await vv.send(f"出处：{src}")
        await browser.close()