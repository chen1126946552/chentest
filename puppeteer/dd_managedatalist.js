
const puppeteer = require('puppeteer');
const {TimeoutError} = require('puppeteer/Errors');  // Error handling
const fs = require('fs');
const log = console.log;  // 缩写 console.log

function cps(Exp, Act) {
	if (Act.includes(Exp)) {
		return '检查点匹配'
	}
	else {
		return '检查点不匹配'
	}
}

let exp = {
	Case_02: 'Title\nConnected date\nLast updated\nMembers',   // 数据管理列表标题
	Case_03: 'Auto_UI_MySQL,Ptmind_jp,Title,YDN_UI_Auto,YSS_UI_Auto,autotest_table.csv,bin.wu@ptengine.com,bin.wu@ptengine.com,chen.chen@ptmind.com,chenchen0503@outlook.com,dev-info-lead@synergy101.jp,guy.geeraedts@ptengine.com,marketing@ptengine.com,marketing@ptengine.com,marketing@ptengine.com,mkt@datadeck.com,peterangel536@gmail.com',  // ND一级列表
	Case_04: 'All data sources,Excel/CSV,Facebook Pages,Google Adsense,Google Adwords,Google Analytics,Google Drive,Google Search Console,MailChimp,MySQL,One Drive,Ptengine,Salesforce,Twitter (Beta),Yahoo Ads Sponsored Search,Yahoo Ads YDN,',  // DM页面过滤下拉项
	Case_05: 'Rename,Edit data format,Update file,Delete',  // Upload更多下拉列表项
	Case_06: 'Delete',  // GA更多下拉列表项
	Case_07: 'Edit connection,Connect a table,Delete',  // MySQL连接下拉列表项
	Case_07_1: 'Edit data format,Update table schema,Delete', // MySQL数据表下拉列表项
	Case_08: 'Connect a file,Delete', // OneDrive连接下拉列表项
	Case_08_1: 'Edit data format,Update file,Delete', // OneDrive数据表下拉列表项
	Case_09: 'Amazon RDS for Aurora,Amazon RDS for MySQL,Amazon Redshift,AmazonS3,Blend data,Excel/CSV,Facebook Ads,Facebook Pages,Google Adsense,Google Adwords,Google Analytics,Google BigQuery,Google Drive,Google Search Console,Linkedin,MailChimp,MySQL,One Drive,Oracle,PostgreSQL,Ptengine,Refersion (Beta),SQL Server,Salesforce,Shopify (Beta),Stripe,Stripe,Trello,Twitter (Beta),Twitter Ads (Beta),Yahoo Ads Sponsored Search,Yahoo Ads YDN,Youtube,Zapier',  // 数据源列表名称
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
		const Case_02 = 'Case_02: Check ManageData_List page. Capture [dd_ui_ManageData_List.jpg]. Excepted: ' + exp.Case_02;
		log(Case_02);
		await page.waitForSelector('.linkList > a.item.data-manage > div');
		const ManageData_Item = await page.$('.linkList > a.item.data-manage > div');
		await ManageData_Item.click();
		await page.waitForSelector('.connection-list > div.connection-list__header > div');
		let Case_02_Act = await page.$eval('.connection-list > div.connection-list__header > div', el => el.innerText);
		let Case_02_Res = 'Case_02_Res: ' + cps(exp.Case_02, Case_02_Act);
		log(Case_02_Res);
		await page.waitFor(1000);
		await page.screenshot({
			path: './pic/dd_ui_ManageData_List.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});

		// Case_03
		const Case_03 = 'Case_03: Check ManageData_List_TitleName. Excepted: ' + exp.Case_03;
		log(Case_03);
		await page.waitForSelector('.connection-list__col-name > span.connection-list__name');
		let ManageData_List_TitleName = await page.$$eval('.connection-list__col-name', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
		let ManageData_List_TitleName_Sort = ManageData_List_TitleName.sort();
        let Case_03_Act = ManageData_List_TitleName_Sort.join(',');
        let Case_03_Res = 'Case_03_Res: ' + cps(exp.Case_03, Case_03_Act);
        log("03  "+ Case_03_Act)
        log(Case_03_Res);

		// Case_04
		const Case_04 = 'Case_04: Check ManageData_List_Filter. Excepted: ' + exp.Case_04;
		log(Case_04);
		await page.waitForSelector('.connection__header > div.connection-searchwrap > div.connection-searchwrap__select-type > div > div > div');
		const ManageData_List_Filter = await page.$('.connection__header > div.connection-searchwrap > div.connection-searchwrap__select-type > div > div > div');
		await ManageData_List_Filter.click();
		await page.waitFor(1000);
		await page.waitForSelector('.pt-dropdown-vnew__dropdown-item');
		let ManageData_List_Filter_Items = await page.$$eval('.pt-dropdown-vnew__dropdown-item', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
        let Case_04_Act = ManageData_List_Filter_Items.join(',');
        let Case_04_Res = 'Case_04_Res: ' + cps(exp.Case_04, Case_04_Act);
        log("04   "+Case_04_Act)
        log(Case_04_Res);

		// Case_05
		const Case_05 = 'Case_05: Check ManageData_Conn_Upload_Items. Excepted: ' + exp.Case_05;
		log(Case_05);
		await page.waitForSelector('.connection__header > div.connection-searchwrap > div.connection-searchwrap__input-name > div > input');
		const ManageData_Search_Input = await page.$('.connection__header > div.connection-searchwrap > div.connection-searchwrap__input-name > div > input');
		await ManageData_Search_Input.click();
		await ManageData_Search_Input.type('Excel/CSV', {delay: 20});
		await page.waitFor(1000);
		await page.waitForSelector('.connection-list__col-tool > span > span > span');
		const Conn_Upload_More = await page.$('.connection-list__col-tool > span > span > span');
		await Conn_Upload_More.click();
		await page.waitFor(1000);
		await page.waitForSelector('body > ul > li > span');
		let Conn_Upload_More_Items = await page.$$eval('body > ul > li > span', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
        let Case_05_Act = Conn_Upload_More_Items.join(',');
        let Case_05_Res = 'Case_05_Res: ' + cps(exp.Case_05, Case_05_Act);
        log(Case_05_Res);

		// Case_06
		const Case_06 = 'Case_06: Check ManageData_Conn_GA_Items. Excepted: ' + exp.Case_06;
		log(Case_06);
		await page.waitForSelector('.connection__header > div.connection-searchwrap > div.connection-searchwrap__input-name > div > input');
		const ManageData_Search_Input_ClearUpload = await page.waitForSelector('.pt-input__inner__clearButton');
		await ManageData_Search_Input_ClearUpload.click();
		const ManageData_Search_Input_GA = await page.$('.connection__header > div.connection-searchwrap > div.connection-searchwrap__input-name > div > input');
		await ManageData_Search_Input_GA.click();
		await ManageData_Search_Input_GA.type('Google Analytics', {delay: 20});
		await page.waitFor(1000);
		await page.waitForSelector('.connection-list__col-tool > span > span > span');
		const Conn_GA_More = await page.$('.connection-list__col-tool > span > span > span');
		await Conn_GA_More.click();
		await page.waitFor(1000);
		await page.waitForSelector('body > ul > li > span');
		let Conn_GA_More_Items = await page.$$eval('body > ul > li > span', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
        let Case_06_Act = Conn_GA_More_Items.join(',');
        let Case_06_Res = 'Case_06_Res: ' + cps(exp.Case_06, Case_06_Act);
        log(Case_06_Res);

		// Case_07
		const Case_07 = 'Case_07: Check ManageData_Conn_MySQL_Items. Excepted: ' + exp.Case_07;
		log(Case_07);
		await page.waitForSelector('.connection__header > div.connection-searchwrap > div.connection-searchwrap__input-name > div > input');
		const ManageData_Search_Input_ClearGA = await page.waitForSelector('.pt-input__inner__clearButton');
		await ManageData_Search_Input_ClearGA.click();
		const ManageData_Search_Input_MySQL = await page.$('.connection__header > div.connection-searchwrap > div.connection-searchwrap__input-name > div > input');
		await ManageData_Search_Input_MySQL.click();
		await ManageData_Search_Input_MySQL.type('MySQL', {delay: 20});
		await page.waitFor(1000);
		// MySQL连接
		await page.waitForSelector('.connection-list__col-tool > span > span > span');
		const Conn_MySQL_More = await page.$('.connection-list__col-tool > span > span > span');
		await Conn_MySQL_More.click();
		await page.waitFor(1000);
		await page.waitForSelector('body > ul > li > span');
		let Conn_MySQL_More_Items = await page.$$eval('body > ul > li > span', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
        let Case_07_Act = Conn_MySQL_More_Items.join(',');
        let Case_07_Res = 'Case_07_Res: ' + cps(exp.Case_07, Case_07_Act);
        log(Case_07_Res);
        await Conn_MySQL_More.click();
        await page.waitFor(1000);
        // 数据表
        await page.waitForSelector('.connection-list__subs > div > div.connection-list__col-tool > span > span > span');
		const Conn_MySQL_Sub_More = await page.$('.connection-list__subs > div > div.connection-list__col-tool > span > span > span');
		await Conn_MySQL_Sub_More.click();
		await page.waitFor(1000);
		await page.waitForSelector('body > ul > div > li > span');
		let Conn_MySQL_Sub_More_Items = await page.$$eval('body > ul > div > li > span', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
        let Case_07_1_Act = Conn_MySQL_Sub_More_Items.join(',');
        let Case_07_1_Res = 'Case_07_1_Res: ' + cps(exp.Case_07_1, Case_07_1_Act);
        log(Case_07_1_Res);

        // Case_08
		const Case_08 = 'Case_08: Check ManageData_Conn_OneDrive_Items. Excepted: ' + exp.Case_08;
		log(Case_08);
		await page.waitForSelector('.connection__header > div.connection-searchwrap > div.connection-searchwrap__input-name > div > input');
		const ManageData_Search_Input_ClearMySQL = await page.waitForSelector('.pt-input__inner__clearButton');
		await ManageData_Search_Input_ClearMySQL.click();
		const ManageData_Search_Input_OneDrive = await page.$('.connection__header > div.connection-searchwrap > div.connection-searchwrap__input-name > div > input');
		await ManageData_Search_Input_OneDrive.click();
		await ManageData_Search_Input_OneDrive.type('One Drive', {delay: 20});
		await page.waitFor(1000);
		// OneDrive连接
		await page.waitForSelector('.connection-list__col-tool > span > span > span');
		const Conn_OneDrive_More = await page.$('.connection-list__col-tool > span > span > span');
		await Conn_OneDrive_More.click();
		await page.waitFor(1000);
		await page.waitForSelector('body > ul > li > span');
		let Conn_OneDrive_More_Items = await page.$$eval('body > ul > li > span', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
        let Case_08_Act = Conn_OneDrive_More_Items.join(',');
        let Case_08_Res = 'Case_08_Res: ' + cps(exp.Case_08, Case_08_Act);
        log(Case_08_Res);
        await Conn_OneDrive_More.click();
        await page.waitFor(1000);
        // 数据表
        await page.waitForSelector('.connection-list__subs > div > div.connection-list__col-tool > span > span > span');
		const Conn_OneDrive_Sub_More = await page.$('.connection-list__subs > div > div.connection-list__col-tool > span > span > span');
		await Conn_OneDrive_Sub_More.click();
		await page.waitFor(1000);
		await page.waitForSelector('body > ul > div > li > span');
		let Conn_OneDrive_Sub_More_Items = await page.$$eval('body > ul > div > li > span', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
        let Case_08_1_Act = Conn_OneDrive_Sub_More_Items.join(',');
        let Case_08_1_Res = 'Case_08_1_Res: ' + cps(exp.Case_08_1, Case_08_1_Act);
        log(Case_08_1_Res);

        // Case_09
		const Case_09 = 'Case_09: Check ManageData_Conn_DSList_DSName. Excepted: ' + exp.Case_09;
		log(Case_09);
        await page.waitForSelector('.ds-manager > div > div > div.connection__wrap > div.connection__header > div.controlbutton > button');
        const Connect_DS_Button = await page.$('.ds-manager > div > div > div.connection__wrap > div.connection__header > div.controlbutton > button');
        await Connect_DS_Button.click();
        await page.waitFor(2000);
        await page.waitForSelector('#ds-card__googleanalytics-v4');
		let Conn_DSList_DSName = await page.$$eval('.ds-card__name.pt-tooltip', els => {
			return els.map(v => {
				return v.innerText;
			});
		});
		let DSList_DSName_Sort = Conn_DSList_DSName.sort();
		let Case_09_Act = DSList_DSName_Sort.join(',');
		log(Case_09_Act)
		let Case_09_Res = 'Case_09_Res: ' + cps(exp.Case_09, Case_09_Act);
		log(Case_09_Res);
		await page.screenshot({
			path: './pic/dd_ui_ManageData_DSList.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});

        await page.waitFor(5000);

		// log
		const log_server_1 = 'log_server_1: 【AT_DD_Online_UI_ManageDataList】 runs Finished.';
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
			+ Case_08_1_Res + '\r\n'
			+ Case_09 + '\r\n'
			+ Case_09_Res + '\r\n'
			+ log_server_1 + '\r\n', 'UTF8');
		writerStream.end();

	} catch (e) {
		if (e instanceof TimeoutError) {
			console.error(e);
			const log_block = 'Log_Block: Service unexpected termination! 【AT_DD_Online_UI_ManageDataList】 runs Error!';
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




