
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
	Case_02: 'Auto_panel_GA',   // Auto_panel_GA 面板名
	Case_02_1: 'Auto_widget_GA_H_勿删', // Auto_panel_GA 面板包括 widget名称
	Case_03: 'Date,Device Category,Browser,User Type,Hits,Sessions,User Type,Users,Date,Device Category,Browser,User Type,Hits,Sessions', // Table 表头字段名
	Case_04: '2019-03-10,03-12,03-14,03-16,2019-03-10,03-11,03-12,03-13,03-14,03-15,03-16', // Column X-轴内容
    Case_05: '2019-03-10,03-12,03-14,03-16,2019-03-10,03-11,03-12,03-13,03-14,03-15,03-16',  // Bar X-轴内容
	Case_06: '2019-03-10,03-12,03-14,03-16,2019-03-10,03-11,03-12,03-13,03-14,03-15,03-16',  // StackedColumn X-轴内容
	Case_07: '2019-03-10,03-12,03-14,03-16,2019-03-10,03-11,03-12,03-13,03-14,03-15,03-16',  // StackedBar X-轴内容
	Case_08: '2019-03-10,03-12,03-14,03-16,2019-03-10,03-11,03-12,03-13,03-14,03-15,03-16',  // Line X-轴内容
	Case_09: '2019-03-10,03-12,03-14,03-16,2019-03-10,03-11,03-12,03-13,03-14,03-15,03-16',  // Area X-轴内容
	Case_10: '2019-03-10,03-12,03-14,03-16,2019-03-10,03-11,03-12,03-13,03-14,03-15,03-16',  // GroupedColumn X-轴内容
	Case_11: 'Users,New Users,2019-03-10,2019-03-11,2019-03-12,2019-03-13,2019-03-14,2019-03-15,2019-03-16',  // Donut Date分类值
	Case_12: '3,596\nHits',  // SingleValue
	Case_13: '---\n3,596\nHits',  // Progress Bar
	Case_14: 'Hits',  // Map 总值指标
	Case_15: 'Users,New Users,Hits,Sessions',  // Funnel Metric
	Case_16: '2019-03-10,03-12,03-14,03-16,120,140,160,180,200,220,240,260,280,300,320', //  Bubble Date分类值
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
		const Case_01 = 'Case_01: Login Datadeck with dd_auto_jp216@mailinator.com.';
		log(Case_01);
		await page.goto('https://dashv2.datadeck.com/login');
		await page.waitForSelector('.pt-ui-button__text');
		const documentSize = await page.evaluate(() => {
			return {
				width: document.documentElement.clientWidth,
				height: document.body.clientHeight,
			}
		});
		await page.type('[name=email]', 'dd_auto_jp216@mailinator.com', {delay: 20});
		await page.type('[name=userPassword]', '123456', {delay: 20});
		const authLogin = await page.$('.pt-ui-button');
		await authLogin.click();
		await page.waitFor(3000);
		await page.waitForSelector('.dashboardlist-wrap > div.pt-menu > div > div > ul');


		// Case_02
		const Case_02 = 'Case_02: Check Auto_panel_GA panel includes widget in Favorites. Excepted: ' + exp.Case_02 + ' widget: ' + exp.Case_02_1;
		log(Case_02);
		await page.waitForSelector('.dashboardlist-wrap > div.pt-menu > div > div > ul > li:nth-child(2)');
		const Favorites_Sheet = await page.$('.dashboardlist-wrap > div.pt-menu > div > div > ul > li:nth-child(2)');
		await Favorites_Sheet.click();
		await page.waitFor(1000);
		await page.waitForSelector('.panel-tree__inner > div > div > div:nth-child(2) > a > div.node-name.folder-icon > div.name > span');
		let Case_02_Act = await page.$eval('.panel-tree__inner > div > div > div:nth-child(2) > a > div.node-name.folder-icon > div.name > span', el => el.innerText);
		let Case_02_Res = 'Case_02_Res: ' + cps(exp.Case_02, Case_02_Act);
		log(Case_02_Res);
		// 进入 Auto_panel_GA 面板
		const Panel_GA = await page.$('.panel-tree__inner > div > div > div:nth-child(2) > a > div.node-name.folder-icon > div.name');
		await Panel_GA.click();
		await page.waitFor(2000);
		await page.waitForSelector('.fg-container > div > div:nth-child(1) > div > div.pt-widget.pt-widget__clear-overflow > div.pt-widget__header > div.widget__header-flex-wrap.pt-tooltip > div > span');
		let Case_02_1_Act = await page.$eval('.fg-container > div > div:nth-child(1) > div > div.pt-widget.pt-widget__clear-overflow > div.pt-widget__header > div.widget__header-flex-wrap.pt-tooltip > div > span', el => el.innerText);
		let Case_02_1_Res = 'Case_02_1_Res: ' + cps(exp.Case_02_1, Case_02_1_Act);
		log(Case_02_1_Res);


		// Case_03
		const Case_03 = 'Case_03: Check Widget_Editor_Table. Capture [dd_ui_Widget_Editor_Table.jpg]. Excepted: ' + exp.Case_03;
		log(Case_03);
		const Widget_More = await page.$('.fg-container > div > div:nth-child(1) > div > div.pt-widget.pt-widget__clear-overflow > div.pt-widget__header > div.widget__tools > a > svg');
		await Widget_More.click();
		await page.waitFor(2000);

		const Widget_More_Edit = await page.$('.fg-container > div > div:nth-child(1) > div > div.pt-widget.pt-widget__clear-overflow > div.pt-widget__header > div.widget__tools > a > div > ul > li:nth-child(1)');
		await Widget_More_Edit.click();
		await page.waitFor(2000);
		await page.waitForSelector('.editor-setting__header > button.active > span');
		await page.waitForSelector('.editor-chart__header > div.editor-chart__total > span.editor-chart__total-label');
		let Table_Character = await page.$$eval('.pt-table__thead__tr-th-content', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
        let Case_03_Act = Table_Character.join(',');
        // log(Case_03_Act);
        let Case_03_Res = 'Case_03_Res: ' + cps(exp.Case_03, Case_03_Act);
        log(Case_03_Res);
		await page.screenshot({
			path: './pic/dd_ui_Widget_Editor_Table.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});


		// Case_04
		const Case_04 = 'Case_04: Check Widget_Editor_Column. Capture [dd_ui_Widget_Editor_Column.jpg]. Excepted: ' + exp.Case_04;
		log(Case_04);
		await page.waitForSelector('.editor__body > div.choose-chart > div > ul > li:nth-child(2) > a');
		const Chart_Column_Group = await page.$('.editor__body > div.choose-chart > div > ul > li:nth-child(2) > a');
		await Chart_Column_Group.click();
		await page.waitFor(2000);
		await page.waitForSelector('.editor__body > div.choose-chart > div.choose-chart__sub-menu > a:nth-child(1)');
		const Chart_Column_Sub_Column = await page.$('.editor__body > div.choose-chart > div.choose-chart__sub-menu > a:nth-child(1)');
		await Chart_Column_Sub_Column.click();
		await page.waitFor(3000);
		await page.waitForSelector('.editor-chart__header > div.editor-chart__total > span.editor-chart__total-label');
		let Column_x_axis = await page.$$eval('.highcharts-axis-labels.highcharts-xaxis-labels > span', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
        let Case_04_Act = Column_x_axis.join(',');
        // log(Case_04_Act);
        let Case_04_Res = 'Case_04_Res: ' + cps(exp.Case_04, Case_04_Act);
        log(Case_04_Res);
		await page.screenshot({
			path: './pic/dd_ui_Widget_Editor_Column.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});


		// Case_05
		const Case_05 = 'Case_05: Check Widget_Editor_Bar. Capture [dd_ui_Widget_Editor_Bar.jpg]. Excepted: ' + exp.Case_05;
		log(Case_05);
		await page.waitForSelector('.editor__body > div.choose-chart > div.choose-chart__sub-menu > a:nth-child(2)');
		const Chart_Column_Sub_Bar = await page.$('.editor__body > div.choose-chart > div.choose-chart__sub-menu > a:nth-child(2)');
		await Chart_Column_Sub_Bar.click();
		await page.waitFor(3000);
		await page.waitForSelector('.editor-chart__header > div.editor-chart__total > span.editor-chart__total-label');
		let Bar_x_axis = await page.$$eval('.highcharts-axis-labels.highcharts-xaxis-labels > span', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
        let Case_05_Act = Bar_x_axis.join(',');
        // log(Case_05_Act);
        let Case_05_Res = 'Case_05_Res: ' + cps(exp.Case_05, Case_05_Act);
        log(Case_05_Res);
		await page.screenshot({
			path: './pic/dd_ui_Widget_Editor_Bar.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});


		// Case_06
		const Case_06 = 'Case_06: Check Widget_Editor_StackedColumn. Capture [dd_ui_Widget_Editor_StackedColumn.jpg]. Excepted: ' + exp.Case_06;
		log(Case_06);
		await page.waitForSelector('.editor__body > div.choose-chart > div.choose-chart__sub-menu > a:nth-child(3)');
		const Chart_Column_Sub_StackedColumn = await page.$('.editor__body > div.choose-chart > div.choose-chart__sub-menu > a:nth-child(3)');
		await Chart_Column_Sub_StackedColumn.click();
		await page.waitFor(3000);
		await page.waitForSelector('.editor-chart__header > div.editor-chart__total > span.editor-chart__total-label');
		let StackedColumn_x_axis = await page.$$eval('.highcharts-axis-labels.highcharts-xaxis-labels > span', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
        let Case_06_Act = StackedColumn_x_axis.join(',');
        // log(Case_06_Act);
        let Case_06_Res = 'Case_06_Res: ' + cps(exp.Case_06, Case_06_Act);
        log(Case_06_Res);
		await page.screenshot({
			path: './pic/dd_ui_Widget_Editor_StackedColumn.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});


		// Case_07
		const Case_07 = 'Case_07: Check Widget_Editor_StackedBar. Capture [dd_ui_Widget_Editor_StackedBar.jpg]. Excepted: ' + exp.Case_07;
		log(Case_07);
		await page.waitForSelector('.editor__body > div.choose-chart > div.choose-chart__sub-menu > a:nth-child(4)');
		const Chart_Column_Sub_StackedBar = await page.$('.editor__body > div.choose-chart > div.choose-chart__sub-menu > a:nth-child(4)');
		await Chart_Column_Sub_StackedBar.click();
		await page.waitFor(3000);
		await page.waitForSelector('.editor-chart__header > div.editor-chart__total > span.editor-chart__total-label');
		let StackedBar_x_axis = await page.$$eval('.highcharts-axis-labels.highcharts-xaxis-labels > span', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
        let Case_07_Act = StackedBar_x_axis.join(',');
        // log(Case_07_Act);
        let Case_07_Res = 'Case_07_Res: ' + cps(exp.Case_07, Case_07_Act);
        log(Case_07_Res);
		await page.screenshot({
			path: './pic/dd_ui_Widget_Editor_StackedBar.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});


		// Case_08
		const Case_08 = 'Case_08: Check Widget_Editor_Line. Capture [dd_ui_Widget_Editor_Line.jpg]. Excepted: ' + exp.Case_08;
		log(Case_08);
		await page.waitForSelector('.editor__body > div.choose-chart > div > ul > li:nth-child(3) > a');
		const Chart_Line_Group = await page.$('.editor__body > div.choose-chart > div > ul > li:nth-child(3) > a');
		await Chart_Line_Group.click();
		await page.waitFor(2000);
		await page.waitForSelector('.editor__body > div.choose-chart > div.choose-chart__sub-menu > a:nth-child(1)');
		const Chart_Line_Sub_StackedBar = await page.$('.editor__body > div.choose-chart > div.choose-chart__sub-menu > a:nth-child(1)');
		await Chart_Line_Sub_StackedBar.click();
		await page.waitFor(3000);
		await page.waitForSelector('.editor-chart__header > div.editor-chart__total > span.editor-chart__total-label');
		let Line_x_axis = await page.$$eval('.highcharts-axis-labels.highcharts-xaxis-labels > span', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
        let Case_08_Act = Line_x_axis.join(',');
        // log(Case_08_Act);
        let Case_08_Res = 'Case_08_Res: ' + cps(exp.Case_08, Case_08_Act);
        log(Case_08_Res);
		await page.screenshot({
			path: './pic/dd_ui_Widget_Editor_Line.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});


		// Case_09
		const Case_09 = 'Case_09: Check Widget_Editor_Area. Capture [dd_ui_Widget_Editor_Line.jpg]. Excepted: ' + exp.Case_09;
		log(Case_09);
		await page.waitForSelector('.editor__body > div.choose-chart > div.choose-chart__sub-menu > a:nth-child(2)');
		const Chart_Line_Sub_Area = await page.$('.editor__body > div.choose-chart > div.choose-chart__sub-menu > a:nth-child(2)');
		await Chart_Line_Sub_Area.click();
		await page.waitFor(3000);
		await page.waitForSelector('.editor-chart__header > div.editor-chart__total > span.editor-chart__total-label');
		let Area_x_axis = await page.$$eval('.highcharts-axis-labels.highcharts-xaxis-labels > span', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
        let Case_09_Act = Area_x_axis.join(',');
        // log(Case_09_Act);
        let Case_09_Res = 'Case_09_Res: ' + cps(exp.Case_09, Case_09_Act);
        log(Case_09_Res);
		await page.screenshot({
			path: './pic/dd_ui_Widget_Editor_Area.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});


		// Case_10
		const Case_10 = 'Case_10: Check Widget_Editor_GroupedColumn. Capture [dd_ui_Widget_Editor_GroupedColumn.jpg]. Excepted: ' + exp.Case_10;
		log(Case_10);
		await page.waitForSelector('.editor__body > div.choose-chart > div.scrollbar__holder.ps-container.ps-theme-light.ps > ul > li:nth-child(4) > a');
		const Chart_GroupedColumn = await page.$('.editor__body > div.choose-chart > div.scrollbar__holder.ps-container.ps-theme-light.ps > ul > li:nth-child(4) > a');
		await Chart_GroupedColumn.click();
		await page.waitFor(3000);
		await page.waitForSelector('.editor-chart__header > div.editor-chart__total > span.editor-chart__total-label');
		let GroupedColumn_x_axis = await page.$$eval('.highcharts-axis-labels.highcharts-xaxis-labels > span', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
        let Case_10_Act = GroupedColumn_x_axis.join(',');
        // log(Case_10_Act);
        let Case_10_Res = 'Case_10_Res: ' + cps(exp.Case_10, Case_10_Act);
        log(Case_10_Res);
		await page.screenshot({
			path: './pic/dd_ui_Widget_Editor_GroupedColumn.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});


		// Case_11
		const Case_11 = 'Case_11: Check Widget_Editor_Donut. Capture [dd_ui_Widget_Editor_Donut.jpg]. Excepted: ' + exp.Case_11;
		log(Case_11);
		await page.waitForSelector('.editor__body > div.choose-chart > div.scrollbar__holder.ps-container.ps-theme-light.ps > ul > li:nth-child(5) > a');
		const Chart_Donut = await page.$('.editor__body > div.choose-chart > div.scrollbar__holder.ps-container.ps-theme-light.ps > ul > li:nth-child(5) > a');
		await Chart_Donut.click();
		await page.waitFor(3000);
		await page.waitForSelector('.editor__body > div.editor-graph > div.editor-graph__body > div > div.editor-chart__body > div > div');
		let Donut_Date = await page.$$eval('.highcharts-legend > div > div > div > span > div', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
        let Case_11_Act = Donut_Date.join(',');
        log(Case_11_Act);
        let Case_11_Res = 'Case_11_Res: ' + cps(exp.Case_11, Case_11_Act);
        log(Case_11_Res);
		await page.screenshot({
			path: './pic/dd_ui_Widget_Editor_Donut.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});


		// Case_12
		const Case_12 = 'Case_12: Check Widget_Editor_SingleValue. Capture [dd_ui_Widget_Editor_SingleValue.jpg]. Excepted: ' + exp.Case_12;
		log(Case_12);
		await page.waitForSelector('.editor__body > div.choose-chart > div > ul > li:nth-child(6) > a');
		const Chart_SingleValue = await page.$('.editor__body > div.choose-chart > div > ul > li:nth-child(6) > a');
		await Chart_SingleValue.click();
		await page.waitFor(3000);
		await page.waitForSelector('.editor__body > div.editor-graph > div.editor-graph__body > div > div.editor-chart__body > div > div > div');
		let Case_12_Act = await page.$eval('.editor__body > div.editor-graph > div.editor-graph__body > div > div.editor-chart__body > div > div > div', el => el.innerText);
        log(Case_12_Act);
        let Case_12_Res = 'Case_12_Res: ' + cps(exp.Case_12, Case_12_Act);
        log(Case_12_Res);
		await page.screenshot({
			path: './pic/dd_ui_Widget_Editor_SingleValue.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});


		// Case_13
		const Case_13 = 'Case_13: Check Widget_Editor_ProgressBar. Capture [dd_ui_Widget_Editor_ProgressBar.jpg]. Excepted: ' + exp.Case_13;
		log(Case_13);
		await page.waitForSelector('.editor__body > div.choose-chart > div > ul > li:nth-child(7) > a');
		const Chart_ProgressBar = await page.$('.editor__body > div.choose-chart > div > ul > li:nth-child(7) > a');
		await Chart_ProgressBar.click();
		await page.waitFor(3000);
		await page.waitForSelector('.editor__body > div.editor-graph > div.editor-graph__body > div > div.editor-chart__body > div > div > div');
		let Case_13_Act = await page.$eval('.editor__body > div.editor-graph > div.editor-graph__body > div > div.editor-chart__body > div > div > div', el => el.innerText);
        // log(Case_13_Act);
        let Case_13_Res = 'Case_13_Res: ' + cps(exp.Case_13, Case_13_Act);
        log(Case_13_Res);
		await page.screenshot({
			path: './pic/dd_ui_Widget_Editor_ProgressBar.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});


		// Case_14
		const Case_14 = 'Case_14: Check Widget_Editor_Map. Capture [dd_ui_Widget_Editor_Map.jpg]. Excepted: ' + exp.Case_14;
		log(Case_14);
		await page.waitForSelector('.editor__body > div.choose-chart > div > ul > li:nth-child(8) > a');
		const Chart_Map = await page.$('.editor__body > div.choose-chart > div > ul > li:nth-child(8) > a');
		await Chart_Map.click();
		await page.waitFor(3000);
		await page.waitForSelector('.editor-chart__header > div.editor-chart__total > span.editor-chart__total-label');
		let Case_14_Act = await page.$eval('.editor-chart__header > div.editor-chart__total > span.editor-chart__total-label', el => el.innerText);
        // log(Case_14_Act);
        let Case_14_Res = 'Case_14_Res: ' + cps(exp.Case_14, Case_14_Act);
        log(Case_14_Res);
		await page.screenshot({
			path: './pic/dd_ui_Widget_Editor_Map.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});


		// Case_15
		const Case_15 = 'Case_15: Check Widget_Editor_Funnel. Capture [dd_ui_Widget_Editor_Funnel.jpg]. Excepted: ' + exp.Case_15;
		log(Case_15);
		await page.waitForSelector('.editor__body > div.choose-chart > div > ul > li:nth-child(9) > a');
		const Chart_Funnel = await page.$('.editor__body > div.choose-chart > div > ul > li:nth-child(9) > a');
		await Chart_Funnel.click();
		await page.waitFor(3000);
		await page.waitForSelector('.editor__body > div.editor-graph > div.editor-graph__body > div > div.editor-chart__header > div.editor-chart__total');
		let Funnel_Label = await page.$$eval('.highcharts-legend > div > div > div > span > div', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
        let Case_15_Act = Funnel_Label.join(',');
        // log(Case_15_Act);
        let Case_15_Res = 'Case_15_Res: ' + cps(exp.Case_15, Case_15_Act);
        log(Case_15_Res);
		await page.screenshot({
			path: './pic/dd_ui_Widget_Editor_Funnel.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});


		// Case_16
		const Case_16 = 'Case_16: Check Widget_Editor_Bubble. Capture [dd_ui_Widget_Editor_Bubble.jpg]. Excepted: ' + exp.Case_16;
		log(Case_16);
		await page.waitForSelector('.editor__body > div.choose-chart > div > ul > li:nth-child(10) > a');
		const Chart_Bubble = await page.$('.editor__body > div.choose-chart > div > ul > li:nth-child(10) > a');
		await Chart_Bubble.click();
		await page.waitFor(3000);
		await page.waitForSelector('.editor__body > div.editor-graph > div.editor-graph__body > div > div.editor-chart__header > div.editor-chart__total');
		let Bubble_Label = await page.$$eval('.highcharts-axis-labels.highcharts-xaxis-labels > span', els => {
        	return els.map(v => {
        		return v.innerText;
			})
		});
        let Case_16_Act = Bubble_Label.join(',');
        // log(Case_16_Act);
        let Case_16_Res = 'Case_16_Res: ' + cps(exp.Case_16, Case_16_Act);
        log(Case_16_Res);
		await page.screenshot({
			path: './pic/dd_ui_Widget_Editor_Bubble.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
		});


		await page.waitFor(3000);

		// log
		const log_server_1 = 'log_server_1: 【AT_DD_Online_UI_Widget】 runs Finished.';
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
			+ Case_11_Res + '\r\n'
			+ Case_12 + '\r\n'
			+ Case_12_Res + '\r\n'
			+ Case_13 + '\r\n'
			+ Case_13_Res + '\r\n'
			+ Case_14 + '\r\n'
			+ Case_14_Res + '\r\n'
			+ Case_15 + '\r\n'
			+ Case_15_Res + '\r\n'
			+ Case_16 + '\r\n'
			+ Case_16_Res + '\r\n'
			+ log_server_1 + '\r\n', 'UTF8');
		writerStream.end();

	} catch (e) {
		if (e instanceof TimeoutError) {
			console.error(e);
			const log_block = 'Log_Block: Service unexpected termination! 【AT_DD_Online_UI_Widget】 runs Error!';
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


