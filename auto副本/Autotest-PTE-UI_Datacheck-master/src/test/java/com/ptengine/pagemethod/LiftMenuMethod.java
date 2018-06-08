package com.ptengine.pagemethod;

import com.ptengine.page.LiftMenu;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.interactions.Actions;

public class LiftMenuMethod extends LiftMenu {


    public void menuContentClick() throws Exception{
       menu_Content.click();
        waitpageloading();
    }

    public void menuContentpageClick()throws Exception{
//       Actions action=new Actions(driver);
//        action.moveToElement(menu_Content).perform();
//        Thread.sleep(5000);
////        action.click(menu_Content_page);
////        action.moveToElement(menu_Content_page).click();
////        action.moveToElement(menu_Content_page).perform();
//        System.out.println(menu_Content_page.getText());;
        menu_Content_page.click();
        waitpageloading();
    }

    public void menuContententrypageClick()throws Exception{
//        new Actions(driver).moveToElement(menu_Content).perform();
        menu_Content_entry_page.click();
        waitpageloading();
    }


}
