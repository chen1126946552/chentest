
const puppeteer = require('puppeteer');
const devices = require('puppeteer/DeviceDescriptors');
const {TimeoutError} = require('puppeteer/Errors');  // Error handling
const fs = require('fs');
const log = console.log;  // 缩写 console.log

function cps(Exp, Act) {
	if (Exp === Act) {
		return '检查点匹配'
	}
	else {
		return '检查点不匹配'
	}
}

let exp = {
	Case_02: 'Auto_panel_MySQL',
	Case_03: 'Auto_widget_MySQL_H_勿删',
	Case_04: '3.36',
};

(async () => {
	const browser = await puppeteer.launch({
		args: ['--no-sandbox', '--disable-setuid-sandbox'],
		ignoreHTTPSErrors: true,
		devtools: false,
		headless: false,
		defaultViewport: {width:1366, height:768},
		timeout: 30000,
	});
	const log_server_0 = 'Log_server_0: [AT_DD_Online_UI_SharePanel_iphone8] Service start-up.';
	log(log_server_0);

	try {
		const page = await browser.newPage();
		await page.emulate(devices['iPhone 8']);

		// Run Case
		const shareURL = 'https://dashv2.datadeck.com/share-panel.html?id=6f191eea-14e0-421d-ac1d-c4add2a961a9';


		// Case_01
		const Case_01 = 'Case_01: Access share-panel URL. URL: ' + shareURL;
		log(Case_01);
		await page.goto(shareURL);
		await page.waitForSelector('.pt-table__thead__tr-th-content');
		await page.waitFor(2000);
		const documentSize = await page.evaluate(() => {
			return {
				width: document.documentElement.clientWidth,
				height: document.body.clientHeight,
			}
		});


		// Case_02
		const Case_02 = 'Case_02: Check Panel_Name. Excepted: ' + exp.Case_02;
		log(Case_02);
		await page.waitForSelector('.share-dashboard__header-title');
		let Case_02_Act = await page.$eval('.share-dashboard__header-title', el => el.innerText);
		let Case_02_Res = 'Case_02_Res: ' + cps(exp.Case_02, Case_02_Act);
		log(Case_02_Res);


		// Case_03
		const Case_03 = 'Case_03: Check Widget_Name. Excepted: ' + exp.Case_03;
		log(Case_03);
		await page.waitForSelector('.pt-widget__header > div.widget__header-flex-wrap.pt-tooltip > div');
		let Case_03_Act = await page.$eval('.pt-widget__header > div.widget__header-flex-wrap.pt-tooltip > div', el => el.innerText);
		let Case_03_Res = 'Case_03_Res: ' + cps(exp.Case_03, Case_03_Act);
		log(Case_03_Res);


		// Case_04
		const Case_04 = 'Case_04: Check Widget_Value. Excepted: ' + exp.Case_04;
		log(Case_04);
		await page.waitForSelector('.widget__header__total > div.widget__header__total-amount');
		let Case_04_Act = await page.$eval('.widget__header__total > div.widget__header__total-amount', el => el.innerText);
		let Case_04_Res = 'Case_04_Res: ' + cps(exp.Case_04, Case_04_Act);
		log(Case_04_Res);


		// Capture
		await page.screenshot({
			path: './pic/dd_ui_share_panel_iphone8.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:documentSize.width, height:documentSize.height
			}
			});

		const log_server_1 = 'log_server_1: [AT_DD_Online_UI_SharePanel_iPhone8] runs Finished.';
		log(log_server_1);


		// Write Log
		let writerStream = fs.createWriteStream('./log/dd_ui_log.txt');
		writerStream.write(log_server_0 + '\r\n'
			+ Case_01 + '\r\n'
			+ Case_02 + '\r\n'
			+ Case_02_Res + '\r\n'
			+ Case_03 + '\r\n'
			+ Case_03_Res + '\r\n'
			+ Case_04 + '\r\n'
			+ Case_04_Res + '\r\n'
			+ log_server_1, 'UTF8');
		writerStream.end();

	} catch (e) {
		if (e instanceof TimeoutError) {
			console.error(e);
			const log_block = 'Log_Block: Service unexpected termination! [AT_DD_Online_UI_SharePanel_iPhone8] runs Error!';
			log(log_block);

			let writerStream = fs.createWriteStream('./log/dd_ui_log.txt');
			writerStream.write(log_block, 'UTF8');
			writerStream.end();
		}
	} finally {
		// exit
		await browser.close();
	}
})();




