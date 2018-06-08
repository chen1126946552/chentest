package com.listener;

//import org.apache.log4j.Logger;
import org.testng.IRetryAnalyzer;
import org.testng.ITestResult;
import org.testng.Reporter;


/**
 * Created by yaowang on 2017/5/10.
 */
public class OverrideIReTry implements IRetryAnalyzer {
//        public static Logger logger = Logger.getLogger(OverrideIReTry.class);
    public  int initReTryNum = 1;
    public  int maxReTryNum = 2;
//    private static ThreadLocal pagegroup = new ThreadLocal();

    @Override
    public boolean retry(ITestResult iTestResult) {
        if (initReTryNum < maxReTryNum) {
            String message = "用例 <" + iTestResult.getName() + ">运行失败，第" + initReTryNum + "次重试";
//            logger.info(message);
            System.out.println(message);
//            System.out.println(String.format("%s.%s", iTestResult.getMethod().getRealClass().toString(), iTestResult.getMethod().getMethodName()));
            Reporter.setCurrentTestResult(iTestResult);
            Reporter.log(message);
//            ((ExtentTest.java)pagegroup.get()).info(message);
            initReTryNum++;
            return true;
        }
        return false;
    }

}




