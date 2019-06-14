
const puppeteer = require('puppeteer');
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
	Case_01: 'Let’s create your first dashboard',   // 面板空白页引导提示标题
	Case_02: 'Let\'s create\nyour first card',  // 新建面板，创建新Card引导提示
	Case_03: 'What data would you like to use?',  // 选择数据源页面，标题内容
	Case_04: 'What metrics would you like to see?',  // 选择Widget Demo页面，标题内容
	Case_04_1: 'New User Trend',  // 选择的Demo_Widget名
	Case_05: 'New User Trend',  // 新Widget名称
	Case_06: 'Delete card',  // 删除Widget提示框标题
	Case_07: 'Delete dashboard',  // 删除Panel提示框标题
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
	const log_server_0 = 'Log_server_0: Service start-up.';
	log(log_server_0);

	try {
		const page = await browser.newPage();

		// Case_01
		const Case_01 = 'Case_01: Login Datadeck dd_auto_jp210@mailinator.com. Capture [dd_ui_Dashboards_Blank]. Excepted: ' + exp.Case_01;
		log(Case_01);
		await page.goto('https://dashv2.datadeck.com/login');
		await page.waitForSelector('.pt-ui-button__text');
		const documentSize = await page.evaluate(() => {
			return {
				width: document.documentElement.clientWidth,
				height: document.body.clientHeight,
			}
		});
		await page.type('[name=email]', 'dd_auto_jp210@mailinator.com', {delay: 20});
		await page.type('[name=userPassword]', '123456', {delay: 20});
		const authLogin = await page.$('.pt-ui-button');
		await authLogin.click();

		
		await page.waitForSelector('.pt-main__content-tips-item > button');
		let Case_01_Act = await page.$eval('.pt-main__content-tips-item-title', el => el.innerText);
		let Case_01_Res = 'Case_01_Res: ' + cps(exp.Case_01, Case_01_Act);
		log(Case_01_Res);
		await page.waitFor(1000);
		await page.screenshot({
			path: './pic/dd_ui_Dashboards_Blank.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_02
		const Case_02 = 'Case_02: Check create panel. Capture [dd_ui_Dashboard_Create.jpg]. Excepted: ' + exp.Case_02;
		log(Case_02);
		const Dashboard_Create = await page.$('.pt-main__content-tips-item > button');
		await Dashboard_Create.click();
		await page.waitForSelector('.pt-main__content-tips-btns-new');
		let Case_02_Act = await page.$eval('.pt-main__content-tips-btns-new > div', el => el.innerText);
		let Case_02_Res = 'Case_02_Res: ' + cps(exp.Case_02, Case_02_Act);
		log(Case_02_Res);
		await page.screenshot({
			path: './pic/dd_ui_Dashboard_Create.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		

		// Case_03
		const Case_03 = 'Case_03: Check Widget_Select_DS page. Capture [dd_ui_Widget_Select_DS.jpg]. Excepted: ' + exp.Case_03;
		log(Case_03);
		const Widget_Create = await page.$('.pt-main__content-tips-btns-new > button');
		await Widget_Create.click();
		await page.waitForSelector('#ds-card__googleanalytics-v4');
		let Case_03_Act = await page.$eval('.datasource-choose__header > div > div.title', el => el.innerText);
		let Case_03_Res = 'Case_03_Res: ' + cps(exp.Case_03, Case_03_Act);
		log(Case_03_Res);
		await page.screenshot({
			path: './pic/dd_ui_Widget_Select_DS.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_04
		const Case_04 = 'Case_04: Check Widget_Select_Metrics page. Capture [dd_ui_Widget_Select_Widget_Demo.jpg]. Excepted: ' + exp.Case_04 + ' ' + exp.Case_04_1;
		log(Case_04);
		const Widget_Select_DS = await page.$('.dashboard > div.widget-editor__datasource > div.datasource-choose > div.datasource-choose__container > div > div.datasource-choose__quick > ul > li');
		await Widget_Select_DS.click();
		await page.waitForSelector('.datasource-template__container > div.scrollbar__holder.ps-container.ps-theme-light.ps.ps--active-y > ul > li:nth-child(2)');
		let Case_04_Act = await page.$eval('.datasource-template__header > div > div.title', el => el.innerText);
		let Case_04_Res = 'Case_04_Res: ' + cps(exp.Case_04, Case_04_Act);
		log(Case_04_Res);
		let Case_04_1_Act = await page.$eval('.datasource-template__container > div.scrollbar__holder.ps-container.ps-theme-light.ps.ps--active-y > ul > li:nth-child(2) > div.template-card__footer > div', el => el.innerText);
		let Case_04_1_Res = 'Case_04_1_Res: ' + cps(exp.Case_04_1, Case_04_1_Act);
		log(Case_04_1_Res);
		await page.screenshot({
			path: './pic/dd_ui_Widget_Select_Widget_Demo.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		
		// Case_05
		const Case_05 = 'Case_05: Check Select_Account&Profile_windows. Capture [dd_ui_Widget_Connect_DS_Window.jpg]. Excepted: ' + exp.Case_05;
		log(Case_05);
		const Widget_Select_DemoCard = await page.$('.datasource-template__container > div.scrollbar__holder.ps-container.ps-theme-light.ps.ps--active-y > ul > li:nth-child(2)');
		await Widget_Select_DemoCard.click();
		const Widget_Select_DemoCard_Create = await page.$('.datasource-template__header > div > div.search > button');
		await Widget_Select_DemoCard_Create.click();		
		await page.waitFor(2000);
		await page.waitForSelector('.pt-widget.pt-widget__clear-overflow > div.pt-widget__body > div > div');
		let Case_05_Act = await page.$eval('.pt-widget__header > div.widget__header-flex-wrap.pt-tooltip > div > span', el => el.innerText);
		let Case_05_Res = 'Case_05_Res: ' + cps(exp.Case_05, Case_05_Act);
		log(Case_05_Res);
		await page.screenshot({
			path: './pic/dd_ui_Widget_Create_Done.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});
			

		// Case_06
		const Case_06 = 'Case_06: Delete new Widget. Excepted: ' + exp.Case_06;
		log(Case_06);
		await page.waitForSelector('.pt-widget.pt-widget__clear-overflow > div.pt-widget__header > div.widget__tools');
		const Widget_More = await page.$('.pt-widget.pt-widget__clear-overflow > div.pt-widget__header > div.widget__tools');
		await Widget_More.click();
		await page.waitFor(2000);
		await page.waitForSelector('.pt-widget.pt-widget__clear-overflow > div.pt-widget__header > div.widget__tools > a > div > ul > li:nth-child(12)');
		const Widget_Delete = await page.$('.pt-widget.pt-widget__clear-overflow > div.pt-widget__header > div.widget__tools > a > div > ul > li:nth-child(12)');
		await Widget_Delete.click();
		await page.waitFor(1000);
		await page.waitForSelector('.pt-popupv2__content.is-middle > footer > button');
		let Case_06_Act = await page.$eval('.pt-popupv2__content.is-middle > header > h3 > span', el => el.innerText);
		let Case_06_Res = 'Case_06_Res: ' + cps(exp.Case_06, Case_06_Act);
		log(Case_06_Res);
		const Widget_Delete_Remove = await page.$('.pt-popupv2__content.is-middle > footer > button');
		await Widget_Delete_Remove.click();
		await page.waitFor(1000);
	

		// Case_07
		const Case_07 = 'Case_07: Delete new Dashboards. Excepted: ' + exp.Case_07;
		log(Case_07);
		const Panel_Back = await page.$('.pt-main__header > div.pt-main__header-packup > a > span');
		await Panel_Back.click();
		await page.waitFor(1000);
		await page.reload();
		await page.waitForSelector('.panel-tree > div > div.panel-tree__inner.can_drop > div > div > div:nth-child(2) > a > div.tools > div > svg');
		const Panel_More = await page.$('.panel-tree > div > div.panel-tree__inner.can_drop > div > div > div:nth-child(2) > a > div.tools > div > svg');
		await Panel_More.click();
		const Panel_Delete = await page.$('.pt-main__content > div:nth-child(1) > div > div.dashboardlist-wrap > div.pt-menu__content > div > div > div.pt-panel__tools > a:nth-child(5)');
		await Panel_Delete.click();
		await page.waitFor(1000);
		await page.waitForSelector('.pt-popupv2__content.is-middle > footer > button');
		let Case_07_Act = await page.$eval('.pt-popupv2__content.is-middle > header > h3 > span', el => el.innerText);
		let Case_07_Res = 'Case_07_Res: ' + cps(exp.Case_07, Case_07_Act);
		log(Case_07_Res);
		const Panel_Delete_Remove = await page.$('.pt-popupv2__content.is-middle > footer > button');
		await Panel_Delete_Remove.click();
		await page.waitFor(1000);
		await page.waitForSelector('.pt-main__content > div:nth-child(1) > div.pt-main__content-tips > div.pt-main__content-tips-wrap > div.pt-main__content-tips-item > button');
		
		// log
		const log_server_1 = 'log_server_1: 【AT_DD_Online_UI_Dashboard】 runs Finished.';
		log(log_server_1);

		let writerStream = fs.createWriteStream('./log/dd_ui_log.txt');
		writerStream.write(log_server_0 + '\r\n'
			+ Case_01 + '\r\n'
			+ Case_01_Res + '\r\n'
			+ Case_02 + '\r\n'
			+ Case_02_Res + '\r\n'
			+ Case_03 + '\r\n'
			+ Case_03_Res + '\r\n'
			+ Case_04 + '\r\n'
			+ Case_04_Res + '\r\n'
			+ Case_04_1_Res + '\r\n'
			+ Case_05 + '\r\n'
			+ Case_05_Res + '\r\n'
			+ Case_06 + '\r\n'
			+ Case_06_Res + '\r\n'
			+ Case_07 + '\r\n'
			+ Case_07_Res + '\r\n'
			+ log_server_1 + '\r\n', 'UTF8');
		writerStream.end();

	} catch (e) {
		if (e instanceof TimeoutError) {
			console.error(e);
			const log_block = 'Log_Block: Service unexpected termination! 【AT_DD_Online_UI_Dashboard】 runs Error!';
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




