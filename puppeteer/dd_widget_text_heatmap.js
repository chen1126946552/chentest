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
	Case_01: 'Auto_widget_text_heatmap',   // 登录后，进入已存在的面板
	Case_02: 'Auto_Text',  // 检查已存在的文本widget、热图widget，并截图
	Case_02_1:'そのKPI、本当に大丈夫ですか? KPI設定とその検証の注意点。 | Ptengine Blog',// 检查已存在的文本widget、热图widget，并截图
	Case_03: 'New_Auto_Text',  // 创建新的文本widget，输入内容，并截图
	Case_04: 'Delete card',  // 删除新的文本widget
	Case_05: '- Ptengine heatmap -',// 检查新建热图弹框，并截图
	Case_05_1: 'New_Auto_Heatmap',//创建新的热图widget，正常展示热图，并截图
	Case_06: 'Delete card',  // 删除新的热图widget
};


(async () => {
	const browser = await puppeteer.launch({
		args: ['--no-sandbox', '--disable-setuid-sandbox'],
		ignoreHTTPSErrors: true,
		devtools: false,
		headless: false,
		defaultViewport: {width:1280, height:800},
		timeout: 30000,
	});
	const log_server_0 = 'Log_server_0: Service start-up.';
	log(log_server_0);

	try {
		const page = await browser.newPage();

		// Case_01
		const Case_01 = 'Case_01: Login Datadeck dd_auto_jp217@mailinator.com and click panel. Excepted: ' + exp.Case_01;
		log(Case_01);
		await page.goto('https://dashv2.datadeck.com/login');
		await page.waitForSelector('.pt-ui-button__text');
		const documentSize = await page.evaluate(() => {
			return {
				width: document.documentElement.clientWidth,
				height: document.body.clientHeight,
			}
		});
		await page.type('[name=email]', 'dd_auto_jp217@mailinator.com', {delay: 20});
		await page.type('[name=userPassword]', '123456', {delay: 20});
		const authLogin = await page.$('.pt-ui-button');
		await authLogin.click();
		await page.waitFor(2000);

		await page.waitForSelector('.dashboardlist-wrap > div.pt-menu__content > div > div > div.panel-tree > div > div.panel-tree__inner.can_drop > div > div > div:nth-child(2) > a');
		const autoPanel = await page.$('.dashboardlist-wrap > div.pt-menu__content > div > div > div.panel-tree > div > div.panel-tree__inner.can_drop > div > div > div:nth-child(2) > a')
		await autoPanel.click()
		await page.waitFor(2000);

		let Case_01_Act = await page.$eval('.pt-main__content > div.dashboard > div.dashboard__header > div.dashboard__header__title > div.dashboard__header__title-title > div > span', el => el.innerText);
		let Case_01_Res = 'Case_01_Res: ' + cps(exp.Case_01, Case_01_Act);
		log(Case_01_Res);
		

		// Case_02
		const Case_02 = 'Case_02: Check Text and Heatmap. Capture [dd_ui_Widget_Text_Heatmap.jpg]. Excepted: ' + exp.Case_02 + ' ' + exp.Case_02_1;
		log(Case_02);

		await page.waitForSelector('.pt-widget.pt-widget__clear-overflow.pt-widget__richtext > div > div > div > div > div.chart-richtext__wrap > div > div.chart-richtext__content > p:nth-child(1)');
		let Case_02_Act = await page.$eval('.pt-widget.pt-widget__clear-overflow.pt-widget__richtext > div > div > div > div > div.chart-richtext__wrap > div > div.chart-richtext__content > p:nth-child(1)', el => el.innerText);
		let Case_02_Res = 'Case_02_Res: ' + cps(exp.Case_02, Case_02_Act);
		log(Case_02_Res);

		await page.waitForSelector('.pt-widget.pt-widget__clear-overflow.pt-widget__heatmap > div.pt-widget__body > div > div > div > div.pt-heatmap__wrap > iframe');
		const frame = await page.frames().find(f => f.name() === 'pt_engine_share');
		await frame.waitForSelector('.pt-heatmap-share > main > div.pt-heatmap.pt-panel.js-heatmap > div > div.pt-heatmap-toolbar.clearfix')

		const childframe = (await frame.childFrames())[0]
		await childframe.waitForSelector('#ptengine-hero')
		await page.waitFor(5000);

		await frame.waitForXPath('html/body/div[2]/main/div[3]/div/div[2]/div/div[3]');
		let Case_02_1_Act = await page.$eval('.pt-widget.pt-widget__clear-overflow.pt-widget__heatmap > div.pt-widget__header > div.widget__header-flex-wrap.pt-tooltip > div > span', el => el.innerText);
		let Case_02_1_Res = 'Case_02_1_Res: ' + cps(exp.Case_02_1, Case_02_1_Act);
		log(Case_02_1_Res);

		await page.screenshot({
			path: './pic/dd_ui_Widget_Text_Heatmap.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		
		// Case_03
		const Case_03 = 'Case_03: Check dd_ui_Widget_Text page. Capture [dd_ui_Widget_Text.jpg]. Excepted: ' + exp.Case_03;
		log(Case_03);
		const Widget_Add = await page.$('.pt-main__container > div.pt-main__content > div.dashboard > div.dashboard__header > div.dashboard__header__tools > div > button');
		await Widget_Add.click();
		await page.waitFor(2000);

		const Text_Create = await page.$('.pt-main__container > div.pt-main__content > div.dashboard > div.dashboard__header > div.dashboard__header__tools > div > div > ul > li:nth-child(2)');
		await Text_Create.click();
		await page.waitFor(2000);

		await page.waitForSelector('#widgetListScrollbar > div.fg-container > div > div.fg-item.fg-item-animate');
		await page.waitFor(2000);
		
		const Text_Edit = await page.$('.fg-container > div > div:nth-child(3) > div > div.pt-widget.pt-widget__clear-overflow.pt-widget__richtext > div > div > div > div > div.chart-richtext__wrap > div');
		await Text_Edit.click({clickCount:2});
		await page.waitFor(2000);

		const Text = await page.$('.fg-container > div > div:nth-child(3) > div > div.pt-widget.pt-widget__clear-overflow.pt-widget__richtext > div > div > div > div > div.chart-richtext__wrap > div');
		await Text.type(exp.Case_03, {delay: 20});
		await page.waitFor(2000);

		const Lost_fouse = await page.$('#widgetListScrollbar')
		await Lost_fouse.click()
		
		let Case_03_Act = await page.$eval('.fg-container > div > div:nth-child(3) > div > div.pt-widget.pt-widget__clear-overflow.pt-widget__richtext > div > div > div > div > div.chart-richtext__wrap > div > div.chart-richtext__content > p', el => el.innerText);
		let Case_03_Res = 'Case_03_Res: ' + cps(exp.Case_03, Case_03_Act);
		log(Case_03_Res);
		
		await page.screenshot({
			path: './pic/dd_ui_Widget_Text.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});


		// Case_04
		const Case_04 = 'Case_04: Delete widget_Text page. Capture [dd_ui_Widget_Text_Delete.jpg]. Excepted: ' + exp.Case_04;
		log(Case_04);

		await page.waitFor(2000);
		await page.waitForSelector('.fg-container > div > div:nth-child(3) > div > div.pt-widget.pt-widget__clear-overflow.pt-widget__richtext > div > div > div > div > div.widget__tools');
		const Text_More = await page.$('.fg-container > div > div:nth-child(3) > div > div.pt-widget.pt-widget__clear-overflow.pt-widget__richtext > div > div > div > div > div.widget__tools');
		await Text_More.click();
		await page.waitFor(2000);	

		await page.waitForSelector('.fg-container > div > div:nth-child(3) > div > div.pt-widget.pt-widget__clear-overflow.pt-widget__richtext > div > div > div > div > div.widget__tools > a > div > ul > li:nth-child(7)');
		const Text_Delete = await page.$('.fg-container > div > div:nth-child(3) > div > div.pt-widget.pt-widget__clear-overflow.pt-widget__richtext > div > div > div > div > div.widget__tools > a > div > ul > li:nth-child(7)');
		await Text_Delete.click();
		await page.waitFor(2000);

		await page.waitForSelector('.pt-popupv2__content.is-middle > footer > button');
		let Case_04_Act = await page.$eval('.pt-popupv2__content.is-middle > header > h3 > span', el => el.innerText);
		let Case_04_Res = 'Case_04_Res: ' + cps(exp.Case_04, Case_04_Act);
		log(Case_04_Res);
		const Text_Delete_Remove = await page.$('.pt-popupv2__content.is-middle > footer > button');
		await Text_Delete_Remove.click();
		await page.waitFor(1000);
		

		
		// Case_05
		const Case_05 = 'Case_05: Check dd_ui_Widget_Heatmap. Capture [dd_ui_Widget_Heatmap.jpg]. Excepted: ' + exp.Case_05 + ' ' + exp.Case_05_1;
		log(Case_05);

		const Widget_Add_2 = await page.$('.pt-main__container > div.pt-main__content > div.dashboard > div.dashboard__header > div.dashboard__header__tools > div > button');
		await Widget_Add_2.click();
		await page.waitFor(2000);

		const Heatmap_Create = await page.$('.pt-main__container > div.pt-main__content > div.dashboard > div.dashboard__header > div.dashboard__header__tools > div > div > ul > li:nth-child(3)')
		await Heatmap_Create.click();
		await page.waitForSelector('.pt-main__container > div.pt-main__content > div.dashboard > div.pt-popup > div.pt-popup__content');
		await page.waitFor(2000);

		let Case_05_Act = await page.$eval('.pt-main__container > div.pt-main__content > div.dashboard > div.pt-popup > div.pt-popup__content > header > h3 > span', el => el.innerText);
		let Case_05_Res = 'Case_05_Res: ' + cps(exp.Case_05, Case_05_Act);
		log(Case_05_Res);
		await page.screenshot({
			path: './pic/dd_ui_Widget_Heatmap_popup.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// 输入title
		page.waitForSelector('.pt-main__container > div.pt-main__content > div.dashboard > div.pt-popup > div.pt-popup__content > div > div > div.has-content.pt-input.pt-input--default.pt-input_border > input');
		const Heatmap_title_input = await page.$('.pt-main__container > div.pt-main__content > div.dashboard > div.pt-popup > div.pt-popup__content > div > div > div.has-content.pt-input.pt-input--default.pt-input_border > input');
		await Heatmap_title_input.focus();
		await page.$eval(".pt-main__container > div.pt-main__content > div.dashboard > div.pt-popup > div.pt-popup__content > div > div > div.pt-input.pt-input--default.focus.pt-input_border > input", (selector) => {selector.value = "";});
		await Heatmap_title_input.type(exp.Case_05_1, {delay: 20});

		// 输入热图url
		page.waitForSelector('.pt-main__content > div.dashboard > div.pt-popup > div.pt-popup__content > div > div > div.heatmap-editor__content > div > div > div');
		const Heatmap_input = await page.$('.pt-main__content > div.dashboard > div.pt-popup > div.pt-popup__content > div > div > div.heatmap-editor__content > div > div > div');
		await Heatmap_input.click();
		await Heatmap_input.type('http://reportv3.ptengine.jp/heatmap_share.html#ptengine=e9659986af8d1d21b737da9eadcaf361', {delay: 20});

		const Heatmap_save = await page.$('.pt-main__content > div.dashboard > div.pt-popup > div.pt-popup__content > footer > button.pt-ui-button.pt-btn_right.pt-ui-button--primary.pt-ui-button--type-default.pt-ui-button--size-big');
		await Heatmap_save.click();
		await page.waitFor(20000);

		let Case_05_1_Act = await page.$eval('.fg-container > div > div:nth-child(3) > div > div.pt-widget.pt-widget__clear-overflow.pt-widget__heatmap > div.pt-widget__header > div.widget__header-flex-wrap.pt-tooltip > div > span', el => el.innerText);
		let Case_05_1_Res = 'Case_05_1_Res: ' + cps(exp.Case_05_1, Case_05_1_Act);
		log(Case_05_1_Res);

		await page.screenshot({
			path: './pic/dd_ui_Widget_Heatmap.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_06
		const Case_06 = 'Case_06: Delete Heatmap Widget. Excepted: ' + exp.Case_06;
		log(Case_06);

		await page.waitForSelector('.fg-container > div > div:nth-child(3) > div > div.pt-widget.pt-widget__clear-overflow.pt-widget__heatmap > div.pt-widget__header > div.widget__tools');
		const Heatmap_More = await page.$('.fg-container > div > div:nth-child(3) > div > div.pt-widget.pt-widget__clear-overflow.pt-widget__heatmap > div.pt-widget__header > div.widget__tools');
		await Heatmap_More.click();
		await page.waitFor(1000);

		await page.waitForSelector('.fg-container > div > div:nth-child(3) > div > div.pt-widget.pt-widget__clear-overflow.pt-widget__heatmap > div.pt-widget__header > div.widget__tools > a > div > ul > li:nth-child(8)');
		const Heatmap_Delete = await page.$('.fg-container > div > div:nth-child(3) > div > div.pt-widget.pt-widget__clear-overflow.pt-widget__heatmap > div.pt-widget__header > div.widget__tools > a > div > ul > li:nth-child(8)');
		await Heatmap_Delete.click();
		await page.waitFor(1000);
		await page.waitForSelector('.pt-popupv2__content.is-middle > footer > button');

		let Case_06_Act = await page.$eval('.pt-popupv2__content.is-middle > header > h3 > span', el => el.innerText);
		let Case_06_Res = 'Case_06_Res: ' + cps(exp.Case_06, Case_06_Act);
		log(Case_06_Res);
		const Heatmap_Delete_Remove = await page.$('.pt-popupv2__content.is-middle > footer > button');
		await Heatmap_Delete_Remove.click();
		await page.waitFor(1000);
		

		// log
		const log_server_1 = 'log_server_1: 【AT_DD_Online_UI_Widget_Text_Heatmap】 runs Finished.';
		log(log_server_1);

		let writerStream = fs.createWriteStream('./log/dd_ui_log.txt');
		writerStream.write(log_server_0 + '\r\n'
			+ Case_01 + '\r\n'
			+ Case_01_Res + '\r\n'
			+ Case_02 + '\r\n'
			+ Case_02_Res + '\r\n'
			+ Case_02 + '\r\n'
			+ Case_02_1_Res + '\r\n'
			+ Case_03 + '\r\n'
			+ Case_03_Res + '\r\n'
			+ Case_04 + '\r\n'
			+ Case_04_Res + '\r\n'
			+ Case_05 + '\r\n'
			+ Case_05_Res + '\r\n'
			+ Case_05 + '\r\n'
			+ Case_05_1_Res + '\r\n'
			+ Case_06 + '\r\n'
			+ Case_06_Res + '\r\n'
			+ log_server_1 + '\r\n', 'UTF8');
		writerStream.end();

	} catch (e) {
		if (e instanceof TimeoutError) {
			console.error(e);
			const log_block = 'Log_Block: Service unexpected termination! 【AT_DD_Online_UI_Widget_Text_Heatmap】 runs Error!';
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




