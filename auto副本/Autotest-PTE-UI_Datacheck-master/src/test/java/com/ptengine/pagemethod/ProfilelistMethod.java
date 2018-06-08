package com.ptengine.pagemethod;

import com.ptengine.page.ProfilelistPage;

public class ProfilelistMethod extends ProfilelistPage {

    boolean flag=false;

//        点击增加档案按钮
    public void addProfile() {

       button_addprofile.click();
    }


    public void clickFirstProfile() throws Exception{
        profillist.click();
        waitpageloading();
    }

    public void searchProfile(String profilename)throws Exception{
        inputbox_search.sendKeys(profilename);
        button_search.click();
    }





}
