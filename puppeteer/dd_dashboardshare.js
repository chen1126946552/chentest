
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
	Case_02: 'Share with people\nPublic link',  // Dashboard_Share 弹框，Sheet标题内容
	Case_03: 'dd_auto_jp213@mailinator.com',  // Currently Shared with，仅包括Owner
	Case_04: 'Can View Only,Can View & Analyze,Can Edit,Can Edit & Share',  // 面板分享权限
	Case_05: 'dd_auto_jp213@mailinator.com,dd_auto_jp212@mailinator.com', // 面板分享用户列表
	Case_06: 'Can View Only,Can View & Analyze,Can Edit,Can Edit & Share,Remove', // 分享下拉列表项
	Case_06_1: 'dd_auto_jp213@mailinator.com', // 移除分享用户后，用户列表
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
		const Case_02 = 'Case_02: Check Dashboard_Share window. Capture [dd_ui_Dashboard_Share.jpg]. Excepted: ' + exp.Case_02;
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
		let Case_02_Act = await page.$eval('.panel-share > div > div > div.pt-popupv2__content.is-middle.panel-share__content > header > div > div > div > div > ul', el => el.innerText);
		let Case_02_Res = 'Case_02_Res: ' + cps(exp.Case_02, Case_02_Act);
		log(Case_02_Res);
		await page.screenshot({
			path: './pic/dd_ui_Dashboard_Share.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});

		// Case_03
		const Case_03 = 'Case_03: Check Dashboard_Share_Userlist_NoShare. Excepted: ' + exp.Case_03;
		log(Case_03);
		// 检查 Share with people 当前分享用户列表
		await page.waitForSelector('.pt-cooperation > div.pt-cooperation__share > div > div.pt-cooperation__title');
		let Share_With_Userlist = await page.$$eval('.pt-cooperation__list-info > div.name > span', els => {
			return els.map(v => {
				return v.innerText;
			});
		});
		let Case_03_Act = Share_With_Userlist.join(',');
		let Case_03_Res = 'Case_03_Res: ' + cps(exp.Case_03, Case_03_Act);
		log(Case_03_Res);

		// Case_04
		const Case_04 = 'Case_04: Check Dashboard_Share_InviteUser. Excepted: ' + exp.Case_04;
		log(Case_04);
		// 焦点键入Share with输入框，检查表单项
		await page.waitForSelector('.pt-cooperation > div.pt-cooperation__share > div > div.cooperation-input');
		const Share_With_Input = await page.$('.cooperation-input__list-wrap > div');
		// 点击输入框
		await Share_With_Input.click();
		// 输入邀请用户
		await Share_With_Input.type('dd_auto_jp212@mailinator.com', {delay: 20});
		// 点击输入框，确认用户已选中
		await Share_With_Input.click();
		// 检查权限
        await page.waitForSelector('.pt-cooperation > div.pt-cooperation__share.all > div > div.pt-cooperation__share-notes > div.pt-select.select_en_US > div');
        const Share_Permission = await page.$('.pt-cooperation > div.pt-cooperation__share.all > div > div.pt-cooperation__share-notes > div.pt-select.select_en_US > div');
        await Share_Permission.click();
        await page.waitFor(1000);
        await page.waitForSelector('.pt-select__dropdown > div > div > ul');
        let Share_Permission_Items = await page.$$eval('.pt-select__dropdown-item', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
        let Case_04_Act = Share_Permission_Items.join(',');
		let Case_04_Res = 'Case_04_Res: ' + cps(exp.Case_04, Case_04_Act);
		log(Case_04_Res);
		await page.waitFor(1000);

		// Case_05
		const Case_05 = 'Case_05: Check Dashboard_Share_jp212. Capture [dd_ui_Dashboard_Share_CurrentList.jpg] Excepted: ' + exp.Case_05;
		log(Case_05);
		// 点击 Share 按钮
		await page.waitForSelector('.panel-share > div > div > div.pt-popupv2__content.is-middle.panel-share__content > footer > button');
		const Share_With_Button = await page.$('.panel-share > div > div > div.pt-popupv2__content.is-middle.panel-share__content > footer > button');
		await Share_With_Button.click();
		await page.waitFor(5000);
		// 面板分享弹框，分享用户列表
		await page.waitForSelector('.pt-cooperation > div.pt-cooperation__list > div > div > ul > li:nth-child(2) > div.pt-cooperation__list-info > div.name');
		let Share_With_Userlist_2 = await page.$$eval('.pt-cooperation__list-info > div.name > span', els => {
			return els.map(v => {
				return v.innerText;
			});
		});
		let Case_05_Act = Share_With_Userlist_2.join(',');
		let Case_05_Res = 'Case_05_Res: ' + cps(exp.Case_05, Case_05_Act);
		log(Case_05_Res);
		await page.screenshot({
			path: './pic/dd_ui_Dashboard_Share_CurrentList.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});

		// Case_06
		const Case_06 = 'Case_06: Check Dashboard_Remove_Share_jp212. Excepted: ' + exp.Case_06;
		log(Case_06);
		// 点击 Share 按钮，检查列表项
		await page.waitForSelector('.pt-cooperation > div.pt-cooperation__list > div > div > ul > li:nth-child(2) > div.change-role > div > div');
		const Share_DropDownList = await page.$('.pt-cooperation > div.pt-cooperation__list > div > div > ul > li:nth-child(2) > div.change-role > div > div');
		await Share_DropDownList.click();
		await page.waitFor(1000);
		let Share_DropDownList_Items = await page.$$eval('.pt-select__dropdown-item', els => {
			return els.map(v => {
				return v.innerText;
			})
		});
		let Case_06_Act = Share_DropDownList_Items.join(',');
		let Case_06_Res = 'Case_06_Res: ' + cps(exp.Case_06, Case_06_Act);
		log(Case_06_Res);
		// 点击 Remove
		const Share_DropDownList_Remove = await page.$('.change-role > div > div.pt-select__dropdown > div > div > ul > li:nth-child(5)');
		await Share_DropDownList_Remove.click();
		await page.waitFor(1000);
		// 面板分享弹框，分享用户列表
		await page.waitForSelector('.pt-cooperation > div.pt-cooperation__list > div > div > ul > li > div.pt-cooperation__list-info');
		let Share_With_Userlist_3 = await page.$$eval('.pt-cooperation__list-info > div.name > span', els => {
			return els.map(v => {
				return v.innerText;
			});
		});
		let Case_06_1_Act = Share_With_Userlist_3.join(',');
		let Case_06_1_Res = 'Case_06_1_Res: ' + cps(exp.Case_06_1, Case_06_1_Act);
		log(Case_06_1_Res);
		// 关闭 面板分享 弹框
		const Panel_Share_Close = await page.$('.panel-share > div > div > div.pt-popupv2__content.is-middle.panel-share__content > footer > button');
		await Panel_Share_Close.click();
		await page.waitFor(1000);

		await page.waitFor(3000);

		// log
		const log_server_1 = 'log_server_1: 【AT_DD_Online_UI_DashboardShare】 runs Finished.';
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
			+ Case_06_Res + '\r\n'
			+ Case_06_1_Res + '\r\n'
			+ log_server_1 + '\r\n', 'UTF8');
		writerStream.end();

	} catch (e) {
		if (e instanceof TimeoutError) {
			console.error(e);
			const log_block = 'Log_Block: Service unexpected termination! 【AT_DD_Online_UI_DashboardShare】 runs Error!';
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




