
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
	Case_02: 'Template Category',   // Template Gallery页面，搜索条件标题
	Case_03: ' All, Marketing, Advertising, Analytics, CRM & Sales, Social Media, Ecommerce, Other',  // Template Gallery页面，待选关键词
	Case_04: 'Google Analytics Overview',  // 创建订阅弹框标题
	Case_05: 'This pre-built template will help you quickly get a snapshot of your key metrics in Google Analytics.', // Google Analytics Overview面板模板，描述信息
	Case_06: 'Users,Sessions,Pageviews,Avg. Time on page,Bounce rate,% New Sessions,Avg. session duration,Number of sessions per user', // Google Analytics Overview面板模板，Key Metrics
	Case_07: 'Traffic Overview,New Sessions %,Bounce Rate,Time on Site,Visits per User,User Acquistion by Source,Top Aquisition Source,Most Visited Pages,User Location', // Google Analytics Overview面板模板,widgets Name
	Case_08: 'Connect with Google Analytics', // Connect with Google Analytics按钮名
	Case_09: 'Connect your data source', // 连接弹框标题
	Case_11: 'Google Analytics Overview', // 新添加的面板标题
	Case_12: 'Are you sure you want to delete dashboard"Google Analytics Overview"?', // 删除面板确认提示内容
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
		// 输入用户密码登录
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
		await page.waitForSelector('#app > div > div.pt-main__aside.pt-main__aside > div > div > div.pt-account');
		await page.waitFor(3000);

		// Case_02
		const Case_02 = 'Case_02: Check Template_Gallery page. Capture [dd_ui_Template_Gallery.jpg]. Excepted: ' + exp.Case_02;
		log(Case_02);
		await page.waitForSelector('.linkList > a.item.template-gallery > div');
		const Template_Gallery = await page.$('.linkList > a.item.template-gallery > div');
		await Template_Gallery.click();
		await page.waitFor(1000);
		await page.waitForSelector('.pt-main__content > div.tmpg > div.tmpg__search > div.tmpg-categories > p');
		let Case_02_Act = await page.$eval('.pt-main__content > div.tmpg > div.tmpg__search > div.tmpg-categories > p', el => el.innerText);
		let Case_02_Res = 'Case_02_Res: ' + cps(exp.Case_02, Case_02_Act);
		log(Case_02_Res);
		await page.screenshot({
			path: './pic/dd_ui_Template_Gallery.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_03
		const Case_03 = 'Case_03: Check Template_Gallery_Keywords. Excepted: ' + exp.Case_03;
		log(Case_03);
		await page.waitForSelector('.tmpg-categories__item');
		let Template_Gallery_Keywords = await page.$$eval('.tmpg-categories__item', els => {
			return els.map(v => {
				return v.innerText;
			});
		});
		let Case_03_Act = Template_Gallery_Keywords.join(',');
		let Case_03_Res = 'Case_03_Res: ' + cps(exp.Case_03, Case_03_Act);
		log(Case_03_Res);
		await page.waitFor(1000);

		// Case_04
		const Case_04 = 'Case_04: Check Template_Gallery_PanelName. Excepted: ' + exp.Case_04;
		log(Case_04);
		await page.waitForSelector('.tmpg-card__title');
		let Template_Gallery_PanelNames = await page.$$eval('.tmpg-card__title', els => {
			return els.map(v => {
				return v.innerText;
			});
		});
		let Case_04_Act = Template_Gallery_PanelNames.join(',');
		let Case_04_Res = 'Case_04_Res: ' + cps(exp.Case_04, Case_04_Act);
		log(Case_04_Res);
		log("04  " + Case_04_Act);
		await page.waitFor(1000);

		// Case_05
		const Case_05 = 'Case_05: Check Template_GA_Overview. Capture [dd_ui_Template_GA_Overview.jpg]. Excepted: ' + exp.Case_05;
		log(Case_05);
		// 选择 Google Analytics Overview 进入面板模板
		await page.waitForSelector('.tmpg-list.tmpg__autoWidth > div:nth-child(1) > a > p.tmpg-card__footer');
		const Template_Gallery_Panel = await page.$('.tmpg-list.tmpg__autoWidth > div:nth-child(1) > a > p.tmpg-card__footer');
		await Template_Gallery_Panel.click();
		await page.waitFor(3000);
		await page.waitForSelector('.pt-main__content > div.glyd > div.glyd__scroll > div > p:nth-child(2)');
		let Case_05_Act = await page.$eval('.pt-main__content > div.glyd > div.glyd__scroll > div > p:nth-child(2)', el => el.innerText);
		let Case_05_Res = 'Case_05_Res: ' + cps(exp.Case_05, Case_05_Act);
		log(Case_05_Res);
		const documentSize_1 = await page.evaluate(() => {
			return {
				width: document.documentElement.clientWidth,
				height: document.body.clientHeight,
			}
		});
		await page.screenshot({
			path: './pic/dd_ui_Template_GA_Overview.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize_1.height
			}
		});

		// Case_06
		const Case_06 = 'Case_06: Check Template_GA_Overview_KM. Capture [dd_ui_Template_GA_Overview_KM.jp]. Excepted: ' + exp.Case_06;
		log(Case_06);
		await page.waitForSelector('.glyd-metrics > ul > li');
		let Template_GA_Overview_KM = await page.$$eval('.glyd-metrics > ul > li', els => {
			return els.map(v => {
				return v.innerText;
			});
		});
		let Case_06_Act = Template_GA_Overview_KM.join(',');
		let Case_06_Res = 'Case_06_Res: ' + cps(exp.Case_06, Case_06_Act);
		log(Case_06_Res);
		await page.waitFor(1000);

		// Case_07
		const Case_07 = 'Case_07: Check Template_GA_Overview_Widgets. Capture [dd_ui_Template_GA_Overview_Widgets.jp]. Excepted: ' + exp.Case_07;
		log(Case_07);
		await page.waitForSelector('.widget__header__title > span');
		let Template_GA_Overview_Widgets = await page.$$eval('.widget__header__title > span', els => {
			return els.map(v => {
				return v.innerText;
			});
		});
		let Case_07_Act = Template_GA_Overview_Widgets.join(',');
		let Case_07_Res = 'Case_07_Res: ' + cps(exp.Case_07, Case_07_Act);
		log(Case_07_Res);
		await page.waitFor(3000);

		// Case_08
		const Case_08 = 'Case_08: Check Template_GA_Overview_Use_Add. Capture [dd_ui_Template_GA_Overview_Use_Add.jp]. Excepted: ' + exp.Case_08;
		log(Case_08);
		// 点击 Use the Template
		await page.waitForSelector('.pt-main__content > div.glyd > div.glyd__header > button');
		const Template_Use_Template = await page.$('.pt-main__content > div.glyd > div.glyd__header > button');
		await Template_Use_Template.click();
		await page.waitFor(3000);
		// 检查存在 Connect with Google Analytics 按钮
		await page.waitForSelector('.pt-main__content > div.dashboard > div.dashboard-auth > div > ul > li');
		let Case_08_Act = await page.$eval('.pt-main__content > div.dashboard > div.dashboard-auth > div > ul > li > span', el => el.innerText);
		let Case_08_Res = 'Case_08_Res: ' + cps(exp.Case_08, Case_08_Act);
		log(Case_08_Res);
		await page.screenshot({
			path: './pic/dd_ui_Template_GA_Overview_Use_Add.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize_1.height
			}
		});

		// Case_09
		const Case_09 = 'Case_09: Check Conn_DS_GA window. Excepted: ' + exp.Case_09;
		log(Case_09);
		// 点击 Connect with Google Analytics 按钮
		await page.waitForSelector('.pt-main__content > div.dashboard > div.dashboard-auth > div > ul > li');
		const Connect_GA_Button = await page.$('.pt-main__content > div.dashboard > div.dashboard-auth > div > ul > li');
		await Connect_GA_Button.click();
		await page.waitFor(3000);
		// 检查 Connect DS 弹框标题
		await page.waitForSelector('.datasource-connection > div > div > div.pt-popupv2__content.datasource-connection__container > header > h3 > span');
		let Case_09_Act = await page.$eval('.datasource-connection > div > div > div.pt-popupv2__content.datasource-connection__container > header > h3 > span', el => el.innerText);
		let Case_09_Res = 'Case_09_Res: ' + cps(exp.Case_09, Case_09_Act);
		log(Case_09_Res);

		// Case_10
		const Case_10 = 'Case_10: Check Template_Panel_Batch_Authorize.';
		log(Case_10);
		const Widget_Select_Account = await page.$('.pt-popupv2__main > div.datasource-connection__from > div:nth-child(2) > div > div > div');
		await Widget_Select_Account.click();
		await page.waitFor(5000);
		await page.waitForSelector('.datasource-connection__from > div:nth-child(2) > div > div.pt-dropdown-vnew__dropdown > div > div.pt-dropdown-vnew__dropdown-wrap-body > div > div > div > div.pt-list__wrap > div');
		const Widget_Select_Account_GA = await page.$('.datasource-connection__from > div:nth-child(2) > div > div.pt-dropdown-vnew__dropdown > div > div.pt-dropdown-vnew__dropdown-wrap-body > div > div > div > div.pt-list__wrap > div');
		await Widget_Select_Account_GA.click();
		await page.waitFor(5000);
		await page.waitForSelector('.pt-popupv2__main > div.datasource-connection__from > div.datasource-connection__from-item.no-add > div > div > div');
		const Widget_Select_Profile_GA = await page.$('.pt-popupv2__main > div.datasource-connection__from > div.datasource-connection__from-item.no-add > div > div > div');
		await Widget_Select_Profile_GA.click();
		await page.waitFor(5000);
		await page.waitForSelector('.datasource-connection__from > div.datasource-connection__from-item.no-add > div > div.pt-dropdown-vnew__dropdown > div > div.search.has-prefix.pt-input.pt-input--default.pt-input_border > input');
		await page.waitFor(5000);
		const searchInput = await page.$('.datasource-connection__from > div.datasource-connection__from-item.no-add > div > div.pt-dropdown-vnew__dropdown > div > div.search.has-prefix.pt-input.pt-input--default.pt-input_border > input');
		await searchInput.focus();
		await searchInput.type('Raw data', {delay: 20});
		await page.waitFor(3000);
		await page.waitForSelector('.datasource-connection__from > div.datasource-connection__from-item.no-add > div > div.pt-dropdown-vnew__dropdown > div > div.pt-dropdown-vnew__dropdown-wrap-body > div > div > ul:nth-child(1) > li > ul > li > ul > li:nth-child(1) > span');
		const Widget_Select_Profile_GA_Rawdata = await page.$('.datasource-connection__from > div.datasource-connection__from-item.no-add > div > div.pt-dropdown-vnew__dropdown > div > div.pt-dropdown-vnew__dropdown-wrap-body > div > div > ul:nth-child(1) > li > ul > li > ul > li:nth-child(1) > span');
		await Widget_Select_Profile_GA_Rawdata.click();
		await page.waitFor(2000);
		const Widget_Select_DS_Confirm = await page.$('.datasource-connection > div > div > div.pt-popupv2__content.datasource-connection__container > footer > button');
		await Widget_Select_DS_Confirm.click();
		await page.waitFor(10000);
		await page.waitForSelector('.pt-widget__header > div.widget__header-flex-wrap.pt-tooltip > div > span');

		// Case_11
		const Case_11 = 'Case_11: Check Back_Dashboards_All_Sheet. Excepted: ' + exp.Case_11;
		log(Case_11);
		await page.waitForSelector('.pt-main__header > div.pt-main__header-packup > a > span');
		const Panel_Back = await page.$('.pt-main__header > div.pt-main__header-packup > a > span');
		await Panel_Back.click();
		await page.waitFor(2000);
		await page.waitForSelector('.panel-tree > div > div.panel-tree__inner.can_drop > div > div > div:nth-child(2) > a > div.node-name.folder-icon > div.name > span');
		let Case_11_Act = await page.$eval('.panel-tree > div > div.panel-tree__inner.can_drop > div > div > div:nth-child(2) > a > div.node-name.folder-icon > div.name > span', el => el.innerText);
		let Case_11_Res = 'Case_11_Res: ' + cps(exp.Case_11, Case_11_Act);
		log(Case_11_Res);

		// Case_12
		const Case_12 = 'Case_12: Check Delete_New_Panel. Capture [dd_ui_Delete_Dashboard_Confirm.jp]. Excepted: ' + exp.Case_12;
		log(Case_12);
		// 选择新添加的面板，点击更多icon
		await page.waitForSelector('.panel-tree > div > div.panel-tree__inner.can_drop > div > div > div:nth-child(2) > a > div.tools > div');
		const Panel_More = await page.$('.panel-tree > div > div.panel-tree__inner.can_drop > div > div > div:nth-child(2) > a > div.tools > div');
		await Panel_More.click();
		await page.waitFor(1000);
		// 点击 Delete dashboard
		await page.waitForSelector('.pt-main__content > div:nth-child(1) > div > div.dashboardlist-wrap > div.pt-menu__content > div > div > div.pt-panel__tools > a:nth-child(5)');
		const Delete_Dashboard = await page.$('.pt-main__content > div:nth-child(1) > div > div.dashboardlist-wrap > div.pt-menu__content > div > div > div.pt-panel__tools > a:nth-child(5)');
		await Delete_Dashboard.click();
		await page.waitFor(1000);
		// 检查删除确认提示
		await page.waitForSelector('.pt-menu__content > div > div.pt-popupv2.short-popup > div > div.pt-popupv2__content.is-middle > div.pt-popupv2__main > div');
		let Case_12_Act = await page.$eval('.pt-menu__content > div > div.pt-popupv2.short-popup > div > div.pt-popupv2__content.is-middle > div.pt-popupv2__main > div', el => el.innerText);
		let Case_12_Res = 'Case_12_Res: ' + cps(exp.Case_12, Case_12_Act);
		log(Case_12_Res);
		await page.screenshot({
			path: './pic/dd_ui_Delete_Dashboard_Confirm.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize_1.height
			}
		});
		// 在删除确认弹框，点击 Delete 按钮
		await page.waitForSelector('.pt-menu__content > div > div.pt-popupv2.short-popup > div > div.pt-popupv2__content.is-middle > footer > button');
		const Delete_Dashboard_Confirm = await page.$('.pt-menu__content > div > div.pt-popupv2.short-popup > div > div.pt-popupv2__content.is-middle > footer > button');
		await Delete_Dashboard_Confirm.click();
		await page.waitFor(5000);

		// log
		const log_server_1 = 'log_server_1: 【AT_DD_Online_UI_TemplateGallery】 runs Finished.';
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
			+ Case_09 + '\r\n'
			+ Case_09_Res + '\r\n'
			+ Case_10 + '\r\n'
			+ Case_11 + '\r\n'
			+ Case_11_Res + '\r\n'
			+ Case_12 + '\r\n'
			+ Case_12_Res + '\r\n'
			+ log_server_1 + '\r\n', 'UTF8');
		writerStream.end();

	} catch (e) {
		if (e instanceof TimeoutError) {
			console.error(e);
			const log_block = 'Log_Block: Service unexpected termination! 【AT_DD_Online_UI_TemplateGallery】 runs Error!';
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




