from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chrome_options = Options()

# 禁止弹窗
prefs = {
        'profile.default_content_setting_values':
            {
                'notifications': 2
            }
    }
# 禁止弹窗加入
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get('https://www.1688.com/')
# 就可以访问无通知弹窗的浏览器了



((RemoteWebDriver) driver).executeScript(
				"window.getJSON=$.getJSON;$.getJSON=function(){ window.funObj=arguments[2]; var myFun=function(data){  window.myData=data;} ; window.getJSON(arguments[0],arguments[1],myFun) }");
		driver.findElement(By.id("submit")).click();
		try {
			WebDriverWait wait = new WebDriverWait(driver, 10);
			@SuppressWarnings("unchecked")
			Map<String, ?> data = (Map<String, ?>) wait.until(new Function<WebDriver, Object>() {
				public Object apply(@Nullable WebDriver driver) {
					return ((RemoteWebDriver) driver).executeScript("return window.myData;");
				}
			});
			((RemoteWebDriver) driver)
					.executeScript("window.funObj(window.myData);delete window.myData;$.getJSON=window.getJSON;");
			if (!"0".equals(data.get("code"))) {
				return new Result(Constants.INPUTERROR, data.get("desc"));
			}
			return new Result(Constants.SUCCESS, data.get("desc"));
		} catch (Exception e) {
			e.printStackTrace();
			return new Result(Constants.SYSTEMERROR, Constants.getMessage(Constants.SYSTEMERROR));
		}