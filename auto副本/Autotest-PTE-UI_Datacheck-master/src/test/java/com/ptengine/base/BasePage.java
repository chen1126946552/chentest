package com.ptengine.base;

import org.openqa.selenium.*;
import org.openqa.selenium.support.CacheLookup;
import org.openqa.selenium.support.FindBy;
import org.testng.Assert;

import java.text.SimpleDateFormat;
import java.util.Calendar;

public class BasePage {

    @FindBy(xpath = "//*[@id=\"pt-mod-upgrade\"]/div/div/div")
    @CacheLookup
    public WebElement popup_upgrade;

    @FindBy(xpath = "//*[@id=\"pt-mod-upgrade\"]/div/div/div/input[1]")
    @CacheLookup
    public WebElement button_cancelupgrade;

    @FindBy(xpath = "//*[@id=\"pt-mod-upgrade\"]/div/div/div/input[2]")
    @CacheLookup
    WebElement button_upgrade;

    @FindBy(xpath = "//*[@id=\"toolbar_left\"]/div[1]/div[1]")
    @CacheLookup
    WebElement button_date;

    @FindBy(xpath = "//*[@id=\"toolbar_left\"]/div[1]/div[2]/div[1]/ul/li[2]")
    @CacheLookup
    WebElement button_yesterday;

//    @FindBy(xpath = "")


    public void waitpageloading() throws Exception{
//        ExtentTest log=el.getlog();
//        WebDriverWait wait = new WebDriverWait(com.driver, 10);
//        wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("pt-header-logo")));
//        System.out.println(wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("pt-header-logo"))));
//        log.debug("等待页面加载，30秒");
        Thread.sleep(10000);
    }

    public String getCurrentURL(WebDriver driver){
        return driver.getCurrentUrl();
    }


    public void currentURLCheck(WebDriver driver, String value){
        String currentURL=this.getCurrentURL(driver);
        if(!currentURL.endsWith(value)){
            Assert.fail("当前url未以："+value+"结束，可能存在错误");
        }
    }

//    判断升级窗口是否存在
    public void isPopupUpgradePresent(){
        try{
            popup_upgrade.isDisplayed();
        }catch (NoSuchElementException e){
            Assert.fail("未找到升级窗口");
        }
    }


    //    点击取消升级按钮
    public void clickButtonCancelupgrade() throws Exception{
        button_cancelupgrade.click();
        waitpageloading();
    }


    public void openURL(WebDriver driver,String url){
        driver.get(url);
    }


    public void waitpageloading(long value) throws Exception{
//        ExtentTest log=el.getlog();
//        WebDriverWait wait = new WebDriverWait(com.driver, 10);
//        wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("pt-header-logo")));
//        System.out.println(wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("pt-header-logo"))));
//        log.debug("等待页面加载，30秒");
        Thread.sleep(value);
    }

    public void upDate()throws Exception{
        button_date.click();
        button_yesterday.click();
        this.waitpageloading();
    }



}
