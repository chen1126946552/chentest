import asyncio
from pyppeteer import launch
from pyppeteer.network_manager import Request
import time

async def main():
    browser = await launch({'headless': False})
    page = await browser.newPage()
    await page.setViewport({'width': 1366, 'height': 768})
    await page.goto('https://www.ptengine.cn')
    await page.setRequestInterception(True)
    await page.setJavaScriptEnabled(enabled=True)


asyncio.get_event_loop().run_until_complete(main())