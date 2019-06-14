const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({headless:false});
    const page = await browser.newPage();
    //
    await page.goto('http://192.168.2.15:9998');
    await page.setViewport({width:1280,height:800});
    await page.waitForSelector('.pt-ui-button__text');
    await page.type('[name=email]', 'chen.chen@ptmind.com', {delay: 20});
	await page.type('[name=userPassword]', '123123', {delay: 20});
	const authLogin = await page.$('.pt-ui-button');
	await authLogin.click();
	await page.waitFor(3000);
	


	// await datasource = await page.waitForSelector('.pt-main__aside > pt-touch > div > div.linkList > a.item.data-manage')
	// await datasource.click()
	// await page.waitFor(2000)
	// 点击 Manage data
	await page.waitForSelector('.linkList > a.item.data-manage > div');
	const ManageData_Item = await page.$('.linkList > a.item.data-manage > div');
	await ManageData_Item.click();
	await page.waitFor(1000);
	await page.waitForSelector('.connection-list > div.connection-list__header > div');
		
	

	const addDatasource = await page.$('.controlbutton > button')
	await addDatasource.click()
	await page.waitFor(2000)
	

	const addGa = await page.$('#ds-card__googleanalysis')
	await addGa.click()
	

    await page.waitFor(3000);//等待3秒，等待新窗口打开
   
    const page2 = ( await browser.pages() )[2];//得到所有窗口使用列表索引得到新的窗口
    const emailInput = await page2.waitFor('#identifierId');
    await emailInput.type('pttestchen001@gmail.com', {delay: 20});
    const emailNext = await page2.waitFor('#identifierNext');
    await emailNext.click()
    await page2.waitFor(2000)

    const passwordInput = await page2.waitFor('#password');
    await passwordInput.type('1126946552', {delay: 20});
    const passwordNext = await page2.waitFor('#passwordNext');
    await passwordNext.click()
    await page2.waitFor(2000)

    const approveAccess = await page2.waitFor('#submit_approve_access');
    await approveAccess.click()
    await page2.waitFor(2000)

	let text = await page.$eval('.connection-list__col-name > span.connection-list__name', el => el.innerText);  
    console.log(text);

    let text = await page.$eval('.connection-list__col-name > span.connection-list__name', el => el.innerText);  
    console.log(text);
    
})();