package com.ptengine.pagemethod;

import com.ptengine.page.LoginPage;

public class LoginMethod extends LoginPage {

    public void login(String username,String password) throws Exception{
        inputbox_username.sendKeys(username);
        inputbox_password.sendKeys(password);
        button_login.click();
        waitpageloading();
    }

}
