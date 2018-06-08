package com.ptengine.check;

import com.ptengine.pagemethod.HeatmapMethod;
import org.testng.Assert;

public class HeatmapCheck extends HeatmapMethod {

    public void checkClicknum(){
        int clicknum=getClicknum();
        if (clicknum>500){
            Assert.fail("点击数超出预期，数量为："+clicknum);
        }
        if (clicknum<460){
            Assert.fail("点击数低于预期，数量为："+clicknum);
        }
    }

    public void checkPVnum(){
        int pvnum=getPVnum();
        if (pvnum>140){
            Assert.fail("PV超出预期，数量为："+pvnum);
        }
        if (pvnum<100){
            Assert.fail("PV低于预期，数量为："+pvnum);
        }
    }

    public void checkVInum(){
        int VInum=getVInum();
        if (VInum>140){
            Assert.fail("VI超出预期，数量为："+VInum);
        }
        if (VInum<100){
            Assert.fail("VI低于预期，数量为："+VInum);
        }
    }
}
