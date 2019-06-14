
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
	Case_02: 'Let\'s connect your first data source',   // 数据管理空白页引导提示标题
	Case_03: 'What data would you like to use?',  // 选择数据源页面，标题内容
	Case_04: 'Add MySQL connection',  // 添加MySQL数据源连接弹框，标题内容
	Case_05: 'Select a table',  // 选择数据表，标题内容
	Case_06: 'Format your table',  // 数据表格式，标题内容
	Case_07: 'Auto_UI_MySQL',  // 新添加MySQL连接名称
	Case_07_1: 'autotest_table',  // 新添加MySQL的连接表名称
	Case_08: '0 cards created previously are using the table from “autotest_table” ! Removing this data source will leave those cards blank. Are you sure to continue?',  // 删除数据表确认提示
	Case_09: '0 cards created previously are using the connection from “Auto_UI_MySQL” ! Removing this data source will leave those cards blank. Are you sure to continue?',  // 删除连接记录确认提示
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
		const Case_01 = 'Case_01: Login Datadeck dd_auto_jp211@mailinator.com.';
		log(Case_01);
		await page.goto('https://dashv2.datadeck.com/login');
		await page.waitForSelector('.pt-ui-button__text');
		const documentSize = await page.evaluate(() => {
			return {
				width: document.documentElement.clientWidth,
				height: document.body.clientHeight,
			}
		});
		await page.type('[name=email]', 'dd_auto_jp211@mailinator.com', {delay: 20});
		await page.type('[name=userPassword]', '123456', {delay: 20});
		const authLogin = await page.$('.pt-ui-button');
		await authLogin.click();
		await page.waitForSelector('.pt-main__content-tips-item > button');

		// Case_02
		const Case_02 = 'Case_02: Check ManageData_Blank page. Capture [dd_ui_ManageData_Blank.jpg]. Excepted: ' + exp.Case_02;
		log(Case_02);
		await page.waitForSelector('.linkList > a.item.data-manage > div');
		const ManageData_Item = await page.$('.linkList > a.item.data-manage > div');
		await ManageData_Item.click();
		await page.waitForSelector('.connection_scrollbar-wrapper > div.pt-main__content-tips-wrap > div.pt-main__content-tips-item > button > span');
		let Case_02_Act = await page.$eval('.connection_scrollbar-wrapper > div.pt-main__content-tips-wrap > div.pt-main__content-tips-item > div.pt-main__content-tips-item-title', el => el.innerText);
		let Case_02_Res = 'Case_02_Res: ' + cps(exp.Case_02, Case_02_Act);
		log(Case_02_Res);
		await page.waitFor(1000);
		await page.screenshot({
			path: './pic/dd_ui_ManageData_Blank.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_03
		const Case_03 = 'Case_03: Check Conn_Select_DS page. Capture [dd_ui_Conn_Select_DS.jpg]. Excepted: ' + exp.Case_03;
		log(Case_03);
		const Conn_DS = await page.$('.connection_scrollbar-wrapper > div.pt-main__content-tips-wrap > div.pt-main__content-tips-item > button');
		await Conn_DS.click();
		await page.waitForSelector('#ds-card__mysql > div');
		let Case_03_Act = await page.$eval('.datasource-choose > div.datasource-choose__header > div > div.title', el => el.innerText);
		let Case_03_Res = 'Case_03_Res: ' + cps(exp.Case_03, Case_03_Act);
		log(Case_03_Res);
		await page.screenshot({
			path: './pic/dd_ui_Conn_Select_DS.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_04
		const Case_04 = 'Case_04: Check Conn_Add_MySQL_connection window. Capture [dd_ui_Conn_Add_MySQL.jpg]. Excepted: ' + exp.Case_04;
		log(Case_04);
		const Conn_Select_DS = await page.$('#ds-card__mysql');
		await Conn_Select_DS.click();
		await page.waitForSelector('.pt-popupv2__content.create-connection__popupv2 > header > h3 > span');
		await page.waitFor(2000);
		let Case_04_Act = await page.$eval('.pt-popupv2__content.create-connection__popupv2 > header > h3 > span', el => el.innerText);
		let Case_04_Res = 'Case_04_Res: ' + cps(exp.Case_04, Case_04_Act);
		log(Case_04_Res);
		await page.screenshot({
			path: './pic/dd_ui_Conn_Add_MySQL.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_05
		const Case_05 = 'Case_05: Check Conn_Select_a_table. Capture [dd_ui_Conn_Select_a_table.jpg]. Excepted: ' + exp.Case_05;
		log(Case_05);
		await page.waitForSelector('.pt-popupv2__main > div > div > div > div > div > div:nth-child(1) > label');
		await page.type('[name=connectionName]', 'Auto_UI_MySQL', {delay: 20});
		await page.type('[name=host]', 'initdbtest.ptengine.com', {delay: 20});
		await page.type('[name=port]', '23308', {delay: 20});
		await page.type('[name=user]', 'datadeck_test', {delay: 20});
		await page.type('[name=password]', 'OqiAdTulRO', {delay: 20});
		await page.type('[name=dataBaseName]', 'datadeck_test', {delay: 20});
		const Conn_Connect_button = await page.$('.pt-popupv2__content.create-connection__popupv2 > footer > button');
		await Conn_Connect_button.click();
		await page.waitFor(5000);
		let Case_05_Act = await page.$eval('.pt-main__container > div.pt-main__content > div.all_pop > div > div > div.title', el => el.innerText);
		let Case_05_Res = 'Case_05_Res: ' + cps(exp.Case_05, Case_05_Act);
		log(Case_05_Res);
		await page.screenshot({
			path: './pic/dd_ui_Conn_Select_a_table.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_06
		const Case_06 = 'Case_06: Check Conn_Format_your_table. Capture [dd_ui_Conn_Format_your_table.jpg]. Excepted: ' + exp.Case_06;
		log(Case_06);
		await page.waitForSelector('.search > div.file_search.has-prefix.pt-input.pt-input--default.pt-input_underline > input');
		await page.waitFor(2000);
		const Conn_table_Search = await page.$('.search > div.file_search.has-prefix.pt-input.pt-input--default.pt-input_underline > input');
		await Conn_table_Search.focus();
		await Conn_table_Search.type('autotest_table', {delay: 20});
		const Conn_autotest_table = await page.$('.file_content > div > div.file_content--item > div:nth-child(2) > div > div:nth-child(2) > div:nth-child(1) > div > div > div.text');
		await Conn_autotest_table.click();
		await page.waitFor(5000);
		let Case_06_Act = await page.$eval('.create-zone__table > div.create-zone__data-control > h3', el => el.innerText);
		let Case_06_Res = 'Case_06_Res: ' + cps(exp.Case_06, Case_06_Act);
		log(Case_06_Res);
		await page.screenshot({
			path: './pic/dd_ui_Conn_Format_your_table.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_07
		const Case_07 = 'Case_07: Check ManageData_MySQL_table_New. Capture [dd_ui_ManageData_MySQL_table_New.jpg]. Excepted: ' + exp.Case_07;
		log(Case_07);
		const Format_table_Confirm = await page.$('.create-zone__table > div.create-zone__data-control > div.tools > button');
		await Format_table_Confirm.click();
		await page.waitForSelector('.connection-list__main > div.connection-list__col-name > span.connection-list__name');
		await page.waitFor(3000);
		let Case_07_Act = await page.$eval('.connection-list__main > div.connection-list__col-name > span.connection-list__name', el => el.innerText);
		let Case_07_Res = 'Case_07_Res: ' + cps(exp.Case_07, Case_07_Act);
		log(Case_07_Res);
		let Case_07_1_Act = await page.$eval('.connection-list__subs > div > div.connection-list__col-name > span.connection-list__name', el => el.innerText);
		let Case_07_1_Res = 'Case_07_1_Res: ' + cps(exp.Case_07_1, Case_07_1_Act);
		log(Case_07_1_Res);
		await page.screenshot({
			path: './pic/dd_ui_ManageData_MySQL_table_New.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_08
		const Case_08 = 'Case_08: Check Delete_Table_Confirm window. Capture [dd_ui_Delete_Table_Confirm.jpg]. Excepted: ' + exp.Case_08;
		log(Case_08);
		await page.waitForSelector('.connection-list__subs > div > div.connection-list__col-tool > span > span > span');
		const Table_More = await page.$('.connection-list__subs > div > div.connection-list__col-tool > span > span > span');
		await Table_More.click();
		await page.waitForSelector('body > ul > div > li:nth-child(4) > span > span');
		const Table_Delete = await page.$('body > ul > div > li:nth-child(4) > span > span');
		await Table_Delete.click();
		await page.waitForSelector('body > div.pt-confirm-backdrop > div > section');
		let Case_08_Act = await page.$eval('body > div.pt-confirm-backdrop > div > section', el => el.innerText);
		let Case_08_Res = 'Case_08_Res: ' + cps(exp.Case_08, Case_08_Act);
		log(Case_08_Res);
		await page.waitFor(3000);
		await page.screenshot({
			path: './pic/dd_ui_Delete_Table_Confirm.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});
		const Table_Delete_Button = await page.$('body > div.pt-confirm-backdrop > div > footer > button.pt-ui-button.pt-ui-button--primary.pt-ui-button--type-default.pt-ui-button--size-big');
		await Table_Delete_Button.click();
		await page.waitFor(2000);

		// Case_09
		const Case_09 = 'Case_09: Check Delete_Conn_Confirm window. Capture [dd_ui_Delete_Conn_Confirm.jpg]. Excepted: ' + exp.Case_09;
		log(Case_09);
		await page.waitForSelector('.connection-list__col-tool > span > span > span');
		const Conn_More = await page.$('.connection-list__col-tool > span > span > span');
		await Conn_More.click();
		await page.waitForSelector('body > ul > li.dropdown.dropdown--default.dropdown-delect-hover > span > span');
		const Conn_Delete = await page.$('body > ul > li.dropdown.dropdown--default.dropdown-delect-hover > span > span');
		await Conn_Delete.click();
		await page.waitForSelector('body > div.pt-confirm-backdrop > div > section');
		let Case_09_Act = await page.$eval('body > div.pt-confirm-backdrop > div > section', el => el.innerText);
		let Case_09_Res = 'Case_09_Res: ' + cps(exp.Case_09, Case_09_Act);
		log(Case_09_Res);
		await page.waitFor(3000);
		await page.screenshot({
			path: './pic/dd_ui_Delete_Conn_Confirm.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});
		const Conn_Delete_Button = await page.$('body > div.pt-confirm-backdrop > div > footer > button.pt-ui-button.pt-ui-button--primary.pt-ui-button--type-default.pt-ui-button--size-big');
		await Conn_Delete_Button.click();
		await page.waitFor(2000);

		// log
		const log_server_1 = 'log_server_1: 【AT_DD_Online_UI_ManageData】 runs Finished.';
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
			+ Case_07_1_Res + '\r\n'
			+ Case_08 + '\r\n'
			+ Case_08_Res + '\r\n'
			+ Case_09 + '\r\n'
			+ Case_09_Res + '\r\n'
			+ log_server_1 + '\r\n', 'UTF8');
		writerStream.end();

	} catch (e) {
		if (e instanceof TimeoutError) {
			console.error(e);
			const log_block = 'Log_Block: Service unexpected termination! 【AT_DD_Online_UI_ManageData】 runs Error!';
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




