
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
	Case_02: 'dd_auto_jp210',   // 空间名
	Case_03: 'Account Settings',  // 账户设置
	Case_04: 'dd_auto_jp210@mailinator.com',  // 账户设置弹框的邮件
	Case_06: 'dd_auto_jp210',  // 空间详情，General的空间名称
	Case_07: 'Invite space members',  // 空间详情，Memeber的邀请空间成员按钮
	Case_08: 'Hobby',  // 空间详情，Plan的套餐名：Hobby
	Case_09: '9980', // 报价单，年付，Business报价：9980
	Case_10: '12980', // 报价单，月付，Business报价：12980
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
		const Case_01 = 'Case_01: Access login page. Capture [dd_ui_login.jpg]';
		log(Case_01);
		await page.goto('https://dashv2.datadeck.com/login');
		await page.waitForSelector('.pt-ui-button__text');
		const documentSize = await page.evaluate(() => {
			return {
				width: document.documentElement.clientWidth,
				height: document.body.clientHeight,
			}
		});
		await page.screenshot({
			path: './pic/dd_ui_login.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_02
		const Case_02 = 'Case_02: Login Datadeck use [dd_auto_jp210@mailinator.com], check Space_Name. Excepted: ' + exp.Case_02;
		log(Case_02);
		await page.type('[name=email]', 'dd_auto_jp210@mailinator.com', {delay: 20});
		await page.type('[name=userPassword]', '123456', {delay: 20});
		const authLogin = await page.$('.pt-ui-button');
		await authLogin.click();
		await page.waitForSelector('.pt-account__title');
		let Case_02_Act = await page.$eval('.pt-account > div > h1', el => el.innerText);
		let Case_02_Res = 'Case_02_Res: ' + cps(exp.Case_02, Case_02_Act);
		log(Case_02_Res);
		await page.waitFor(1000);

		// Case_03
		const Case_03 = 'Case_03: Check Account_Menu. Capture [dd_ui_Account_menu.jpg]. Excepted: ' + exp.Case_03;
		log(Case_03);
		const Space_Name = await page.$('.pt-account__title');
		await Space_Name.click();
		await page.waitForSelector('.account-menu__item.account');
		let Case_03_Act = await page.$eval('.account-menu__item.account', el => el.innerText);
		let Case_03_Res = 'Case_03_Res: ' + cps(exp.Case_03, Case_03_Act);
		log(Case_03_Res);
		await page.screenshot({
			path: './pic/dd_ui_Account_menu.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_04
		const Case_04 = 'Case_04: Check Account_Settings window. Capture [dd_ui_Account_Settings_window.jpg]. Excepted: ' + exp.Case_04;
		log(Case_04);
		const Account_Settings = await page.$('.account-menu__item.account');
		await Account_Settings.click();
		await page.waitForSelector('.account-profile__info-email > div > div > div > div.content');
		let Case_04_Act = await page.$eval('.account-profile__info-email > div > div > div > div.content', el => el.innerText);
		let Case_04_Res = 'Case_04_Res: ' + cps(exp.Case_04, Case_04_Act);
		log(Case_04_Res);
		await page.screenshot({
			path: './pic/dd_ui_Account_Settings_window.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_05
		const Case_05 = 'Case_05: Click Close icon to close Account_Settings window';
		log(Case_05);
		const Account_Settings_Close = await page.$('.pt-popupv2__close');
		await Account_Settings_Close.click();

		// Case_06
		const Case_06 = 'Case_06: Check Space_Details_General page. Capture [dd_ui_Space_Details_General.jpg]. Excepted: ' + exp.Case_06;
		log(Case_06);
		const Space_Name_2 = await page.$('.pt-account__title');
		await Space_Name_2.click();
		await page.waitForSelector('.account-menu > div:nth-child(5)');
		const Space_Details = await page.$('.account-menu > div:nth-child(5)');
		await Space_Details.click();
		await page.waitForSelector('.space-general__wrap > div:nth-child(1) > div.space-general__item-container > div > input');
		let Case_06_Act = await page.$eval('.space-general__wrap > div:nth-child(1) > div.space-general__item-container > div > input', el => el.value);
		let Case_06_Res = 'Case_06_Res: ' + cps(exp.Case_06, Case_06_Act);
		log(Case_06_Res);
		await page.screenshot({
			path: './pic/dd_ui_Space_Details_General.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_07
		const Case_07 = 'Case_07: Check Space_Details_Members page. Capture [dd_ui_Space_Details_Members.jpg]. Excepted: ' + exp.Case_07;
		log(Case_07);
		const Space_Details_Members = await page.$('.space-detail > div.pt-menu > div > div > ul > li:nth-child(2)');
		await Space_Details_Members.click();
		await page.waitForSelector('.space-detail__container-content > div > div.pt-myteam__header > button > span');
		let Case_07_Act = await page.$eval('.space-detail__container-content > div > div.pt-myteam__header > button', el => el.innerText);
		let Case_07_Res = 'Case_07_Res: ' + cps(exp.Case_07, Case_07_Act);
		log(Case_07_Res);
		await page.screenshot({
			path: './pic/dd_ui_Space_Details_Members.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_08
		const Case_08 = 'Case_08: Check Space_Details_Plan page. Capture [dd_ui_Space_Details_Plan.jpg]. Excepted: ' + exp.Case_08;
		log(Case_08);
		const Space_Details_Plan = await page.$('.space-detail > div.pt-menu > div > div > ul > li:nth-child(3)');
		await Space_Details_Plan.click();
		await page.waitForSelector('.plan-usage__wrap > div:nth-child(1) > div:nth-child(1) > h3 > b');
		let Case_08_Act = await page.$eval('.plan-usage__wrap > div:nth-child(1) > div:nth-child(1) > h3 > b', el => el.innerText);
		let Case_08_Res = 'Case_08_Res: ' + cps(exp.Case_08, Case_08_Act);
		log(Case_08_Res);
		await page.screenshot({
			path: './pic/dd_ui_Space_Details_Plan.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_09
		const Case_09 = 'Case_09: Check Plan_List_Yearly page. Capture [dd_ui_Plan_List_Yearly.jpg]. Excepted: ' + exp.Case_09;
		log(Case_09);
		const Space_Name_3 = await page.$('.pt-account__title');
		await Space_Name_3.click();
		await page.waitForSelector('.account-menu');
		const Upgrade_Plan = await page.$('.account-menu > div:nth-child(6)');
		await Upgrade_Plan.click();
		await page.waitForSelector('.pt-plan-menu > div > div > div > ul');
		let Case_09_Act = await page.$eval('.pt-plan__plans.has_4_plan > div:nth-child(3) > div.pt-plan-card-price > span.pt-plan-card-price__amount', el => el.innerText);
		let Case_09_Res = 'Case_09_Res: ' + cps(exp.Case_09, Case_09_Act);
		log(Case_09_Res);
		await page.screenshot({
			path: './pic/dd_ui_Plan_List_Yearly.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_10
		const Case_10 = 'Case_10: Check Plan_List_Monthly page. Capture [dd_ui_Plan_List_Monthly.jpg]. Excepted: ' + exp.Case_10;
		log(Case_10);
		const Plan_List_Monthly = await page.$('.pt-plan-menu > div > div > div > ul > li:nth-child(1)');
		await Plan_List_Monthly.click();
		await page.waitForSelector('.pt-plan-menu > div > div > div > ul');
		let Case_10_Act = await page.$eval('.pt-plan__plans.has_4_plan > div:nth-child(3) > div.pt-plan-card-price > span.pt-plan-card-price__amount', el => el.innerText);
		let Case_10_Res = 'Case_10_Res: ' + cps(exp.Case_10, Case_10_Act);
		log(Case_10_Res);
		await page.screenshot({
			path: './pic/dd_ui_Plan_List_Monthly.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_11
		const Case_11 = 'Case_11: Click Back to back Home Page.';
		log(Case_11);
		const Plan_Back = await page.$('.pt-plan__header > a > span');
		await Plan_Back.click();
		await page.waitForSelector('.pt-account__title');

		// Case_12
		const Case_12 = 'Case_12: Check Log_Out page. Capture [dd_ui_Log_Out.jpg]. ';
		log(Case_12);
		const Space_Name_4 = await page.$('.pt-account__title');
		await Space_Name_4.click();
		await page.waitForSelector('.account-menu');
		const Log_Out = await page.$('.account-menu__item.last-child');
		await Log_Out.click();
		await page.waitForSelector('.pt-ui-button__text');
		await page.screenshot({
			path: './pic/dd_ui_Log_Out.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Log
		const log_server_1 = 'log_server_1: 【AT_DD_Online_UI_Account】 runs Finished.';
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
			+ Case_06 + '\r\n'
			+ Case_06_Res + '\r\n'
			+ Case_07 + '\r\n'
			+ Case_07_Res + '\r\n'
			+ Case_08 + '\r\n'
			+ Case_08_Res + '\r\n'
			+ Case_09 + '\r\n'
			+ Case_09_Res + '\r\n'
			+ Case_10 + '\r\n'
			+ Case_10_Res + '\r\n'
			+ Case_11 + '\r\n'
			+ Case_12 + '\r\n'
			+ log_server_1 + '\r\n', 'UTF8');
		writerStream.end();

	} catch (e) {
		if (e instanceof TimeoutError) {
			console.error(e);
			const log_block = 'Log_Block: Service unexpected termination! 【AT_DD_Online_UI_Account】 runs Error!';
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




