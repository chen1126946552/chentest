
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
	Case_02: 'Share your data" autotest_table.csv "',  // 分享Upload连接弹框
	Case_03: 'dd_auto_jp213@mailinator.com,dd_auto_jp214@mailinator.com',  // 分享用户列表
	Case_04: 'Share your data" peterangel536@gmail.com "',  // 分享GA连接弹框
	Case_04_1: 'dd_auto_jp213@mailinator.com,dd_auto_jp214@mailinator.com',  // 分享用户列表
	Case_06: 'Title,autotest_table.csv,peterangel536@gmail.com', // jp214，Manage data 列表，分享连接信息
	Case_08: 'dd_auto_jp213@mailinator.com', // 仅存在Owner
	Case_09: 'dd_auto_jp213@mailinator.com', // 仅存在Owner
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
		const Case_01 = 'Case_01: Login Datadeck with dd_auto_jp213@mailinator.com.';
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
		const Case_02 = 'Case_02: Check ManageData_Share_Upload window. Capture [dd_ui_ManageData_Share_Upload.jpg]. Excepted: ' + exp.Case_02;
		log(Case_02);
		// 点击 Manage data
		await page.waitForSelector('.linkList > a.item.data-manage > div');
		const ManageData_Item = await page.$('.linkList > a.item.data-manage > div');
		await ManageData_Item.click();
		await page.waitFor(1000);
		await page.waitForSelector('.connection-list > div.connection-list__header > div');
		// 过滤Excel/CSV
		await page.waitForSelector('.connection__header > div.connection-searchwrap > div.connection-searchwrap__input-name > div > input');
		const ManageData_Search_Input = await page.$('.connection__header > div.connection-searchwrap > div.connection-searchwrap__input-name > div > input');
		await ManageData_Search_Input.click();
		await page.waitFor(1000);
		await ManageData_Search_Input.type('Excel/CSV', {delay: 20});
		// 点击 Share 按钮
		await page.waitForSelector('.connection-list__col-share > div > a');
		const Share_Button_Upload = await page.$('.connection-list__col-share > div > a');
		await Share_Button_Upload.click();
		await page.waitFor(1000);
		await page.screenshot({
			path: './pic/dd_ui_ManageData_Share_Upload.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});
		// 检查分享标题
		await page.waitForSelector('.pt-popupv2__content.is-middle.datasource-share__content > header > div');
		let Case_02_Act = await page.$eval('.pt-popupv2__content.is-middle.datasource-share__content > header > div', el => el.innerText);
		let Case_02_Res = 'Case_02_Res: ' + cps(exp.Case_02, Case_02_Act);
		log(Case_02_Res);

		// Case_03
		const Case_03 = 'Case_03: Check ManageData_Share_Upload_jp214. Excepted: ' + exp.Case_03;
		log(Case_03);
		// 分享 Upload 给 jp214
		await page.waitForSelector('.pt-cooperation__share > div > div.cooperation-input > div > div > div > div.inner > input');
		const Upload_Share_Input_jp214 = await page.$('.pt-cooperation__share > div > div.cooperation-input > div > div > div > div.inner > input');
		await Upload_Share_Input_jp214.click();
		await page.waitFor(1000);
		await Upload_Share_Input_jp214.type('dd_auto_jp214@mailinator.com', {delay: 20});
		await Upload_Share_Input_jp214.click();
		await page.waitFor(1000);
		await page.waitForSelector('.pt-popupv2__content.is-middle.datasource-share__content > footer > button');
		const Upload_Share_Button = await page.$('.pt-popupv2__content.is-middle.datasource-share__content > footer > button');
		await Upload_Share_Button.click();
		await page.waitFor(1000);
        let Upload_Share_UserList = await page.$$eval('.pt-cooperation__list-info > div.name > span', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
        let Case_03_Act = Upload_Share_UserList.join(',');
        let Case_03_Res = 'Case_03_Res: ' + cps(exp.Case_03, Case_03_Act);
        log(Case_03_Res);
        await page.waitForSelector('.pt-popupv2__content.is-middle.datasource-share__content > footer > button');
        const Upload_Share_Close = await page.$('.pt-popupv2__content.is-middle.datasource-share__content > footer > button');
        await Upload_Share_Close.click();
        await page.waitFor(3000);

		// Case_04
		const Case_04 = 'Case_04: Check ManageData_Share_GA_jp214. Excepted: ' + exp.Case_04 + ' ' + exp.Case_04_1;
		log(Case_04);
		// 清除 Upload 检索条件
		await page.waitForSelector('.connection__header > div.connection-searchwrap > div.connection-searchwrap__input-name > div > input');
		const ManageData_Search_Input_ClearUpload = await page.waitForSelector('.pt-input__inner__clearButton');
		await ManageData_Search_Input_ClearUpload.click();
		// 过滤 Google Analytics
		const ManageData_Search_Input_GA = await page.$('.connection__header > div.connection-searchwrap > div.connection-searchwrap__input-name > div > input');
		await ManageData_Search_Input_GA.click();
		await page.waitFor(1000);
		await ManageData_Search_Input_GA.type('Google Analytics', {delay: 20});
		// 点击 Share 按钮
		await page.waitForSelector('.connection-list__col-share > div > a');
		const Share_Button_GA = await page.$('.connection-list__col-share > div > a');
		await Share_Button_GA.click();
		await page.waitFor(1000);
		// 分享 GA 弹框，检查标题
		await page.waitForSelector('.pt-popupv2__content.is-middle.datasource-share__content > header > div');
		let Case_04_Act = await page.$eval('.pt-popupv2__content.is-middle.datasource-share__content > header > div', el => el.innerText);
		let Case_04_Res = 'Case_04_Res: ' + cps(exp.Case_04, Case_04_Act);
		log(Case_04_Res);
		// 分享 GA 给 jp214
		await page.waitForSelector('.pt-cooperation__share > div > div.cooperation-input > div > div > div > div.inner > input');
		const GA_Share_Input_jp214 = await page.$('.pt-cooperation__share > div > div.cooperation-input > div > div > div > div.inner > input');
		await GA_Share_Input_jp214.click();
		await page.waitFor(1000);
		await GA_Share_Input_jp214.type('dd_auto_jp214@mailinator.com', {delay: 20});
		await GA_Share_Input_jp214.click();
		await page.waitFor(1000);
		await page.waitForSelector('.pt-popupv2__content.is-middle.datasource-share__content > footer > button');
		const GA_Share_Button = await page.$('.pt-popupv2__content.is-middle.datasource-share__content > footer > button');
		await GA_Share_Button.click();
		await page.waitFor(1000);
        let GA_Share_UserList = await page.$$eval('.pt-cooperation__list-info > div.name > span', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
        let Case_04_1_Act = GA_Share_UserList.join(',');
        let Case_04_1_Res = 'Case_04_1_Res: ' + cps(exp.Case_04_1, Case_04_1_Act);
        log(Case_04_1_Res);
        await page.waitForSelector('.pt-popupv2__content.is-middle.datasource-share__content > footer > button');
        const GA_Share_Close = await page.$('.pt-popupv2__content.is-middle.datasource-share__content > footer > button');
        await GA_Share_Close.click();
        await page.waitFor(3000);

		// Case_05
		const Case_05 = 'Case_05: Logout and Login Datadeck with dd_auto_jp214@mailinator.com.';
		log(Case_05);
		// Logout jp213
		await page.waitForSelector('.pt-account > div > h1');
		const Space_Name = await page.$('.pt-account > div > h1');
		await Space_Name.click();
		await page.waitFor(1000);
		await page.waitForSelector('.pt-account > div.account-menu > div.account-menu__item.last-child');
		const Logout_jp213 = await page.$('.pt-account > div.account-menu > div.account-menu__item.last-child');
		await Logout_jp213.click();
		await page.waitFor(5000);
		// Login jp214
		await page.waitForSelector('.pt-ui-button__text');
		await page.type('[name=email]', 'dd_auto_jp214@mailinator.com', {delay: 20});
		await page.type('[name=userPassword]', '123456', {delay: 20});
		const authLogin_jp214 = await page.$('.pt-ui-button');
		await authLogin_jp214.click();
		await page.waitFor(3000);
		await page.waitForSelector('.pt-main__header > div.freetrial-tips.freetrail-tips > div');

		// Case_06
		const Case_06 = 'Case_06: Check ManageData_ShareUser_List. Capture [dd_ui_ManageData_ShareUser_List.jpg]. Excepted: ' + exp.Case_06;
		log(Case_06);
		await page.waitForSelector('.linkList > a.item.data-manage > div');
		const ManageData_Item_2 = await page.$('.linkList > a.item.data-manage > div');
		await ManageData_Item_2.click();
		await page.waitFor(1000);
		await page.screenshot({
			path: './pic/dd_ui_ManageData_ShareUser_List.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});
		await page.waitForSelector('.connection-list__col-name > span.connection-list__name');
		let ManageData_List_TitleName = await page.$$eval('.connection-list__col-name', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
		let ManageData_List_TitleName_Sort = ManageData_List_TitleName.sort();
        let Case_06_Act = ManageData_List_TitleName_Sort.join(',');
        let Case_06_Res = 'Case_06_Res: ' + cps(exp.Case_06, Case_06_Act);
        log(Case_06_Res);

        // Case_07
		const Case_07 = 'Case_07: Logout and Login Datadeck with dd_auto_jp213@mailinator.com.';
		log(Case_07);
		// Logout jp214
		await page.waitForSelector('.pt-account > div > h1');
		const Space_Name_2 = await page.$('.pt-account > div > h1');
		await Space_Name_2.click();
		await page.waitFor(1000);
		await page.waitForSelector('.pt-account > div.account-menu > div.account-menu__item.last-child');
		const Logout_jp214 = await page.$('.pt-account > div.account-menu > div.account-menu__item.last-child');
		await Logout_jp214.click();
		await page.waitFor(5000);
		// Login jp213
		await page.waitForSelector('.pt-ui-button__text');
		await page.type('[name=email]', 'dd_auto_jp213@mailinator.com', {delay: 20});
		await page.type('[name=userPassword]', '123456', {delay: 20});
		const authLogin_jp213 = await page.$('.pt-ui-button');
		await authLogin_jp213.click();
		await page.waitFor(3000);
		await page.waitForSelector('.pt-main__header > div.freetrial-tips.freetrail-tips > div');

		// Case_08
		const Case_08 = 'Case_08: Check ManageData_Cancel_Share_Upload. Excepted: ' + exp.Case_08;
		log(Case_08);
		await page.waitForSelector('.linkList > a.item.data-manage > div');
		const ManageData_Item_3 = await page.$('.linkList > a.item.data-manage > div');
		await ManageData_Item_3.click();
		await page.waitFor(1000);
		// 过滤Excel/CSV
		await page.waitForSelector('.connection__header > div.connection-searchwrap > div.connection-searchwrap__input-name > div > input');
		const ManageData_Search_Input_3 = await page.$('.connection__header > div.connection-searchwrap > div.connection-searchwrap__input-name > div > input');
		await ManageData_Search_Input_3.click();
		await page.waitFor(1000);
		await ManageData_Search_Input_3.type('Excel/CSV', {delay: 20});
		// 点击 Share 按钮
		await page.waitForSelector('.connection-list__col-share > div > a');
		const Share_Button_Upload_3 = await page.$('.connection-list__col-share > div > a');
		await Share_Button_Upload_3.click();
		await page.waitFor(1000);
		// 移除 jp214
		await page.waitForSelector('.pt-cooperation__list > div > div > ul > li:nth-child(2) > div.change-role > div > div > div');
		const Role_Dropdown = await page.$('.pt-cooperation__list > div > div > ul > li:nth-child(2) > div.change-role > div > div > div');
		await Role_Dropdown.click();
		await page.waitFor(1000);
		await page.waitForSelector('.change-role > div > div.pt-select__dropdown > div > div > ul > li:nth-child(4)');
		const Role_Dropdown_Remove = await page.$('.change-role > div > div.pt-select__dropdown > div > div > ul > li:nth-child(4)');
		await Role_Dropdown_Remove.click();
		await page.waitFor(1000);
		await page.waitForSelector('.pt-cooperation__list-info > div.name > span');
		let Upload_Share_UserList_2 = await page.$$eval('.pt-cooperation__list-info > div.name > span', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
		let Upload_Share_UserList_2_Sort = Upload_Share_UserList_2.sort();
        let Case_08_Act = Upload_Share_UserList_2_Sort.join(',');
        let Case_08_Res = 'Case_08_Res: ' + cps(exp.Case_08, Case_08_Act);
        log(Case_08_Res);
        await page.waitForSelector('.pt-popupv2__content.is-middle.datasource-share__content > footer > button');
        const Upload_Share_Close_2 = await page.$('.pt-popupv2__content.is-middle.datasource-share__content > footer > button');
        await Upload_Share_Close_2.click();
        await page.waitFor(3000);

        // Case_09
		const Case_09 = 'Case_09: Check ManageData_Cancel_Share_GA. Excepted: ' + exp.Case_09;
		log(Case_09);
		// 清除 Upload 检索条件
		await page.waitForSelector('.connection__header > div.connection-searchwrap > div.connection-searchwrap__input-name > div > input');
		const ManageData_Search_Input_ClearUpload_2 = await page.waitForSelector('.pt-input__inner__clearButton');
		await ManageData_Search_Input_ClearUpload_2.click();
		// 过滤 Google Analytics
		await page.waitForSelector('.connection__header > div.connection-searchwrap > div.connection-searchwrap__input-name > div > input');
		const ManageData_Search_Input_4 = await page.$('.connection__header > div.connection-searchwrap > div.connection-searchwrap__input-name > div > input');
		await ManageData_Search_Input_4.click();
		await page.waitFor(1000);
		await ManageData_Search_Input_4.type('Google Analytics', {delay: 20});
		// 点击 Share 按钮
		await page.waitForSelector('.connection-list__col-share > div > a');
		const Share_Button_Upload_4 = await page.$('.connection-list__col-share > div > a');
		await Share_Button_Upload_4.click();
		await page.waitFor(1000);
		// 移除 jp214
		await page.waitForSelector('.pt-cooperation__list > div > div > ul > li:nth-child(2) > div.change-role > div > div > div');
		const Role_Dropdown_4 = await page.$('.pt-cooperation__list > div > div > ul > li:nth-child(2) > div.change-role > div > div > div');
		await Role_Dropdown_4.click();
		await page.waitFor(1000);
		await page.waitForSelector('.change-role > div > div.pt-select__dropdown > div > div > ul > li:nth-child(4)');
		const Role_Dropdown_Remove_4 = await page.$('.change-role > div > div.pt-select__dropdown > div > div > ul > li:nth-child(4)');
		await Role_Dropdown_Remove_4.click();
		await page.waitFor(1000);
		await page.waitForSelector('.pt-cooperation__list-info > div.name > span');
		let GA_Share_UserList_2 = await page.$$eval('.pt-cooperation__list-info > div.name > span', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
		let GA_Share_UserList_2_Sort = GA_Share_UserList_2.sort();
        let Case_09_Act = GA_Share_UserList_2_Sort.join(',');
        let Case_09_Res = 'Case_09_Res: ' + cps(exp.Case_09, Case_09_Act);
        log(Case_09_Res);
        await page.waitForSelector('.pt-popupv2__content.is-middle.datasource-share__content > footer > button');
        const GA_Share_Close_2 = await page.$('.pt-popupv2__content.is-middle.datasource-share__content > footer > button');
        await GA_Share_Close_2.click();
        await page.waitFor(3000);

		await page.waitFor(5000);

		// log
		const log_server_1 = 'log_server_1: 【AT_DD_Online_UI_ManageDataShare】 runs Finished.';
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
			+ Case_04_1_Res + '\r\n'
			+ Case_05 + '\r\n'
			+ Case_06 + '\r\n'
			+ Case_06_Res + '\r\n'
			+ Case_07 + '\r\n'
			+ Case_08 + '\r\n'
			+ Case_08_Res + '\r\n'
			+ Case_09 + '\r\n'
			+ Case_09_Res + '\r\n'
			+ log_server_1 + '\r\n', 'UTF8');
		writerStream.end();

	} catch (e) {
		if (e instanceof TimeoutError) {
			console.error(e);
			const log_block = 'Log_Block: Service unexpected termination! 【AT_DD_Online_UI_ManageDataShare】 runs Error!';
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




