package com.listener;

import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.ExtentTest;
import com.aventstack.extentreports.reporter.ExtentXReporter;

import com.driver.Driver;
import org.testng.*;
import org.testng.annotations.ITestAnnotation;

import java.io.File;
import java.lang.reflect.Constructor;
import java.lang.reflect.Method;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;


/**
 * Created by ptmind on 2017/4/27.
 */
public class ExtentTestNGITestListener implements ITestListener,IAnnotationTransformer{
    private Date date=new Date();
    DateFormat format=new SimpleDateFormat("yyyy-MM-dd_HH_mm_ss");
    private String time=format.format(date);

    ExtentXReporter extentx = new ExtentXReporter("localhost", 27017);
    public ExtentReports extent = ExtentManager.getInstance("test-output/extent"+time+".html",extentx);
    public  ThreadLocal<ExtentTest> parentTest = new ThreadLocal<ExtentTest>();
    public  static ThreadLocal<ExtentTest> test = new ThreadLocal<ExtentTest>();

//    ExtentTest.java feature;
//    ExtentTest.java scenario ;
      ExtentTest child;

      SlackAttachmentBuild sab=new SlackAttachmentBuild();




    @Override
    public synchronized void onStart(ITestContext context) {
//        System.out.println(context.getSuite().getName()); ptengine-UI
//        System.out.println(context.getName());
//        parentTest=extent.createTest(context.getName());
//        ExtentTest parent = extent.createTest(context.getName());
        ExtentTest parent = extent.createTest(context.getSuite().getName());
        parentTest.set(parent);

    }

    @Override
    public synchronized void onFinish(ITestContext context) {
        extent.flush();

//        String server=extentx.config().getServerUrl();
        Object reportid=extentx.getReportId();
//        String url=server+"/#/report?id="+reportid;
//        System.out.println("+++++++++++++++++++++++++++++++++++++++");
//        System.out.println(url);
        int i=context.getFailedTests().size();

        if (i>0){
            SlackMessageSend sms=new SlackMessageSend();
            try {
                sms.sendWithAttachment("https://hooks.slack.com/services/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 ", "<!channel|channel> \n"+time+" ptengine前端数据检查", sab.newAttachment("测试报告详情参考：",  "https://ui.yaowang.ptmind.com/#/report?id="+reportid));
////                sms.sendWithAttachment("https://hooks.slack.com/services/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", time+" ptengine接口测试失败2", sab.newAttachment("测试报告详情参考2：", "http://localhost:1337/#/report?id="+reportid));
            }catch (Exception e){
                System.out.println("-------------------"+e);
            }
        }

    }




    @Override
    public synchronized void onTestStart(ITestResult result){

//        child = ((ExtentTest)parentTest.get()).createNode(result.getMethod().getMethodName());
        child = ((ExtentTest)parentTest.get()).createNode(result.getMethod().getDescription());
        test.set(child);
        ((ExtentTest)test.get()).info(result.getMethod().getMethodName()+" begin");
    }


    @Override
    public synchronized void onTestSuccess(ITestResult result) {
        ((ExtentTest)test.get()).pass("Test passed");
    }

    @Override
    public synchronized void onTestFailure(ITestResult result) {
        ((ExtentTest)test.get()).fail(result.getThrowable());
        File directory = new File("test-output");
        try {
            String screenPath = directory.getCanonicalPath() + "/";
            File file = new File(screenPath);
            if (!file.exists()){
                file.mkdirs();
            }
            takeScreenShot(result);
            ((ExtentTest)test.get()).addScreenCaptureFromPath("test-output/" + result.getTestClass().getName() + result.getMethod().getMethodName() + ".png");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void takeScreenShot(ITestResult tr) {
        Driver baseTestcase = (Driver)tr.getInstance();

        /**
         *  截图名称需要为 当前 case所在的java文件名+对应的 case（method）名称，在生成报告时，不同的driver线程，插入对应的图片
         */
//
        baseTestcase.takescreen(tr.getInstanceName() + tr.getName());

//        baseTestcase.takescreen(tr.getInstanceName() + tr.getName());
    }
    @Override
    public synchronized void onTestSkipped(ITestResult result) {
        ((ExtentTest)test.get()).skip(result.getThrowable());
//        File directory = new File("test-output");
//        try {
//            String screenPath = directory.getCanonicalPath() + "/";
//            File file = new File(screenPath);
//            if (!file.exists()){
//                file.mkdirs();
//            }
////
//            takeScreenShot(result);
////
//            ((ExtentTest)test.get()).addScreenCaptureFromPath("test-output/" + result.getTestClass().getName() + result.getMethod().getMethodName() + ".png");
//        } catch (Exception e) {
//            e.printStackTrace();
//        }
    }

    @Override
    public synchronized void onTestFailedButWithinSuccessPercentage(ITestResult result) {
    }

    public ExtentTest getlog(){
        return test.get();
    }


    @Override
    public void transform (ITestAnnotation iTestAnnotation, Class aClass, Constructor constructor, Method method) {
        IRetryAnalyzer iRetryAnalyzer= iTestAnnotation.getRetryAnalyzer();
        if(iRetryAnalyzer==null){
            iTestAnnotation.setRetryAnalyzer(OverrideIReTry.class);
        }
    }
}


