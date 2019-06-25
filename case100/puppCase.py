import asyncio
import time
from pyppeteer import launch


async def gmailLogin(username, password, url):
    #'headless': False如果想要浏览器隐藏更改False为True
    browser = await launch({'headless': False})
    page = await browser.newPage()
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36')

    await page.goto(url)

    # 输入Gmail
    await page.type('#identifierId', username)
    # 点击下一步
    await page.click('#identifierNext')
    page.mouse  # 模拟真实点击
    time.sleep(10)
    # 输入password
    await page.type('#password input', password)
    # 点击下一步
    await page.click('#passwordNext')
    page.mouse  # 模拟真实点击
    time.sleep(10)

    # 登录成功截图
    await page.screenshot({'path': 'gmail-login.png'})
    #打开谷歌全家桶跳转，以Youtube为例
    await page.goto('https://www.youtube.com')
    time.sleep(10)


if __name__ == '__main__':
    username = 'chen.chen@ptmind.com'
    password = 'chen123456'
    url = 'https://gmail.com'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(gmailLogin(username, password, url))
