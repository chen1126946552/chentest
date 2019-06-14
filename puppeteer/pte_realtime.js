
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



    //新打开页签,访问ptengine查看Real-time中存在该访问
    const page2 = await browser.newPage();

    const Case_02 = '登录ptengine';
	log(Case_02);
	
	await page2.goto('https://reportv3.ptengine.jp');
	await page2.waitFor(5000);

	await page2.type('[name=username]', 'chen.chen@ptmind.com', {delay: 20});
	await page2.type('[name=password]', 'ptmind2008', {delay: 20});
	const authLogin = await page2.$('#pt-loginForm > div:nth-child(5) > button');
	await authLogin.click();
	log('登录')
	await page2.waitFor(3000);
	await page2.waitForSelector('#app > div > div > div.wrap > div.pt-homepage--left > div.pt-fl.pt-homepage--quick > div.pt-homepage--quick__top.pt-flex > div.flex--item.pt-tr > p > a')
	
	const profileSetting = await page2.$('#app > div > div > div.wrap > div.pt-homepage--left > div.pt-fl.pt-homepage--quick > div.pt-homepage--quick__top.pt-flex > div.flex--item.pt-tr > p > a')
	await profileSetting.click();
	await page2.waitFor(5000);
	log('点击profile设置')


	const realTime = await page2.$('body > div.ng-scope > div.js-pt-main-outward.pt-main.ng-scope.pt-container-outward-setting > header > div > nav > div > ul > li:nth-child(6) > a')
	await realTime.click();
	await page2.waitFor(5000);
	log('点击realtime')


	let Case_02_Act = await page2.$eval('body > div.ng-scope > div.js-pt-main-outward.pt-main.ng-scope.pt-container-outward-timeclips > div.pt-container-fluid.js-container-fluid > div.pt-tab-content.pt-tab-content-margin-left-fat.js-pt-tab-content > div > div > div > div.pt-w50.pt-fl.pt-clear-padding.pt-tc-auto-block.pt-borderRight.ng-scope > div.pt-tc-overview-layout-row3.pt-borderBottom.clearfix > div:nth-child(1) > div > div.highlight.ng-binding', el => el.innerText);
	log(Number(Case_02_Act))
	if ( Number(Case_02_Act) > 0 ){
		log('检查点匹配')
	}
	else {
		log('检查点不匹配')
	}


	await browser.close();

})();




