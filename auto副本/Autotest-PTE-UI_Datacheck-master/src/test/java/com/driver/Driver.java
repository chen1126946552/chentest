package com.driver;

import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;

import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Parameters;

import java.net.URL;
import java.util.concurrent.TimeUnit;

public class Driver {

    ThreadLocal<WebDriver> ThreadDriver = new ThreadLocal<WebDriver>();
    public WebDriver driver =ThreadDriver.get();

    public void takescreen(String filename) {
        ScreenScr.getScreen((TakesScreenshot) driver, filename);
    }

    @Parameters("browser")
    @BeforeClass
    public void getDriver(String browser) throws Exception {
        if(browser.equalsIgnoreCase("firefox")){
            System.out.println(" Executing on FireFox");
            driver = new FirefoxDriver();
            driver.get("https://reportv3.ptengine.jp/login.html");
            driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
            driver.manage().window().maximize();
            ThreadDriver.set(driver);
        }else if(browser.equalsIgnoreCase("chrome")){
            System.out.println(" Executing on CHROME");
//            //本地测试
//            System.setProperty("webdriver.chrome.driver", "D:\\chromedriver.exe");
//            driver = new ChromeDriver();


            //线上测试
            DesiredCapabilities capability = DesiredCapabilities.chrome();
            capability.setJavascriptEnabled(true);
            driver = new RemoteWebDriver(new URL("http://172.16.100.122:4444/wd/hub"), capability);
            capability.setBrowserName("chrome");
            driver.manage().window().maximize();
            driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
            ThreadDriver.set(driver);
        }else{
            throw new IllegalArgumentException("The Browser Type is Undefined");
        }
    }

    @AfterClass
    public void closeBrowser() {
        driver.close();
        driver.quit();
    }

}
