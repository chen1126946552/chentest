
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
	Case_02: 'Admins (1)',   // My team 管理员数量
	Case_02_1: 'dd_auto_jp212@mailinator.com',  // My team 管理员，dd_auto_jp212@mailinator.com
	Case_03: 'Invite members',  // 邀请成员弹框，标题内容
	Case_04: 'dd_auto_jp211@mailinator.com',  // 邀请新成员
	Case_05: 'Are you sure you want to remove this member?',  // 移除成员确认信息
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
		const Case_01 = 'Case_01: Login Datadeck dd_auto_jp212@mailinator.com.';
		log(Case_01);
		await page.goto('https://dashv2.datadeck.com/login');
		await page.waitForSelector('.pt-ui-button__text');
		const documentSize = await page.evaluate(() => {
			return {
				width: document.documentElement.clientWidth,
				height: document.body.clientHeight,
			}
		});
		await page.type('[name=email]', 'dd_auto_jp212@mailinator.com', {delay: 20});
		await page.type('[name=userPassword]', '123456', {delay: 20});
		const authLogin = await page.$('.pt-ui-button');
		await authLogin.click();
		await page.waitFor(1000);
		await page.waitForSelector('.linkList > a.item.my-team > div');

		// Case_02
		const Case_02 = 'Case_02: Check MyTeam page. Capture [dd_ui_MyTeam.jpg]. Excepted: ' + exp.Case_02 + ' ' + exp.Case_02_1;
		log(Case_02);
		await page.waitForSelector('.linkList > a.item.my-team > div');
		const MyTeam_Item = await page.$('.linkList > a.item.my-team > div');
		await MyTeam_Item.click();
		await page.waitFor(1000);
		await page.waitForSelector('.pt-myteam__content > div:nth-child(1) > div.member-grid__header');
		let Case_02_Act = await page.$eval('.pt-myteam__content > div:nth-child(1) > div.member-grid__header', el => el.innerText);
		let Case_02_Res = 'Case_02_Res: ' + cps(exp.Case_02, Case_02_Act);
		log(Case_02_Res);
		await page.waitForSelector('.member-grid__content > div > div > div.member-card__email');
		let Case_02_1_Act = await page.$eval('.member-grid__content > div > div > div.member-card__email', el => el.innerText);
		let Case_02_1_Res = 'Case_02_1_Res: ' + cps(exp.Case_02_1, Case_02_1_Act);
		log(Case_02_1_Res);
		await page.waitFor(1000);
		await page.screenshot({
			path: './pic/dd_ui_MyTeam.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_03
		const Case_03 = 'Case_03: Check Invite_Members window. Capture [dd_ui_Invite_Members.jpg]. Excepted: ' + exp.Case_03;
		log(Case_03);
		await page.waitForSelector('.pt-main__content > div.pt-myteam > div.pt-myteam__header > button');
		const Invite_Space_Members = await page.$('.pt-main__content > div.pt-myteam > div.pt-myteam__header > button');
		await Invite_Space_Members.click();
		await page.waitFor(1000);
		await page.waitForSelector('.members-invite > div > div > div.pt-popupv2__content.is-middle > header > h3 > span');
		let Case_03_Act = await page.$eval('.members-invite > div > div > div.pt-popupv2__content.is-middle > header > h3 > span', el => el.innerText);
		let Case_03_Res = 'Case_03_Res: ' + cps(exp.Case_03, Case_03_Act);
		log(Case_03_Res);
		await page.screenshot({
			path: './pic/dd_ui_Invite_Members.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_04
		const Case_04 = 'Case_04: Check MyTeam_Space_Member. Capture [dd_ui_MyTeam_Space_Member.jpg]. Excepted: ' + exp.Case_04;
		log(Case_04);
		// 输入邀请邮件
		await page.waitForSelector('.pt-popupv2__main > div > div.members-invite__content > div.textarea-box');
		const Invite_Email = await page.$('.pt-popupv2__main > div > div.members-invite__content > div.textarea-box > div > div.textarea');
		await Invite_Email.focus();
		await Invite_Email.type('dd_auto_jp211@mailinator.com', {delay: 20});
		await page.waitFor(1000);
		// 点击Invite按钮
		await page.waitForSelector('.pt-myteam > div.members-invite > div > div > div.pt-popupv2__content.is-middle > footer > button');
		const Invite_Email_Button = await page.$('.pt-myteam > div.members-invite > div > div > div.pt-popupv2__content.is-middle > footer > button');
		await Invite_Email_Button.click();
		await page.waitFor(2000);
		// 检查新邀请的成员是否存在
		await page.waitForSelector('.pt-myteam__content > div:nth-child(3) > div.member-grid__content > div > div > div.member-card__email');
		let Case_04_Act = await page.$eval('.pt-myteam__content > div:nth-child(3) > div.member-grid__content > div > div > div.member-card__email', el => el.innerText);
		let Case_04_Res = 'Case_04_Res: ' + cps(exp.Case_04, Case_04_Act);
		log(Case_04_Res);
		await page.screenshot({
			path: './pic/dd_ui_MyTeam_Space_Member.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_05
		const Case_05 = 'Case_05: Check Remove_Member_Confirm. Excepted: ' + exp.Case_05;
		log(Case_05);
		// 打开角色下拉框
		await page.waitForSelector('.pt-myteam__content > div:nth-child(3) > div.member-grid__content > div > div > div.member-card__role > div > div');
		const Member_Role = await page.$('.pt-myteam__content > div:nth-child(3) > div.member-grid__content > div > div > div.member-card__role > div > div');
		await Member_Role.click();
		await page.waitFor(1000);
		// 点击Remove member
		await page.waitForSelector('.pt-myteam__content > div:nth-child(3) > div.member-grid__content > div > div > div.member-card__role > div > div.pt-select__dropdown > div > div > ul > li:nth-child(3)');
		const Remove_Member_Item = await page.$('.pt-myteam__content > div:nth-child(3) > div.member-grid__content > div > div > div.member-card__role > div > div.pt-select__dropdown > div > div > ul > li:nth-child(3)');
		await page.waitFor(1000);
		await Remove_Member_Item.click();
		await page.waitFor(1000);
		await page.waitForSelector('.member-card__role > div > div.pt-select__dropdown > div > div > div.pt-select__dropdown-tips > div > div.delete-member__tips-container');
		let Case_05_Act = await page.$eval('.member-card__role > div > div.pt-select__dropdown > div > div > div.pt-select__dropdown-tips > div > div.delete-member__tips-container', el => el.innerText);
		let Case_05_Res = 'Case_05_Res: ' + cps(exp.Case_05, Case_05_Act);
		log(Case_05_Res);
		// 确认移除Member
		const Remove_Member_Button = await page.$('.pt-select__dropdown > div > div > div.pt-select__dropdown-tips > div > div.delete-member__tips-footer > button.pt-ui-button.pt-ui-button--danger.pt-ui-button--type-default.pt-ui-button--size-default.is-little-radius');
		await Remove_Member_Button.click();
		await page.waitFor(2000);

		// log
		const log_server_1 = 'log_server_1: 【AT_DD_Online_UI_MyTeam】 runs Finished.';
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
			const log_block = 'Log_Block: Service unexpected termination! 【AT_DD_Online_UI_MyTeam】 runs Error!';
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




