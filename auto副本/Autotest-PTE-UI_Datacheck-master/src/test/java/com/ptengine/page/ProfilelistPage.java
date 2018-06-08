package com.ptengine.page;

import com.ptengine.base.BasePage;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.CacheLookup;
import org.openqa.selenium.support.FindBy;

import java.util.List;

public class ProfilelistPage extends BasePage {

    @FindBy(xpath = "//*[@id=\"js-add-profile\"]")
    @CacheLookup
    public WebElement button_addprofile;

    @FindBy(className = "qa-table-body-col-name")
    @CacheLookup
    public List<WebElement> list_profilename;

    @FindBy(className = "qa-table-body-col-name")
    @CacheLookup
    public WebElement profillist;

    @FindBy(xpath = "//*[@id=\"profile\"]/div/div[1]/div/div[1]/div[1]/div/div[2]/span[2]/span[2]")
    @CacheLookup
    public WebElement button_search;

    @FindBy(className = "qa-search-input")
    @CacheLookup
   public WebElement inputbox_search;

    @FindBy(xpath = "//*[@id=\"pt-icon-toolbar-clear\"]/path")
    @CacheLookup
    WebElement icon_cleansearch;

    @FindBy(xpath = "//*[@id=\"profile\"]/div/div[1]/div/div[1]/div[2]/div/div/table/tbody/tr[1]/td[7]/div/a[1]")
    @CacheLookup
    WebElement icon_checkjs;

    @FindBy(xpath = "//*[@id=\"profile\"]/div/div[1]/div/div[1]/div[2]/div/div/table/tbody/tr[1]/td[7]/div/a[2]")
    @CacheLookup
    WebElement icon_setting;

    @FindBy(xpath = "//*[@id=\"profile\"]/div/div[1]/div/div[1]/div[2]/div/div/table/tbody/tr[1]/td[7]/div/a[3]")
    @CacheLookup
    WebElement icon_delete;

    @FindBy(xpath = "//*[@id=\"deletePwdModal\"]/div/div/div/div[1]/div/input")
    @CacheLookup
    WebElement inputbox_password;

    @FindBy(xpath = "//*[@id=\"deletePwdModal\"]/div/div/div/div[2]/button[1]")
    @CacheLookup
    WebElement button_canceldelete;

    @FindBy(xpath = "//*[@id=\"deletePwdModal\"]/div/div/div/div[2]/button[2]")
    @CacheLookup
    WebElement button_submitdelete;


}
