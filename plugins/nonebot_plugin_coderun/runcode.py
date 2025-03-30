import httpx
import re
from nonebot import logger

class code():
    def __init__(self):
        self.codeIds = {
            "kotlin": 2960,
            "java": 10,
            "lua": 66,
            "nodejs": 22,
            "go": 21,
            "swift": 20,
            "rust": 19,
            "ruby": 13,
            "c#": 14,
            "c++": 12,
            "c": 11,
            "python": 9,
            "php": 1,
            "bash": 18,
            "groovy": 6208,
            "asm": 6206,
            "R": 5649,
            "vb": 5648,
            "typescript": 5577,
            "pascal": 73
        }
        self.otherName = {
            "kotlin": "kt",
            "java": "java",
            "lua": "lua",
            "nodejs": "node.js",
            "go": "go",
            "swift": "swift",
            "rust": "rs",
            "ruby": "rb",
            "c#": "cs",
            "c++": "cpp",
            "c": "c",
            "python": "py3",
            "php": "php",
            "bash": "sh",
            "groovy": "groovy",
            "asm": "asm",
            "R": "R",
            "vb": "vb",
            "typescript": "ts",
            "pascal": "pas"
        }
    
    async def run(self, language, code):
        language = str(language)
        try:
            codeId = self.codeIds[language]
        except KeyError:
            return '不支持的语言\n目前仅支持\nkotlin/java/lua/nodejs/go/swift/rust/ruby/c#/c++/c/python/php/bash/groovy/asm/R/vb/typescript/pascal\n请输入全称'
        token = await self.getToken(codeId)
        result = await self.getResult(token, code, language)
        return str(result)
    
    async def getToken(self, codeId):
        '''
        url = f"https://c.runoob.com/compile/{codeId}/"
        async with httpx.AsyncClient(verify=False, timeout=60, follow_redirects=True) as client:
            data = await client.get(url)
            result = data.text
        token = re.findall("token = '(.+)';", result)[0]
        '''
        token = "dadefd4c8adfb0e7d2221d31e1639f0c"
        return token
    
    async def getResult(self, token, code, language):
        language = self.otherName[language]
        data = {
            "code": code,
            "token": token,
            "stdin": '',
            "language": 7,
            "fileext": language
        }
        async with httpx.AsyncClient(verify=False, timeout=60, follow_redirects=True) as client:
            data = await client.post("https://www.runoob.com/try/compile2.php", data=data)
            result = data.json()['output']
        return result
        

