
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
	Case_03: 'Switch on the public share link and share the link with anyone who is not in your space. They can view this dashboard by clicking the link.',  // Public link 默认说明
	Case_04: 'on',  // 分享链接开关状态
	Case_04_1: 'Enable share link,Copy this URL to share Copy,Sharing access',  // 分享链接开关状态
	Case_05: 'Auto_panel_GA', // 分享面板名称
	Case_05_1: 'New User Trend,Daily Returning Users Rate (%),Traffic Overview', // 分享Widget名称
	Case_07: 'This dashboard requires a password', // 访问面板的密码保护页面说明
	Case_08: 'Auto_panel_GA', // 密保访问的分享面板名称
	Case_08_1: 'New User Trend,Daily Returning Users Rate (%),Traffic Overview', // 密保访问的分享Widget名称
	Case_09: 'off',  // 分享链接开关状态
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
		const Case_02 = 'Case_02: Check Dashboard_Share window. ';
		log(Case_02);
		// 进入 Favorites 标签页
		await page.waitForSelector('.pt-menu > div > div > ul > li:nth-child(2)');
		const Dashboards_Favorites_Sheet = await page.$('.pt-menu > div > div > ul > li:nth-child(2)');
		await Dashboards_Favorites_Sheet.click();
		await page.waitFor(3000);
		// 点击 More icon
		await page.waitForSelector('.panel-tree > div > div.panel-tree__inner > div > div > div:nth-child(2) > a > div.tools > div');
		const Favorites_Panel_More = await page.$('.panel-tree > div > div.panel-tree__inner > div > div > div:nth-child(2) > a > div.tools > div');
		await Favorites_Panel_More.click();
		await page.waitFor(3000);
		// 点击 Share 项
		await page.waitForSelector('.pt-menu__content > div > div > div.pt-panel__tools > a:nth-child(1)');
		const Favorites_Panel_Share = await page.$('.pt-menu__content > div > div > div.pt-panel__tools > a:nth-child(1)');
		await Favorites_Panel_Share.click();
		await page.waitFor(3000);
		// 检查面板分享弹框
		await page.waitForSelector('.panel-share > div > div > div.pt-popupv2__content.is-middle.panel-share__content > header > div > div > div > div > ul');

		// Case_03
		const Case_03 = 'Case_03: Check Dashboard_Public_Link window. Capture [dd_ui_Dashboard_Public_Link.jpg]. Excepted: ' + exp.Case_03;
		log(Case_03);
		// 检查 Share with people 当前分享用户列表
		await page.waitForSelector('.panel-share > div > div > div.pt-popupv2__content.is-middle.panel-share__content > header > div > div > div > div > ul > li:nth-child(2)');
		const Public_Link_Sheet = await page.$('.panel-share > div > div > div.pt-popupv2__content.is-middle.panel-share__content > header > div > div > div > div > ul > li:nth-child(2)');
		await Public_Link_Sheet.click();
		await page.waitFor(1000);
		let Case_03_Act = await page.$eval('.public-link > div.scrollbar__holder.ps-container.ps-theme-light.ps > div.public-link__head > p', el => el.innerText);
		let Case_03_Res = 'Case_03_Res: ' + cps(exp.Case_03, Case_03_Act);
		log(Case_03_Res);
		await page.screenshot({
			path: './pic/dd_ui_Dashboard_Public_Link.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});

		// Case_04
		const Case_04 = 'Case_04: Check Dashboard_Public_Enable_ShareLink. Capture [dd_ui_Dashboard_Public_Enable_ShareLink.jp]. Excepted: ' + exp.Case_04 + ' ' + exp.Case_04_1;
		log(Case_04);
		// 设置Share link开关 = on
		await page.waitForSelector('.public-link__container > div.public-link__content.checkbox-slide > label > span');
		const Enable_ShareLink = await page.$('.public-link__container > div.public-link__content.checkbox-slide > label > span');
		await Enable_ShareLink.click();
		await page.waitFor(1000);
		let Case_04_Act = await page.$eval('.public-link__container > div.public-link__content.checkbox-slide > label > span', el => el.innerText);
		let Case_04_Res = 'Case_04_Res: ' + cps(exp.Case_04, Case_04_Act);
		log(Case_04_Res);
        let Enable_ShareLink_Titles = await page.$$eval('.public-link__label', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
        let Case_04_1_Act = Enable_ShareLink_Titles.join(',');
        let Case_04_1_Res = 'Case_04_1_Res: ' + cps(exp.Case_04_1, Case_04_1_Act);
        log(Case_04_1_Res);
		await page.screenshot({
			path: './pic/dd_ui_Dashboard_Public_Enable_ShareLink.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});
		let ShareLink_URL = await page.$eval('#link-textarea', el => el.value);
		log(ShareLink_URL);

		// Case_05
		const Case_05 = 'Case_05: Check Access_Public_ShareLink_NoPwd. Capture [dd_ui_Access_Public_ShareLink_NoPwd.jp]. Excepted: ' + exp.Case_05 + ' ' + exp.Case_05_1;
		log(Case_05);
		// 在新的页面打开分享链接
		await page.close();
		const page2 = await browser.newPage();
		await page2.goto(ShareLink_URL);
		await page2.waitFor(5000);
		await page2.waitForSelector('.highcharts-plot-background');
		await page2.waitForSelector('.share-dashboard > div.share-dashboard__header > div.share-dashboard__header-title > span');
		await page2.waitForSelector('.share-dashboard > div.share-dashboard__header > div.share-dashboard__header-tools > div.btn > svg');
		await page2.waitForSelector('.share-dashboard > div.share-dashboard__header > div.share-dashboard__header-tools > div.dashboard-time > div');
		let Case_05_Act = await page2.$eval('.share-dashboard > div.share-dashboard__header > div.share-dashboard__header-title > span', el => el.innerText);
		let Case_05_Res = 'Case_05_Res: ' + cps(exp.Case_05, Case_05_Act);
		log(Case_05_Res);
		let Widget_Name_Items = await page2.$$eval('.pt-widget__header > div.widget__header-flex-wrap.pt-tooltip > div > span', els => {
			return els.map(v => {
				return v.innerText;
			})
		});
		let Case_05_1_Act = Widget_Name_Items.join(',');
		let Case_05_1_Res = 'Case_05_1_Res: ' + cps(exp.Case_05_1, Case_05_1_Act);
		log(Case_05_1_Res);
		await page2.screenshot({
			path: './pic/dd_ui_Access_Public_ShareLink_NoPwd.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});
		await page2.waitFor(3000);

		// Case_06
		const Case_06 = 'Case_06: Check Dashboard_Public_ShareLink_SetPwd. Capture [dd_ui_Access_Public_ShareLink_SetPwd.jp]';
		log(Case_06);
		await page2.close();
		const page3 = await browser.newPage();
		await page3.goto('https://dashv2.datadeck.com/');
		await page3.waitFor(3000);
		await page3.waitForSelector('.pt-main__header > div.freetrial-tips.freetrail-tips > div');
		// 进入 Favorites 标签页
		await page3.waitForSelector('.pt-menu > div > div > ul > li:nth-child(2)');
		const Dashboards_Favorites_Sheet_3 = await page3.$('.pt-menu > div > div > ul > li:nth-child(2)');
		await Dashboards_Favorites_Sheet_3.click();
		await page3.waitFor(3000);
		// 点击 More icon
		await page3.waitForSelector('.panel-tree > div > div.panel-tree__inner > div > div > div:nth-child(2) > a > div.tools > div');
		const Favorites_Panel_More_3 = await page3.$('.panel-tree > div > div.panel-tree__inner > div > div > div:nth-child(2) > a > div.tools > div');
		await Favorites_Panel_More_3.click();
		await page3.waitFor(3000);
		// 点击 Share 项
		await page3.waitForSelector('.pt-menu__content > div > div > div.pt-panel__tools > a:nth-child(1)');
		const Favorites_Panel_Share_3 = await page3.$('.pt-menu__content > div > div > div.pt-panel__tools > a:nth-child(1)');
		await Favorites_Panel_Share_3.click();
		await page3.waitFor(3000);
		// 点击 Public link 标签页
		await page3.waitForSelector('.panel-share > div > div > div.pt-popupv2__content.is-middle.panel-share__content > header > div > div > div > div > ul > li:nth-child(2)');
		const Public_Link_Sheet_3 = await page3.$('.panel-share > div > div > div.pt-popupv2__content.is-middle.panel-share__content > header > div > div > div > div > ul > li:nth-child(2)');
		await Public_Link_Sheet_3.click();
		await page3.waitFor(1000);
		// 勾选 Password protect 复选框
		const Password_Protect_Checkbox = await page3.$('.public-link__container > div:nth-child(6) > label:nth-child(2) > span.pt-checkbox__marker');
		await Password_Protect_Checkbox.click();
		await page3.waitFor(1000);
		// 设置密码：123456
		const Password_Protect_Input = await page3.$('.public-link__container > div:nth-child(6) > div > div > input');
		await Password_Protect_Input.type('123456', {delay: 20});
		await page3.waitFor(1000);
		// 点击密码保护 Save 按钮
		const Password_Protect_Save = await page3.$('.public-link__container > div:nth-child(6) > div > button');
		await Password_Protect_Save.click();
		await page3.waitFor(1000);
		await page3.screenshot({
			path: './pic/dd_ui_Access_Public_ShareLink_SetPwd.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});
		await page3.waitFor(3000);
		let ShareLink_URL_3 = await page3.$eval('#link-textarea', el => el.value);
		log(ShareLink_URL_3);

		// Case_07
		const Case_07 = 'Case_07: Check Access_Public_ShareLink_PwdPage. Capture [dd_ui_Access_Public_ShareLink_PwdPage.jp]. Excepted: ' + exp.Case_07;
		log(Case_07);
		await page3.close();
		const page4 = await browser.newPage();
		await page4.goto(ShareLink_URL_3);
		await page4.waitFor(5000);
		await page4.waitForSelector('.share-password__container-title');
		let Case_07_Act = await page4.$eval('.share-password__container-title', el => el.innerText);
		let Case_07_Res = 'Case_07_Res: ' + cps(exp.Case_07, Case_07_Act);
		log(Case_07_Res);
		await page4.screenshot({
			path: './pic/dd_ui_Access_Public_ShareLink_PwdPage.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});

		// Case_08
		const Case_08 = 'Case_08: Check Access_Public_ShareLink_HavePwd. Capture [dd_ui_Access_Public_ShareLink_HavePwd.jp]. Excepted: ' + exp.Case_08 + ' ' + exp.Case_08_1;
		log(Case_08);
		// 输入密码
		await page4.waitForSelector('.share-password__container-input > div > input');
		const Dashboard_Password_Input = await page4.$('.share-password__container-input > div > input');
		await Dashboard_Password_Input.type('123456', {delay: 20});
		// 点击 View dashboard 按钮
		await page4.waitForSelector('.share-password__container-btn > button');
		const Dashboard_View_Button = await page4.$('.share-password__container-btn > button');
		await Dashboard_View_Button.click();
		await page4.waitFor(5000);
		await page4.waitForSelector('.highcharts-plot-background');
		await page4.waitForSelector('.share-dashboard > div.share-dashboard__header > div.share-dashboard__header-title > span');
		let Case_08_Act = await page4.$eval('.share-dashboard > div.share-dashboard__header > div.share-dashboard__header-title > span', el => el.innerText);
		let Case_08_Res = 'Case_08_Res: ' + cps(exp.Case_08, Case_08_Act);
		log(Case_08_Res);
		let Widget_Name_Items_4 = await page4.$$eval('.pt-widget__header > div.widget__header-flex-wrap.pt-tooltip > div > span', els => {
			return els.map(v => {
				return v.innerText;
			})
		});
		let Case_08_1_Act = Widget_Name_Items_4.join(',');
		let Case_08_1_Res = 'Case_08_1_Res: ' + cps(exp.Case_08_1, Case_08_1_Act);
		log(Case_08_1_Res);
		await page4.screenshot({
			path: './pic/dd_ui_Access_Public_ShareLink_HavePwd.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});
		await page4.waitFor(3000);

		// Case_09
		const Case_09 = 'Case_09: Check Dashboard_Public_ShareLink_CancelToReset. Excepted: ' + exp.Case_09;
		log(Case_09);
		await page4.close();
		const page5 = await browser.newPage();
		await page5.goto('https://dashv2.datadeck.com/');
		await page5.waitFor(3000);
		await page5.waitForSelector('.pt-main__header > div.freetrial-tips.freetrail-tips > div');
		// 进入 Favorites 标签页
		await page5.waitForSelector('.pt-menu > div > div > ul > li:nth-child(2)');
		const Dashboards_Favorites_Sheet_5 = await page5.$('.pt-menu > div > div > ul > li:nth-child(2)');
		await Dashboards_Favorites_Sheet_5.click();
		await page5.waitFor(3000);
		// 点击 More icon
		await page5.waitForSelector('.panel-tree > div > div.panel-tree__inner > div > div > div:nth-child(2) > a > div.tools > div');
		const Favorites_Panel_More_5 = await page5.$('.panel-tree > div > div.panel-tree__inner > div > div > div:nth-child(2) > a > div.tools > div');
		await Favorites_Panel_More_5.click();
		await page5.waitFor(3000);
		// 点击 Share 项
		await page5.waitForSelector('.pt-menu__content > div > div > div.pt-panel__tools > a:nth-child(1)');
		const Favorites_Panel_Share_5 = await page5.$('.pt-menu__content > div > div > div.pt-panel__tools > a:nth-child(1)');
		await Favorites_Panel_Share_5.click();
		await page5.waitFor(3000);
		// 点击 Public link 标签页
		await page5.waitForSelector('.panel-share > div > div > div.pt-popupv2__content.is-middle.panel-share__content > header > div > div > div > div > ul > li:nth-child(2)');
		const Public_Link_Sheet_5 = await page5.$('.panel-share > div > div > div.pt-popupv2__content.is-middle.panel-share__content > header > div > div > div > div > ul > li:nth-child(2)');
		await Public_Link_Sheet_5.click();
		await page5.waitFor(1000);
		// 取消勾选 Password protect 复选框
		const Password_Protect_Checkbox_5 = await page5.$('.public-link__container > div:nth-child(6) > label:nth-child(2) > span.pt-checkbox__marker');
		await Password_Protect_Checkbox_5.click();
		await page5.waitFor(1000);
		// 设置Share link开关 = off
		await page5.waitForSelector('.public-link__container > div.public-link__content.checkbox-slide > label > span');
		const Enable_ShareLink_Off = await page5.$('.public-link__container > div.public-link__content.checkbox-slide > label > span');
		await Enable_ShareLink_Off.click();
		await page5.waitFor(1000);
		let Case_09_Act = await page5.$eval('.public-link__container > div.public-link__content.checkbox-slide > label > span', el => el.innerText);
		let Case_09_Res = 'Case_09_Res: ' + cps(exp.Case_09, Case_09_Act);
		log(Case_09_Res);

		await page5.waitFor(5000);

		// log
		const log_server_1 = 'log_server_1: 【AT_DD_Online_UI_DashboardPublic】 runs Finished.';
		log(log_server_1);

		let writerStream = fs.createWriteStream('./log/dd_ui_log.txt');
		writerStream.write(log_server_0 + '\r\n'
			+ Case_01 + '\r\n'
			+ Case_02 + '\r\n'
			+ Case_03 + '\r\n'
			+ Case_03_Res + '\r\n'
			+ Case_04 + '\r\n'
			+ Case_04_Res + '\r\n'
			+ Case_04_1_Res + '\r\n'
			+ Case_05 + '\r\n'
			+ Case_05_Res + '\r\n'
			+ Case_05_1_Res + '\r\n'
			+ Case_06 + '\r\n'
			+ Case_07 + '\r\n'
			+ Case_07_Res + '\r\n'
			+ Case_08 + '\r\n'
			+ Case_08_Res + '\r\n'
			+ Case_08_1_Res + '\r\n'
			+ Case_09 + '\r\n'
			+ Case_09_Res + '\r\n'
			+ log_server_1 + '\r\n', 'UTF8');
		writerStream.end();

	} catch (e) {
		if (e instanceof TimeoutError) {
			console.error(e);
			const log_block = 'Log_Block: Service unexpected termination! 【AT_DD_Online_UI_DashboardPublic】 runs Error!';
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




