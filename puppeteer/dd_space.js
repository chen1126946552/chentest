
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
	Case_02: 'First, you need to choose a name for your space.This space will be used for your team or company to visualize, analyze and share data.',  // 创建空间说明
	Case_03: 'Datadeck is built for teams. Easily share KPI’s and key metrics with a click of a button. Add your team members here and we will help them get set up!',  // 邀请team说明
	Case_04: 'dd_auto_jp215', // 新空间名称
	Case_05: 'Adwords レポート テンプレート,Facebook Ads と Google Ads,Google Analytics オーディエンス レポート,Google Analytics ダイジェスト,クイック スタート,最初のダッシュボード', // 默认的面板名称
	Case_06: 'If you delete your space you will no longer be able to access any of the data in your space. Do you still want to delete your space?', // 删除空间描述
	Case_07: 'Delete space', // 删除空间弹框标题
	Case_08: 'Password,Please confirm that deleting space will lead to following things', // 删除空间标题
	Case_08_1: 'All dashboards and data sources in this space will be deleted.,All share links will be inaccessible.,This space will no longer exist and this cannot be undone.', // 删除空间可选项
	Case_09: 'First, you need to choose a name for your space.This space will be used for your team or company to visualize, analyze and share data.',  // 创建空间说明
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
		const Case_01 = 'Case_01: Login Datadeck with dd_auto_jp215@mailinator.com.';
		log(Case_01);
		await page.goto('https://dashv2.datadeck.com/login');
		await page.waitForSelector('.pt-ui-button__text');
		const documentSize = await page.evaluate(() => {
			return {
				width: document.documentElement.clientWidth,
				height: document.body.clientHeight,
			}
		});
		await page.type('[name=email]', 'dd_auto_jp215@mailinator.com', {delay: 20});
		await page.type('[name=userPassword]', '123456', {delay: 20});
		const authLogin = await page.$('.pt-ui-button');
		await authLogin.click();
		await page.waitFor(3000);
		await page.waitForSelector('.pt-space__left > div.pt-space__content > div.pt-space__desc');
		await page.screenshot({
			path: './pic/dd_ui_Create_Space.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});

		// Case_02
		const Case_02 = 'Case_02: Check Create_Space page. Capture [dd_ui_Create_Space.jpg]. Excepted: ' + exp.Case_02;
		log(Case_02);
		await page.waitForSelector('.pt-space__left > div.pt-space__content > div.pt-space__desc > p');
		let Case_02_Act = await page.$eval('.pt-space__left > div.pt-space__content > div.pt-space__desc > p', el => el.innerText);
		let Case_02_Res = 'Case_02_Res: ' + cps(exp.Case_02, Case_02_Act);
		log(Case_02_Res);
		// 输入空间名称
		await page.waitForSelector('.pt-space__left > div.pt-space__content > div.pt-space__inputarea > div > input');
		const Space_Name_Input = await page.$('.pt-space__left > div.pt-space__content > div.pt-space__inputarea > div > input');
		await Space_Name_Input.type('dd_auto_jp215', {delay: 20});
		// 点击 Next
		await page.waitForSelector('.pt-space__left > div.pt-space__footer > button');
		const Create_Space_Next = await page.$('.pt-space__left > div.pt-space__footer > button');
		await Create_Space_Next.click();
		await page.waitFor(5000);

		// Case_03
		const Case_03 = 'Case_03: Check Invite_Team page. Capture [dd_ui_Invite_Team.jpg]. Excepted: ' + exp.Case_03;
		log(Case_03);
		await page.waitForSelector('.pt-space__invitation__left > div.pt-space__invitation__content > div.pt-space__invitation__desc');
		let Case_03_Act = await page.$eval('.pt-space__invitation__left > div.pt-space__invitation__content > div.pt-space__invitation__desc > p', el => el.innerText);
		let Case_03_Res = 'Case_03_Res: ' + cps(exp.Case_03, Case_03_Act);
		log(Case_03_Res);
		await page.screenshot({
			path: './pic/dd_ui_Invite_Team.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});

		// Case_04
		const Case_04 = 'Case_04: Check Enter_Datadeck page. Capture [dd_ui_Enter_Datadeck.jpg]. Excepted: ' + exp.Case_04;
		log(Case_04);
		await page.waitForSelector('.pt-space__invitation__left > div.pt-space__invitation__footer > div.pt-space__skiplink > a');
		const Link_Start_Datadeck = await page.$('.pt-space__invitation__left > div.pt-space__invitation__footer > div.pt-space__skiplink > a');
		await Link_Start_Datadeck.click();
		await page.waitFor(3000);
		await page.waitForSelector('.pt-account > div > h1 > span');
		let Case_04_Act = await page.$eval('.pt-account > div > h1 > span', el => el.innerText);
		let Case_04_Res = 'Case_04_Res: ' + cps(exp.Case_04, Case_04_Act);
		log(Case_04_Res);
		await page.screenshot({
			path: './pic/dd_ui_Enter_Datadeck.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});

		// Case_05
		const Case_05 = 'Case_05: Check NewSpace_Default_PanelName. Excepted: ' + exp.Case_05;
		log(Case_05);
		await page.waitForSelector('.pt-menu__content > div > div > div.panel-header');
		let Default_PanelName = await page.$$eval('.node-name > div.name > span', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
		let Default_PanelName_Sort = Default_PanelName.sort();
        let Case_05_Act = Default_PanelName_Sort.join(',');
        let Case_05_Res = 'Case_05_Res: ' + cps(exp.Case_05, Case_05_Act);
        log(Case_05_Res);

        // Case_06
		const Case_06 = 'Case_06: Check Delete_Space_Link. Capture [dd_ui_Delete_Space_Link.jp]. Excepted: ' + exp.Case_06;
		log(Case_06);
		// 点击 空间名称
		await page.waitForSelector('.pt-account > div > h1');
		const Space_Name = await page.$('.pt-account > div > h1');
		await Space_Name.click();
		await page.waitFor(1000);
		// 点击 Space Details
		await page.waitForSelector('.pt-account > div.account-menu > div:nth-child(5)');
		const Space_Details = await page.$('.pt-account > div.account-menu > div:nth-child(5)');
		await Space_Details.click();
		await page.waitFor(1000);
		// 检查删除空间描述
		await page.waitForSelector('.space-detail__container-content > div > div.space-general__wrap > div:nth-child(7) > div.space-general__item-container > div');
		const Case_06_Act = await page.$eval('.space-detail__container-content > div > div.space-general__wrap > div:nth-child(7) > div.space-general__item-container > div', el => el.innerText);
        let Case_06_Res = 'Case_06_Res: ' + cps(exp.Case_06, Case_06_Act);
        log(Case_06_Res);

        // Case_07
		const Case_07 = 'Case_07: Check Delete_Space_Confirm window. Capture [dd_ui_Delete_Space_Confirm.jp]. Excepted: ' + exp.Case_07;
		log(Case_07);
		await page.waitForSelector('.space-detail__container-content > div > div.space-general__wrap > div:nth-child(7) > div.space-general__item-container > div > a');
		const Link_Delete_Space = await page.$('.space-detail__container-content > div > div.space-general__wrap > div:nth-child(7) > div.space-general__item-container > div > a');
		await Link_Delete_Space.click();
		await page.waitFor(1000);
		await page.waitForSelector('.space-delete > div > div > div.pt-popupv2__content.hideFooter.is-middle.space-delete__popup > div.pt-popupv2__main > div > h3');
		const Case_07_Act = await page.$eval('.space-delete > div > div > div.pt-popupv2__content.hideFooter.is-middle.space-delete__popup > div.pt-popupv2__main > div > h3', el => el.innerText);
		let Case_07_Res = 'Case_07_Res: ' + cps(exp.Case_07, Case_07_Act);
        log(Case_07_Res);
        await page.screenshot({
			path: './pic/dd_ui_Delete_Space_Confirm.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});

        // Case_08
		const Case_08 = 'Case_08: Check Delete_Space_Confirm_SelectItems. Excepted: ' + exp.Case_08 + ' ' + exp.Case_08_1;
		log(Case_08);
		let Delete_Space_Title = await page.$$eval('.space-delete__content > dl > dt', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
        let Case_08_Act = Delete_Space_Title.join(',');
        // log(Case_08_Act);
        let Case_08_Res = 'Case_08_Res: ' + cps(exp.Case_08, Case_08_Act);
        log(Case_08_Res);
		let Delete_Space_Items = await page.$$eval('.pt-checkbox__label.pt-tooltip', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
        let Case_08_1_Act = Delete_Space_Items.join(',');
        // log(Case_08_1_Act);
        let Case_08_1_Res = 'Case_08_1_Res: ' + cps(exp.Case_08_1, Case_08_1_Act);
        log(Case_08_1_Res);

        // Case_09
		const Case_09 = 'Case_09: Check Delete_Space_Jump_Create Page. Capture [dd_ui_Delete_Space_Jump_Create.jp].';
		log(Case_09);
		await page.waitForSelector('.pt-popupv2__main > div > div.space-delete__content > dl:nth-child(1) > dd > div > input');
		const Password_Input = await page.$('.pt-popupv2__main > div > div.space-delete__content > dl:nth-child(1) > dd > div > input');
		await Password_Input.type('123456', {delay: 20});
		await page.waitFor(1000);
		const Items_Checkbox_1 = await page.$('.space-delete__content > dl:nth-child(2) > dd:nth-child(2) > label');
		await Items_Checkbox_1.click();
		await page.waitFor(1000);
		const Items_Checkbox_2 = await page.$('.space-delete__content > dl:nth-child(2) > dd:nth-child(3) > label');
		await Items_Checkbox_2.click();
		await page.waitFor(1000);
		const Items_Checkbox_3 = await page.$('.space-delete__content > dl:nth-child(2) > dd:nth-child(4) > label');
		await Items_Checkbox_3.click();
		await page.waitFor(1000);
		// 点击 Delete space
		await page.waitForSelector('.pt-popupv2__main > div > div.space-delete__footer > button');
		const Delete_Space_Button = await page.$('.pt-popupv2__main > div > div.space-delete__footer > button');
		await Delete_Space_Button.click();
		await page.waitFor(5000);
		// 跳转至创建空间页面
		await page.waitForSelector('.pt-space__left > div.pt-space__content > div.pt-space__desc');
		await page.screenshot({
			path: './pic/dd_ui_Delete_Space_Jump_Create.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});
		await page.waitForSelector('.pt-space__left > div.pt-space__content > div.pt-space__desc > p');
		let Case_09_Act = await page.$eval('.pt-space__left > div.pt-space__content > div.pt-space__desc > p', el => el.innerText);
		let Case_09_Res = 'Case_09_Res: ' + cps(exp.Case_09, Case_09_Act);
		log(Case_09_Res);

		await page.waitFor(3000);

		// log
		const log_server_1 = 'log_server_1: 【AT_DD_Online_UI_Space】 runs Finished.';
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
			const log_block = 'Log_Block: Service unexpected termination! 【AT_DD_Online_UI_Space】 runs Error!';
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




