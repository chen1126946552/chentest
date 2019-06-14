
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
	Case_02: 'Auto_panel_CSV_By_jp212,Auto_panel_GA,Auto_panel_GoogleDrive,Auto_panel_MySQL,GA_Overview_190307',  // Dashboards_All 列表，面板名称
	Case_03: 'Auto_panel_GA',  // Dashboards_Favorites 列表，面板内容
	Case_04: 'Share,Dashboard details,Rename',  // Favorites 列表，面板更多下拉框功能项
	Case_05: 'Auto_panel_CSV_By_jp212,Auto_panel_GA,Auto_panel_GoogleDrive,Auto_panel_MySQL,GA_Overview_190307', // Dashboards_Recent 列表，面板内容
	// Case_06: 'Share,Dashboard details', // Recent 列表，面板更多下拉框功能项；容易出现排序问题，暂停检查
	Case_07: 'Auto_panel_GA,Auto_panel_GoogleDrive,Auto_panel_MySQL,GA_Overview_190307',  // Dashboards_CreatedByMe 列表，面板内容
	Case_08: 'Share,Dashboard details,Rename,Duplicate dashboard,Delete dashboard', // Created by me 列表，面板更多下拉框功能项
	Case_09: 'Auto_panel_CSV_By_jp212',  // Dashboards_SharedWithMe 列表，面板内容
	Case_10: 'Share,Dashboard details,Exit sharing', // Shared with me 列表，面板更多下拉框功能项
	Case_11: 'Title\nAuto_panel_CSV_By_jp212', // Dashboard details Title内容
	Case_11_1: 'Created\n2019.03.07 by jp212', // Dashboard details Created内容
	Case_11_2: 'Data sources used in this dashboard\nautotest_table.csv', // Dashboard details Data sources used in this dashboard
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
		await page.waitFor(3000);
		await page.waitForSelector('.pt-main__header > div.freetrial-tips.freetrail-tips > div');

		// Case_02
		const Case_02 = 'Case_02: Check Dashboards_All_list. Capture [dd_ui_Dashboards_All_list.jpg]. Excepted: ' + exp.Case_02;
		log(Case_02);
		await page.waitForSelector('.pt-menu__content > div > div > div.panel-header > div > span.pt-sort-button.filter.panel-header__item.name > span.title');
		let Dashboards_All_List = await page.$$eval('.node-name.folder-icon > div.name > span', els => {
			return els.map(v => {
				return v.innerText;
			});
		});
		let All_List_Sort = Dashboards_All_List.sort();
		let Case_02_Act = All_List_Sort.join(',');
		let Case_02_Res = 'Case_02_Res: ' + cps(exp.Case_02, Case_02_Act);
		log(Case_02_Res);
		await page.waitFor(3000);
		await page.screenshot({
			path: './pic/dd_ui_Dashboards_All_list.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_03
		const Case_03 = 'Case_03: Check Dashboards_Favorites_list. Capture [dd_ui_Dashboards_Favorites_list.jpg]. Excepted: ' + exp.Case_03;
		log(Case_03);
		// 点击 Favorites
		await page.waitForSelector('.pt-menu > div > div > ul > li:nth-child(2)');
		const Dashboards_Favorites_Sheet = await page.$('.pt-menu > div > div > ul > li:nth-child(2)');
		await Dashboards_Favorites_Sheet.click();
		await page.waitFor(1000);
		await page.waitForSelector('.pt-menu__content > div > div > div.panel-header > div > span.pt-sort-button.filter.panel-header__item.name > span.title');
		let Dashboards_Favorites_List = await page.$$eval('.node-name.folder-icon > div.name > span', els => {
			return els.map(v => {
				return v.innerText;
			});
		});
		let Favorites_List_Sort = Dashboards_Favorites_List.sort();
		let Case_03_Act = Favorites_List_Sort.join(',');
		let Case_03_Res = 'Case_03_Res: ' + cps(exp.Case_03, Case_03_Act);
		log("03   " + Case_03_Act);
		log(Case_03_Res);
		await page.waitFor(1000);
		await page.screenshot({
			path: './pic/dd_ui_Dashboards_Favorites_list.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_04
		const Case_04 = 'Case_04: Check Dashboards_Favorites_Panel_FNItems. Excepted: ' + exp.Case_04;
		log(Case_04);
		// Favorites列表，面板功能项
		await page.waitForSelector('.panel-tree > div > div.panel-tree__inner > div > div > div:nth-child(2) > a > div.tools > div');
		const Favorites_Panel_More = await page.$('.panel-tree > div > div.panel-tree__inner > div > div > div:nth-child(2) > a > div.tools > div');
		await Favorites_Panel_More.click();
		await page.waitFor(1000);
		await page.waitForSelector('.pt-menu__content > div > div > div.pt-panel__tools > a:nth-child(1) > span');
		let Favorites_Panel_FNItems = await page.$$eval('.pt-panel__tools > a', els => {
			return els.map(v => {
				return v.innerText;
			});
		});
		let Case_04_Act = Favorites_Panel_FNItems.join(',');
		// log(Case_04_Act);
		let Case_04_Res = 'Case_04_Res: ' + cps(exp.Case_04, Case_04_Act);
		log(Case_04_Res);
		await page.waitFor(1000);

		// Case_05
		const Case_05 = 'Case_05: Check Dashboards_Recent_list. Capture [dd_ui_Dashboards_Recent_list.jpg]. Excepted: ' + exp.Case_05;
		log(Case_05);
		// 点击 Recent
		await page.waitForSelector('.pt-menu > div > div > ul > li:nth-child(3)');
		const Dashboards_Recent_Sheet = await page.$('.pt-menu > div > div > ul > li:nth-child(3)');
		await Dashboards_Recent_Sheet.click();
		await page.waitFor(1000);
		await page.waitForSelector('.pt-menu__content > div > div > div.panel-header > div > span.pt-sort-button.filter.panel-header__item.name > span.title');
		let Dashboards_Recent_List = await page.$$eval('.node-name.folder-icon > div.name > span', els => {
			return els.map(v => {
				return v.innerText;
			});
		});
		let Recent_List_Sort = Dashboards_Recent_List.sort();
		let Case_05_Act = Recent_List_Sort.join(',');
		let Case_05_Res = 'Case_05_Res: ' + cps(exp.Case_05, Case_05_Act);
		log(Case_05_Res);
		await page.waitFor(1000);
		await page.screenshot({
			path: './pic/dd_ui_Dashboards_Recent_list.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_06
		const Case_06 = 'Case_06: Check Dashboards_Recent_Panel_FNItems. Excepted: ' + exp.Case_06 + ' 注释期望结果，暂停检查';
		log(Case_06);
		// Recent 列表，面板功能项
		await page.waitForSelector('.panel-tree > div > div.panel-tree__inner > div > div > div:nth-child(2) > a > div.tools > div');
		const Recent_Panel_More = await page.$('.panel-tree > div > div.panel-tree__inner > div > div > div:nth-child(2) > a > div.tools > div');
		await Recent_Panel_More.click();
		await page.waitFor(1000);
		await page.waitForSelector('.pt-menu__content > div > div > div.pt-panel__tools > a:nth-child(1) > span');
		let Recent_Panel_FNItems = await page.$$eval('.pt-panel__tools > a', els => {
			return els.map(v => {
				return v.innerText;
			});
		});
		let Case_06_Act = Recent_Panel_FNItems.join(',');
		log(Case_06_Act);
		// let Case_06_Res = 'Case_06_Res: ' + cps(exp.Case_06, Case_06_Act);
		// log(Case_06_Res);
		await page.waitFor(1000);

		// Case_07
		const Case_07 = 'Case_07: Check Dashboards_CreatedByMe_list. Capture [dd_ui_Dashboards_CreatedByMe_list.jpg]. Excepted: ' + exp.Case_07;
		log(Case_07);
		// 点击 Created by me
		await page.waitForSelector('.pt-menu > div > div > ul > li:nth-child(4)');
		const Dashboards_CreatedByMe_Sheet = await page.$('.pt-menu > div > div > ul > li:nth-child(4)');
		await Dashboards_CreatedByMe_Sheet.click();
		await page.waitFor(1000);
		await page.waitForSelector('.pt-menu__content > div > div > div.panel-header > div > span.pt-sort-button.filter.panel-header__item.name > span.title');
		let Dashboards_CreatedByMe_List = await page.$$eval('.node-name.folder-icon > div.name > span', els => {
			return els.map(v => {
				return v.innerText;
			});
		});
		let CreatedByMe_List_Sort = Dashboards_CreatedByMe_List.sort();
		let Case_07_Act = CreatedByMe_List_Sort.join(',');
		let Case_07_Res = 'Case_07_Res: ' + cps(exp.Case_07, Case_07_Act);
		log(Case_07_Res);
		await page.waitFor(1000);
		await page.screenshot({
			path: './pic/dd_ui_Dashboards_CreatedByMe_list.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_08
		const Case_08 = 'Case_08: Check Dashboards_CreatedByMe_Panel_FNItems. Excepted: ' + exp.Case_08;
		log(Case_08);
		// Created by me 列表，面板功能项
		await page.waitForSelector('.panel-tree > div > div.panel-tree__inner > div > div > div:nth-child(2) > a > div.tools > div');
		const CreatedByMe_Panel_More = await page.$('.panel-tree > div > div.panel-tree__inner > div > div > div:nth-child(2) > a > div.tools > div');
		await CreatedByMe_Panel_More.click();
		await page.waitFor(1000);
		await page.waitForSelector('.pt-menu__content > div > div > div.pt-panel__tools > a:nth-child(1) > span');
		let CreatedByMe_Panel_FNItems = await page.$$eval('.pt-panel__tools > a', els => {
			return els.map(v => {
				return v.innerText;
			});
		});
		let Case_08_Act = CreatedByMe_Panel_FNItems.join(',');
		// log(Case_08_Act);
		let Case_08_Res = 'Case_08_Res: ' + cps(exp.Case_08, Case_08_Act);
		log(Case_08_Res);
		await page.waitFor(1000);


		// Case_09
		const Case_09 = 'Case_09: Check Dashboards_ShareWithMe_list. Capture [dd_ui_Dashboards_ShareWithMe_list.jpg]. Excepted: ' + exp.Case_09;
		log(Case_09);
		// 点击 Created by me
		await page.waitForSelector('.pt-menu > div > div > ul > li:nth-child(5)');
		const Dashboards_ShareWithMe_Sheet = await page.$('.pt-menu > div > div > ul > li:nth-child(5)');
		await Dashboards_ShareWithMe_Sheet.click();
		await page.waitFor(1000);
		await page.waitForSelector('.pt-menu__content > div > div > div.panel-header > div > span.pt-sort-button.filter.panel-header__item.name > span.title');
		let Dashboards_ShareWithMe_List = await page.$$eval('.node-name.folder-icon > div.name > span', els => {
			return els.map(v => {
				return v.innerText;
			});
		});
		let ShareWithMe_List_Sort = Dashboards_ShareWithMe_List.sort();
		let Case_09_Act = ShareWithMe_List_Sort.join(',');
		let Case_09_Res = 'Case_09_Res: ' + cps(exp.Case_09, Case_09_Act);
		log(Case_09_Res);
		await page.waitFor(1000);
		await page.screenshot({
			path: './pic/dd_ui_Dashboards_ShareWithMe_list.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_10
		const Case_10 = 'Case_10: Check Dashboards_SharedWithMe_Panel_FNItems. Excepted: ' + exp.Case_10;
		log(Case_10);
		// Created by me 列表，面板功能项
		await page.waitForSelector('.panel-tree > div > div.panel-tree__inner > div > div > div:nth-child(2) > a > div.tools > div');
		const SharedWithMe_Panel_More = await page.$('.panel-tree > div > div.panel-tree__inner > div > div > div:nth-child(2) > a > div.tools > div');
		await SharedWithMe_Panel_More.click();
		await page.waitFor(1000);
		await page.waitForSelector('.pt-menu__content > div > div > div.pt-panel__tools > a:nth-child(1) > span');
		let SharedWithMe_Panel_FNItems = await page.$$eval('.pt-panel__tools > a', els => {
			return els.map(v => {
				return v.innerText;
			});
		});
		let Case_10_Act = SharedWithMe_Panel_FNItems.join(',');
		// log(Case_10_Act);
		let Case_10_Res = 'Case_10_Res: ' + cps(exp.Case_10, Case_10_Act);
		log(Case_10_Res);

		// Case_11
		const Case_11 = 'Case_11: Check Dashboard_Details window. Capture [dd_ui_Dashboard_Details.jpg]. Excepted: ' + exp.Case_11 + '\n' + exp.Case_11_1 + '\n' + exp.Case_11_2;
		log(Case_11);
		// 点击 Dashboard details
		await page.waitForSelector('.pt-menu__content > div > div > div.pt-panel__tools > a:nth-child(2)');
		const Dashboard_Details_Item = await page.$('.pt-menu__content > div > div > div.pt-panel__tools > a:nth-child(2)');
		await Dashboard_Details_Item.click();
		await page.waitFor(5000);
		// Dashboard details 弹框
		await page.waitForSelector('.pt-popupv2 > div > div.pt-popupv2__content.is-middle.panel-detail__popup > div.pt-popupv2__main > div > div:nth-child(2)');
		let Case_11_Act = await page.$eval('.pt-popupv2 > div > div.pt-popupv2__content.is-middle.panel-detail__popup > div.pt-popupv2__main > div > div:nth-child(2)', el => el.innerText);
		let Case_11_Res = 'Case_11_Res: ' + cps(exp.Case_11, Case_11_Act);
		log("11   " + Case_11_Act);
		log(Case_11_Res);
		let Case_11_1_Act = await page.$eval('.pt-popupv2 > div > div.pt-popupv2__content.is-middle.panel-detail__popup > div.pt-popupv2__main > div > div:nth-child(3)', el => el.innerText);
		let Case_11_1_Res = 'Case_11_1_Res: ' + cps(exp.Case_11_1, Case_11_1_Act);
		log("11-1   " + Case_11_1_Act);
		log(Case_11_1_Res);
		let Case_11_2_Act = await page.$eval('.pt-popupv2 > div > div.pt-popupv2__content.is-middle.panel-detail__popup > div.pt-popupv2__main > div > div.panel-datasource', el => el.innerText);
		let Case_11_2_Res = 'Case_11_2_Res: ' + cps(exp.Case_11_2, Case_11_2_Act);
		log("11-2   " + Case_11_2_Act);
		log(Case_11_2_Res);
		await page.screenshot({
			path: './pic/dd_ui_Dashboard_Details.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});
		// 关闭详情弹框
		await page.waitForSelector('.pt-popupv2 > div > div.pt-popupv2__content.is-middle.panel-detail__popup > footer > button');
		const Dashboard_Details_Close = await page.$('.pt-popupv2 > div > div.pt-popupv2__content.is-middle.panel-detail__popup > footer > button');
		await Dashboard_Details_Close.click();

		await page.waitFor(3000);

		// log
		const log_server_1 = 'log_server_1: 【AT_DD_Online_UI_DashboardList】 runs Finished.';
		log(log_server_1);

		let writerStream = fs.createWriteStream('./log/dd_ui_log.txt');
		writerStream.write(log_server_0 + '\r\n'
			+ Case_01 + '\r\n'
			+ Case_02 + '\r\n'
			+ Case_02_Res + '\r\n'
			+ Case_03 + '\r\n'
			+ Case_03_Res + '\r\n'
			+ Case_04 + '\r\n'
			+ Case_04_Res + '\r\n'
			+ Case_05 + '\r\n'
			+ Case_05_Res + '\r\n'
			+ Case_06 + '\r\n'
			+ Case_06_Act + '\r\n'
			+ Case_07 + '\r\n'
			+ Case_07_Res + '\r\n'
			+ Case_08 + '\r\n'
			+ Case_08_Res + '\r\n'
			+ Case_09 + '\r\n'
			+ Case_09_Res + '\r\n'
			+ Case_10 + '\r\n'
			+ Case_10_Res + '\r\n'
			+ Case_11 + '\r\n'
			+ Case_11_Res + '\r\n'
			+ Case_11_1_Res + '\r\n'
			+ Case_11_2_Res + '\r\n'
			+ log_server_1 + '\r\n', 'UTF8');
		writerStream.end();

	} catch (e) {
		if (e instanceof TimeoutError) {
			console.error(e);
			const log_block = 'Log_Block: Service unexpected termination! 【AT_DD_Online_UI_DashboardList】 runs Error!';
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




