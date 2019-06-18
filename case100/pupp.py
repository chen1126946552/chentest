import asyncio
from pyppeteer import launch


async def main():
    browser = await launch({'headless': False})
    page = await browser.newPage()
    await page.goto('https://baidu.com')
    await page.screenshot({'path': 'baidu.png'})
    await page.waitFor(5000)
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
