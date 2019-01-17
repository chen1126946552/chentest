package com.ptengine.check;

import com.ptengine.pagemethod.DashboardMethod;

import org.testng.Assert;


import java.util.List;

public class DashboardCheck extends DashboardMethod {

    //
//
//
    public void obaseDataCheck() {
        int vi = getObaseVI();
        int uv = getObaseUV();
        int pv = getObasePV();
        int newvi = getObaseNewvi();
        int oldvi = getObaseOldvi();

        if (vi >= 140) {
            Assert.fail("vi超出预期，数量为：" + vi);
        }

        if (vi <= 100) {
            Assert.fail("vi低于预期，数量为：" + vi);
        }

        if(pv>=140){
            Assert.fail("pv超出预期，数量为：" + pv);
        }

        if (pv <= 100) {
            Assert.fail("pv低于预期，数量为：" + pv);
        }

        if (!(pv >= vi) && (vi >= uv)) {
            Assert.fail("pv,uv,vi数据错误");
        }
    }

    public void obaseOSviCheck() {
        List<Integer> obaseOSvi = getList(os_list_vi);
        if (obaseOSvi.size() == 0) {
            Assert.fail("OS列表未获取到");
        }
        if (obaseOSvi.contains(0)) {
            Assert.fail("OS列表中存在0");
        }
        for (int i = 0; i < obaseOSvi.size() - 1; i++) {
            if (obaseOSvi.get(i) < obaseOSvi.get(i + 1)) {
                Assert.fail("OS列表vi排序错误");
            }
        }
    }


    public void obaseBrowserviCheck(int num1,int num2) {
        List<Integer> obaseBrowservi = getList(browser_list_vi);
        if (obaseBrowservi.size() == 0) {
            Assert.fail("浏览器列表未获取到");
        }
        if (obaseBrowservi.contains(0)) {
            Assert.fail("浏览器列表中存在0");
        }
        if(obaseBrowservi.size()==1){
            if(obaseBrowservi.get(0)>num1||obaseBrowservi.get(0)<num2){
                Assert.fail("浏览器列表中vi不在预期内");
            }
        }else {
            for (int i = 0; i < obaseBrowservi.size() - 1; i++) {
                if (obaseBrowservi.get(i) < obaseBrowservi.get(i + 1)) {
                    Assert.fail("URL列表PV排序错误");
                }
            }
        }
    }


    public void obasePVListCheck(int num1,int num2) {
        List<Integer> PVList = getList(pv_list_pv);
        if (PVList.size() == 0) {
            Assert.fail("URL列表未获取到");
        }
        if (PVList.contains(0)) {
            Assert.fail("URL列表中PV存在0");
        }
        if(PVList.size()==1){
            if(PVList.get(0)>num1||PVList.get(0)<num2){
                Assert.fail("URL列表中PV不在预期内");
            }
        }else {
            for (int i = 0; i < PVList.size() - 1; i++) {
                System.out.println(PVList.get(i));
                if (PVList.get(i) < PVList.get(i + 1)) {
                    Assert.fail("URL列表PV排序错误");
                }
            }
        }
    }


    public void obaseLocationListCheck(int num1,int num2) {
        List<Integer> LocationList = getList(location_item_vi);
        if (LocationList.size() == 0) {
            Assert.fail("城市列表未获取到");
        }
        if (LocationList.contains(0)) {
            Assert.fail("城市列表中vi存在0");
        }
        if(LocationList.size()==1){

            if(LocationList.get(0)>num1||LocationList.get(0)<num2){
                Assert.fail("U城市列表中VI不在预期内");
            }
        }else {
            for (int i = 0; i < LocationList.size() - 1; i++) {

                if (LocationList.get(i) < LocationList.get(i + 1)) {
                    Assert.fail("U城市列表中VI排序错误");
                }
            }
        }
    }



}
