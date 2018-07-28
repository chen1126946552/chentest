package com.ptengine.testcase;

import com.ptengine.check.*;
import com.driver.Driver;
import org.openqa.selenium.support.PageFactory;
import org.testng.annotations.Test;

public class TestWithPOM extends Driver {


    @Test(description = "登录系统")
    public void login() throws Exception {
        LoginCheck loginCheck = PageFactory.initElements(driver, LoginCheck.class);
        ProfilelistCheck profilelistCheck = PageFactory.initElements(driver, ProfilelistCheck.class);
//        try {
        loginCheck.openURL(driver,"https://reportv3.ptengine.jp/");
        loginCheck.login("pttest_autodata_jp@mailinator.com", "123456");
        loginCheck.currentURLCheck(driver, "profilelist");
//        profilelistCheck.clickFirstProfile();

//        }catch (Exception e){
//            e.printStackTrace();
//            System.out.println("-------------------------------");
//            System.out.println(e);
//        }
    }


    @Test(description = "进入指定档案",dependsOnMethods = "login")
    public void intoProfile() throws Exception{
        ProfilelistCheck profilelistCheck = PageFactory.initElements(driver, ProfilelistCheck.class);
        profilelistCheck.searchProfile("自动化造数");
        profilelistCheck.clickFirstProfile();
    }

    @Test(description = "dashboard功能",dependsOnMethods ="intoProfile" )
    public void checkDashboard() throws Exception {
//        try {
            DashboardCheck dashboardCheck = PageFactory.initElements(driver, DashboardCheck.class);
            dashboardCheck.openURL(driver, "https://reportv3.ptengine.jp/?uid=1524652626121681&siteid=1524652698028935#/datacenter/overview");
            dashboardCheck.upDate();
            dashboardCheck.obaseDataCheck();
            dashboardCheck.obaseOSviCheck();
            dashboardCheck.obaseBrowserviCheck(140,120);
            dashboardCheck.obasePVListCheck(140,120);
            dashboardCheck.obaseLocationListCheck(140,120);
            dashboardCheck.clickHeatmap(driver);
            dashboardCheck.waitpageloading();
            dashboardCheck.currentURLCheck(driver,"pagescene/heatmap");
//        }catch (Exception e){
//            System.out.println(e);
//        }
    }

    @Test(description = "Heatmap验证",dependsOnMethods = "checkDashboard")
    public void checkHeatmap()throws Exception{
        HeatmapCheck heatmapCheck=PageFactory.initElements(driver,HeatmapCheck.class);
        heatmapCheck.checkClicknum();
        heatmapCheck.checkPVnum();
        heatmapCheck.checkVInum();

    }

}
