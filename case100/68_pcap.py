import asyncio
from pyppeteer import launch
import time

async def main():exepath = 'C:/Users/tester02/AppData/Local/Google/Chrome/Application/chrome.exe'
    browser = await launch({'executablePath': exepath, 'headless': False, 'slowMo': 30})
    page = await browser.newPage()
    await page.setViewport({'width': 1366, 'height': 768})
    await page.goto('http://192.168.2.66')
    await page.type("#Login_Name_Input", "test02")
    await page.type("#Login_Password_Input", "12345678", )
    await page.waitFor(1000)
    await page.click("#Login_Login_Btn")
    await page.waitFor(3000)
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())