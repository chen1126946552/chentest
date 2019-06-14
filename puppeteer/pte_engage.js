
const puppeteer = require('puppeteer');
const {TimeoutError} = require('puppeteer/Errors');  // Error handling
const fs = require('fs');
const log = console.log;  // 缩写 console.log

const log_server_0 = 'Log_server_0: Service start-up.';
log(log_server_0);


(async () => {
	const browser = await puppeteer.launch({
		args: ['--no-sandbox', '--disable-setuid-sandbox'],
		ignoreHTTPSErrors: true,
		devtools: false,
		headless: false,
		defaultViewport: {width:1366, height:768},
		timeout: 30000,
	});

	const page = await browser.newPage();

	const Case_01 = 'OPEN datatest12.ptmind.com';
	log(Case_01);

	await page.goto('http://datatest12.ptmind.com/');
	await page.waitFor(5000);

	const documentSize = await page.evaluate(() => {
		return {
			width: document.documentElement.clientWidth,
			height: document.body.clientHeight,
			}
	});

	// 鼠标点击
	const sele1 = await page.$('#iphone-bd1 > dl:nth-child(1)');
	await sele1.click();
	await page.waitFor(2000);

	//鼠标滚动
	let element  = await page.$("#iphone-bd4 > dl:nth-child(3)");
    let box = await element.boundingBox();
    const x = box.x + (box.width/2);
    const y = box.y + (box.height/2);
    await page.mouse.move(x,y);
    await page.waitFor(10000);


	let Case_02_Act = await page.$eval('#engage-promo__v1-common > div > div > a', el => el.innerText);
	log(Case_02_Act)
	if ( Case_02_Act == 'Close'){
		log('检查点匹配')
	}
	else {
		log('检查点不匹配')
	}


	await browser.close();

})();




