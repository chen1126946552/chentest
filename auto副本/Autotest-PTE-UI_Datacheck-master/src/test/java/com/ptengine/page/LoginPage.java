package com.ptengine.page;

import com.ptengine.base.BasePage;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.CacheLookup;
import org.openqa.selenium.support.FindBy;

public class LoginPage extends BasePage {

    @FindBy(name="username")
    @CacheLookup
    public WebElement inputbox_username;

    @FindBy(name="password")
    @CacheLookup
    public WebElement inputbox_password;

    @FindBy(xpath = "//button[@type='button']")
    @CacheLookup
    public  WebElement button_login;


}
