
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
	Case_02: 'Subscribe to cards.\nGet notified automatically.',   // Subscriptions空白页，引导提示标题
	Case_02_1: 'Create a Subscription',  // Subscriptions空白页，存在 Create a Subscription 按钮
	Case_03: 'Add alert',  // Alerts Sheet页，按钮名称
	Case_04: 'Create your subscription',  // 创建订阅弹框标题
	Case_05: 'New User Trend', // 已订阅的标题名称
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
		const Case_01 = 'Case_01: Login Datadeck dd_auto_jp213@mailinator.com.';
		log(Case_01);
		await page.goto('https://dashv2.datadeck.com/login');
		await page.waitForSelector('.pt-ui-button__text');
		const documentSize = await page.evaluate(() => {
			return {
				width: document.documentElement.clientWidth,
				height: document.body.clientHeight,
			}
		});
		await page.type('[name=email]', 'dd_auto_jp213@mailinator.com', {delay: 20});
		await page.type('[name=userPassword]', '123456', {delay: 20});
		const authLogin = await page.$('.pt-ui-button');
		await authLogin.click();
		await page.waitForSelector('#app > div > div.pt-main__aside.pt-main__aside > div > div > div.pt-account');
		await page.waitFor(3000);

		// Case_02
		const Case_02 = 'Case_02: Check Preferences_Subscriptions_Blank page. Capture [dd_ui_Preferences_Subscriptions_Blank.jpg]. Excepted: ' + exp.Case_02;
		log(Case_02);
		await page.waitForSelector('.linkList > a.item.preferences > div');
		const Preferences_Item = await page.$('.linkList > a.item.preferences > div');
		await Preferences_Item.click();
		await page.waitFor(1000);
		await page.waitForSelector('.subscribe > div > div > div.pt-main__content-tips-item > div.pt-main__content-tips-item-title');
		let Case_02_Act = await page.$eval('.subscribe > div > div > div.pt-main__content-tips-item > div.pt-main__content-tips-item-title', el => el.innerText);
		let Case_02_Res = 'Case_02_Res: ' + cps(exp.Case_02, Case_02_Act);
		log(Case_02_Res);
		await page.waitForSelector('.subscribe > div > div > div.pt-main__content-tips-item > button > span');
		let Case_02_1_Act = await page.$eval('.subscribe > div > div > div.pt-main__content-tips-item > button > span', el => el.innerText);
		let Case_02_1_Res = 'Case_02_1_Res: ' + cps(exp.Case_02_1, Case_02_1_Act);
		log(Case_02_1_Res);
		await page.screenshot({
			path: './pic/dd_ui_Preferences_Subscriptions_Blank.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_03
		const Case_03 = 'Case_03: Check Preferences_Extras page. Capture [dd_ui_Preferences_Extras.jpg]. Excepted: ' + exp.Case_03;
		log(Case_03);
		await page.waitForSelector('.pt-main__content > div:nth-child(1) > div > div.pt-menu > div > div > ul > li:nth-child(2)');
		const Preferences_Extras_Sheet = await page.$('.pt-main__content > div:nth-child(1) > div > div.pt-menu > div > div > ul > li:nth-child(2)');
		await Preferences_Extras_Sheet.click();
		await page.waitFor(1000);
		await page.waitForSelector('.pt-main__content > div:nth-child(1) > div > div.dal > div > div > div.pt-main__content-tips-item > button > span');
		let Case_03_Act = await page.$eval('.pt-main__content > div:nth-child(1) > div > div.dal > div > div > div.pt-main__content-tips-item > button > span', el => el.innerText);
		let Case_03_Res = 'Case_03_Res: ' + cps(exp.Case_03, Case_03_Act);
		log(Case_03_Res);
		await page.screenshot({
			path: './pic/dd_ui_Preferences_Extras.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_04
		const Case_04 = 'Case_04: Check Create_Your_Subscription window. Capture [dd_ui_Create_Your_Subscription.jpg]. Excepted: ' + exp.Case_04;
		log(Case_04);
		// 点击 Dashboards 菜单项
		await page.waitForSelector('.linkList > a.item.dashboards > div');
		const Dashboards_Item = await page.$('.linkList > a.item.dashboards > div');
		await Dashboards_Item.click();
		await page.waitFor(1000);
		// 点击 Favorites 标签页
		await page.waitForSelector('.dashboardlist-wrap > div.pt-menu > div > div > ul > li:nth-child(2)');
		const Dashboards_Favorites_Sheet = await page.$('.dashboardlist-wrap > div.pt-menu > div > div > ul > li:nth-child(2)');
		await Dashboards_Favorites_Sheet.click();
		await page.waitFor(1000);
		// 进入 Auto_panel_GA 面板
		await page.waitForSelector('.panel-tree > div > div.panel-tree__inner > div > div > div:nth-child(2) > a > div.node-name.folder-icon > div.name > span');
		const Panel_Auto_panel_GA = await page.$('.panel-tree > div > div.panel-tree__inner > div > div > div:nth-child(2) > a > div.node-name.folder-icon > div.name > span');
		await Panel_Auto_panel_GA.click();
		await page.waitFor(1000);
		// 点击 New User Trend Widget更多按钮
		await page.waitForSelector('.fg-container > div > div:nth-child(1) > div > div.pt-widget.pt-widget__clear-overflow > div.pt-widget__header > div.widget__tools');
		const Widget_More = await page.$('.fg-container > div > div:nth-child(1) > div > div.pt-widget.pt-widget__clear-overflow > div.pt-widget__header > div.widget__tools');
		await Widget_More.click();
		await page.waitFor(2000);
		// 点击 Subscribe 项
		await page.waitForSelector('.pt-widget.pt-widget__clear-overflow > div.pt-widget__header > div.widget__tools > a > div > ul > li:nth-child(3)');
		const Widget_Subscribe = await page.$('.pt-widget.pt-widget__clear-overflow > div.pt-widget__header > div.widget__tools > a > div > ul > li:nth-child(3)');
		await Widget_Subscribe.click();
		await page.waitFor(5000);
		await page.waitForSelector('.highcharts-axis-labels.highcharts-yaxis-labels');
		// 进入 创建订阅 弹框
		let Case_04_Act = await page.$eval('.pt-main__content > div.dashboard > div.pt-popupv2 > div > div.pt-popupv2__content.is-middle.subscribe-popup > header > h3 > span', el => el.innerText);
		let Case_04_Res = 'Case_04_Res: ' + cps(exp.Case_04, Case_04_Act);
		log(Case_04_Res);
		await page.screenshot({
			path: './pic/dd_ui_Create_Your_Subscription.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_05
		const Case_05 = 'Case_05: Check Subscription_New. Capture [dd_ui_Subscription_New.jpg]. Excepted: ' + exp.Case_05;
		log(Case_05);
		// 添加新订阅记录
		await page.waitForSelector('.dashboard > div.pt-popupv2 > div > div.pt-popupv2__content.is-middle.subscribe-popup > footer > button');
		const Save_Subscription = await page.$('.dashboard > div.pt-popupv2 > div > div.pt-popupv2__content.is-middle.subscribe-popup > footer > button');
		await Save_Subscription.click();
		await page.waitFor(3000);
		// 点击 Preferences 菜单项
		await page.waitForSelector('.linkList > a.item.preferences > div');
		const Preferences_Item_2 = await page.$('.linkList > a.item.preferences > div');
		await Preferences_Item_2.click();
		await page.waitFor(3000);
		// 检查存在新的订阅记录
		await page.waitForSelector('.subscribe > content > div > dl > dd.list-item__title > div.selected_widget_title > div');
		let Case_05_Act = await page.$eval('.subscribe > content > div > dl > dd.list-item__title > div.selected_widget_title > div', el => el.innerText);
		log(Case_05_Act);
		let Case_05_Res = 'Case_05_Res: ' + cps(exp.Case_05, Case_05_Act);
		log(Case_05_Res);
		await page.screenshot({
			path: './pic/dd_ui_Subscription_New.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_06
		const Case_06 = 'Case_06: Check Remove_Subscription_New. ';
		log(Case_06);
		// 点击订阅记录更多按钮
		await page.waitForSelector('.subscribe > content > div > dl > dd.list-item__tool > div > div:nth-child(1)');
		const Subscription_More = await page.$('.subscribe > content > div > dl > dd.list-item__tool > div > div:nth-child(1)');
		await Subscription_More.click();
		// 点击Remove
		await page.waitForSelector('.subscribe > content > div > dl > dd.list-item__tool > div > div.more > ul > li:nth-child(2)');
		const Subscription_Remove = await page.$('.subscribe > content > div > dl > dd.list-item__tool > div > div.more > ul > li:nth-child(2)');
		await Subscription_Remove.click();
		await page.waitFor(3000);

		// log
		const log_server_1 = 'log_server_1: 【AT_DD_Online_UI_Preferences】 runs Finished.';
		log(log_server_1);

		let writerStream = fs.createWriteStream('./log/dd_ui_log.txt');
		writerStream.write(log_server_0 + '\r\n'
			+ Case_01 + '\r\n'
			+ Case_02 + '\r\n'
			+ Case_02_Res + '\r\n'
			+ Case_02_1_Res + '\r\n'
			+ Case_03 + '\r\n'
			+ Case_03_Res + '\r\n'
			+ Case_04 + '\r\n'
			+ Case_04_Res + '\r\n'
			+ Case_05 + '\r\n'
			+ Case_05_Res + '\r\n'
			+ log_server_1 + '\r\n', 'UTF8');
		writerStream.end();

	} catch (e) {
		if (e instanceof TimeoutError) {
			console.error(e);
			const log_block = 'Log_Block: Service unexpected termination! 【AT_DD_Online_UI_Preferences】 runs Error!';
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




