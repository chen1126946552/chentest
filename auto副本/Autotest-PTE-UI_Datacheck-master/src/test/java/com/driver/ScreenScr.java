package com.driver;

/**
 * Created by yaowang on 2017/5/2.
 */



import org.apache.commons.io.FileUtils;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class ScreenScr {
    /**
     * 该类用于截图，在指定结果（目前主要为 fail及skip时，进行截图）
     */
    private SimpleDateFormat format = new SimpleDateFormat("yyyy_MM_dd_HH_mm_ss");
    public  String dateString = format.format(new Date());
    /**
     *  filename的最原始出处，在TestngListener类中baseTestcase.takescreen方法传入的参数
     */
    public static void getScreen(TakesScreenshot driver, String filename){

        String cyrPatn=System.getProperty("user.dir");

        File scrfile=driver.getScreenshotAs(OutputType.FILE);

        try {
            FileUtils.copyFile(scrfile, new File(cyrPatn+"\\test-output\\"+filename+".png"));
//            FileUtils.copyFile(scrfile, new File(cyrPatn+filename+".png"));
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
            System.out.println("GetScreenshot Fail");
        }finally{
            System.out.println("GetScreenshot Successful   "+cyrPatn+"\\test-output\\"+filename+".png");
//            System.out.println("GetScreenshot Successful  "+cyrPatn+filename+".png");
        }

    }

}