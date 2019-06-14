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
	Case_01: 'Connect a data source',   // 登录后，进入DM管理页面
	Case_02: 'peterangel536@gmail.com',  // 授权GA账号，并截图
	Case_03: 'guy.geeraedts@ptengine.com',  // 授权Mailchimp账号，并截图
	Case_04: 'bin.wu@ptengine.com',  // 授权Mailchimp账号，并截图
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
	
	const page = await browser.newPage();

	async function deleteNode(page) {
		const deleteConnection = 'Delete new Connection account';
		log(deleteConnection);

		const datasourceList = await page.$$('.connection-list__col-tool > span > span > span')
		await datasourceList[0].click()
		await page.waitFor(20000)
		log('list click')

		const removebuttone = await page.$('body > ul > li')
		await removebuttone.click()
		log('remove click')
		await page.waitFor(2000);

		const Conn_Delete_Button = await page.$('body > div.pt-confirm-backdrop > div > footer > button.pt-ui-button.pt-ui-button--primary.pt-ui-button--type-default.pt-ui-button--size-big');
		await Conn_Delete_Button.click();
		await page.waitFor(2000);
	}

	try {

		// Case_01
		const Case_01 = 'Case_01: Login Datadeck dd_auto_jp217@mailinator.com and Data Manage. Excepted: ' + exp.Case_01;
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

		await page.waitForSelector('.linkList > a.item.data-manage > div');
		const ManageData_Item = await page.$('.linkList > a.item.data-manage > div');
		await ManageData_Item.click();
		await page.waitFor(1000);

		// 进入DM管理界面
		await page.waitForSelector('.controlbutton > button')
		let Case_01_Act = await page.$eval('.controlbutton > button > span', el => el.innerText);
		let Case_01_Res = 'Case_01_Res: ' + cps(exp.Case_01, Case_01_Act);
		log(Case_01_Res);
		await page.waitFor(1000)

		
		// Case_02
		const Case_02 = 'Case_02: Add new GA account. Capture [dd_ui_Datasource_Add_GA.jpg]. Excepted: ' + exp.Case_02;
		log(Case_02);

		const addDatasourceGA = await page.$('.controlbutton > button')
		await addDatasourceGA.click()
		await page.waitFor(5000)
	
		const addGa = await page.$('#ds-card__googleanalytics-v4')
		await addGa.click()
	

    	await page.waitFor(3000);//等待3秒，等待新窗口打开   
    	const pageGA = ( await browser.pages() )[2];//得到所有窗口使用列表索引得到新的窗口
    	// 输入授权账号email
    	const emailInputGA = await pageGA.waitFor('#identifierId');
    	await emailInputGA.type('peterangel536@gmail.com', {delay: 20});
    	const emailNextGA = await pageGA.waitFor('#identifierNext');
    	await emailNextGA.click()
    	await pageGA.waitFor(2000)

    	// 输入授权账号password
    	const passwordInputGA = await pageGA.waitFor('#password');
    	await passwordInputGA.type('BJZH@data12345678', {delay: 20});
    	const passwordNextGA = await pageGA.waitFor('#passwordNext');
    	await passwordNextGA.click()
    	await pageGA.waitFor(2000)

    	// 点击允许授权
    	const approveAccessGA = await pageGA.waitFor('#submit_approve_access');
    	await approveAccessGA.click()
    	await pageGA.waitFor(2000)

		await page.screenshot({
			path: './pic/dd_ui_Datasource_Add_GA.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});
		
		// Case_03
		const Case_03 = 'Case_03: Add new Mailchimp account. Capture [dd_ui_Datasource_Add_Mailchimp.jpg]. Excepted: ' + exp.Case_03;
		log(Case_03);

		const addDatasourceMailchmip = await page.$('.controlbutton > button')
		await addDatasourceMailchmip.click()
		await page.waitFor(5000)
	
		const addMailchmip = await page.$('#ds-card__mailchimp')
		await addMailchmip.click()
	

    	await page.waitFor(3000);//等待3秒，等待新窗口打开   
    	const pageMailchimp = ( await browser.pages() )[2];//得到所有窗口使用列表索引得到新的窗口
    	// 输入授权账号email
    	const emailInputMailchimp = await pageMailchimp.waitFor('#username');
    	await emailInputMailchimp.type('miapex', {delay: 20});

    	// 输入授权账号password
    	const passwordInputMailchimp = await pageMailchimp.waitFor('#password');
    	await passwordInputMailchimp.type('Ptmind2008!', {delay: 20});

    	const loginMailchimp = await pageMailchimp.waitFor('#login-form > fieldset > div.line > input');
    	await loginMailchimp.click()
    	await pageMailchimp.waitFor(10000)

		await page.screenshot({
			path: './pic/dd_ui_Datasource_Add_Mailchimp.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});

		// Case_4
		const Case_04 = 'Case_04: Add new Facebookpages account. Capture [dd_ui_Datasource_Add_Facebookpages.jpg]. Excepted: ' + exp.Case_04;
		log(Case_04);

		const addDatasourceFacebookpages = await page.$('.controlbutton > button')
		await addDatasourceFacebookpages.click()
		await page.waitFor(5000)
	
		const addFacebookpages = await page.$('#ds-card__facebookpages')
		await addFacebookpages.click()
	

    	await page.waitFor(3000);//等待3秒，等待新窗口打开   
    	const pageFacebookpages = ( await browser.pages() )[2];//得到所有窗口使用列表索引得到新的窗口
    	// 输入授权账号email
    	const emailInputFacebookpages = await pageFacebookpages.waitFor('#email');
    	await emailInputFacebookpages.type('bin.wu@ptengine.com', {delay: 20});

    	// 输入授权账号password
    	const passwordInputFacebookpages = await pageFacebookpages.waitFor('#pass');
    	await passwordInputFacebookpages.type('test/123', {delay: 20});

    	const loginFacebookpages = await pageFacebookpages.waitFor('#loginbutton');
    	await loginFacebookpages.click()
    	await pageFacebookpages.waitFor(10000)

    	// 点击允许授权
    	const approveAccessFacebookpages = await pageFacebookpages.waitFor('#platformDialogForm > div > div > div > div > div > div._6lqs > div._6lqx > div._6-v1 > button:nth-child(2)');
    	await approveAccessFacebookpages.click()
    	await pageFacebookpages.waitFor(2000)

    	const nextFacebookpages = await pageFacebookpages.waitFor('#platformDialogForm > div > div > div > div > div > div._6lqs > div._6lqx > div > div > button');
    	await nextFacebookpages.click()
    	await pageFacebookpages.waitFor(2000)

    	const next2Facebookpages = await pageFacebookpages.waitFor('#platformDialogForm > div > div > div > div > div > div._6lqs > div._6lqx > div > div > button');
    	await next2Facebookpages.click()
    	await pageFacebookpages.waitFor(2000)

    	const finshFacebookpages = await pageFacebookpages.waitFor('#platformDialogForm > div > div > div > div > div > div._6lqs > div._6lqx > div > button');
    	await finshFacebookpages.click()
    	await pageFacebookpages.waitFor(2000)

		await page.screenshot({
			path: './pic/dd_ui_Datasource_Add_Facebookpages.jpg',
			type: 'png',
			clip: {
				x:0, y:0, width:1366, height:documentSize.height
			}
			});
			

		// log
		const log_server_1 = 'log_server_1: 【AT_DD_Online_UI_Vnext_SAAS_Auth】 runs Finished.';
		log(log_server_1);

		let writerStream = fs.createWriteStream('./log/dd_ui_log.txt');
		writerStream.write(log_server_0 + '\r\n'
			+ Case_01 + '\r\n'
			+ Case_01_Res + '\r\n'
			+ Case_02 + '\r\n'
			+ Case_03 + '\r\n'
			+ Case_04 + '\r\n'
			+ log_server_1 + '\r\n', 'UTF8');
		writerStream.end();

	} catch (e) {
		if (e instanceof TimeoutError) {
			console.error(e);
			const log_block = 'Log_Block: Service unexpected termination! 【AT_DD_Online_UI_Vnext_SAAS_Auth】 runs Error!';
			log(log_block);

			let writerStream = fs.createWriteStream('./log/dd_ui_log.txt');
			writerStream.write(log_block, 'UTF8');
			writerStream.end();
		}
	} finally {
		// exit
		await page.close()
		await browser.close();
	}
})();




