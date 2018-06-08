package com.ptengine.pagemethod;

import com.ptengine.page.DashboardPage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.interactions.Actions;
import org.testng.Assert;

import java.util.ArrayList;
import java.util.List;

import static org.openqa.selenium.By.className;

public class DashboardMethod extends DashboardPage {

    public int getObaseVI(){
        return Integer.parseInt(obase_vi.getText().replace(",",""));
//        return  Integer.parseInt(driver.findElement(className("qa-obase-vi")).getText());
    }

    public int getObaseUV(){
        return Integer.parseInt(obase_uv.getText().replace(",",""));
    }

    public int getObasePV(){
        return Integer.parseInt(obase_pv.getText().replace(",",""));
    }

    public int getObaseNewvi(){
        return Integer.parseInt(obase_newvi.getText().replace(",",""));
    }

    public int getObaseOldvi(){
        return Integer.parseInt(obase_oldvi.getText().replace(",",""));
    }


    public List<Integer> getList(List<WebElement> list){
        List<Integer> listtmp = new ArrayList<>();
        if (list.size() > 0) {
            for(int i=0;i<list.size();i++){
                if(!(list.get(i).getText().equals(""))){
                    int vitmp=Integer.parseInt(list.get(i).getText().replace(",",""));
                    listtmp.add(vitmp);
                }
            }
        }else{
            return listtmp;
        }
        return listtmp;
    }


    public void clickHeatmap(WebDriver driver){
        Actions action=new Actions(driver);
        action.moveToElement(pv_list_url.get(0)).perform();
        pv_list_heatmapbutton.get(0).click();
    }
}
