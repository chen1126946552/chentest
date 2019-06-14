const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({headless:false});
  const page = await browser.newPage();
  await page.goto('https://example.com');
  await page.screenshot({path: 'example.png'});

  await browser.close();
})();

//获取一组元素的对应属性
		const al = await page.$$eval('.connection-list__col-name > span.connection-list__name', els => Array.from(els).map(el=> el.innerText))
		log(al[0])
		log(al[1])
		log(al[2])