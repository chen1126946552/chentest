import asyncio
from pyppeteer import launch


async def main():
    browser = await launch({'headless': True})
    page = await browser.newPage()
    await page.goto('http://datatest12.ptmind.com/chen/test3.html')
    # await page.screenshot({'path': 'baidu.png'})

    await page.setRequestInterception(True);
    # test = await page.on('request', '''req => {
    #     requestUrl = req.url();
    #     if(requestUrl.endsWith('egg')){
    #         req.abort();
    #     }else{
    #         req.continue();
    #     }
    # });''', force_expr=True)
    # print(test)

    await page.waitFor(10000)
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
