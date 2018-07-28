package com.listener;

import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.reporter.ExtentHtmlReporter;
import com.aventstack.extentreports.reporter.ExtentXReporter;
import com.aventstack.extentreports.reporter.configuration.ChartLocation;
import com.aventstack.extentreports.reporter.configuration.Theme;
import org.testng.Reporter;

import java.io.File;

/**
 * Created by ptmind on 2017/4/27.
 */
public class ExtentManager {
    private static ExtentReports extent;

    public static ExtentReports getInstance(String filePath,ExtentXReporter extentx) {
        File reportDir= new File("test-output");
        if(!reportDir.exists()&& !reportDir .isDirectory()){
            reportDir.mkdir();
        }
        if (extent == null)
            createInstance(filePath,extentx);
        return extent;
    }


    public static void createInstance(String filePath,ExtentXReporter extentx) {
        extent = new ExtentReports();

//        extent.attachReporter(createHtmlReporter(filePath));
        extent.attachReporter(createExtentXReporter(extentx));


    }

    public static ExtentHtmlReporter createHtmlReporter(String filePath) {
        ExtentHtmlReporter htmlReporter = new ExtentHtmlReporter(filePath);
        //报表位置
        htmlReporter.config().setTestViewChartLocation(ChartLocation.TOP);
        //使报表上的图表可见
        htmlReporter.config().setChartVisibilityOnOpen(true);
//        设置报表 样式
        htmlReporter.setTestRunnerLogs(Reporter.getOutput());
        htmlReporter.config().setTheme(Theme.STANDARD);
        htmlReporter.config().setDocumentTitle(filePath);
        htmlReporter.config().setEncoding("UTF-8");
        htmlReporter.config().setCSS(".node.level-1  ul{ display:none;} .node.level-1.active ul{display:block;}");
        htmlReporter.config().setFilePath(filePath);
        htmlReporter.config().setLevel();

        htmlReporter.config().setReportName("API测试结果jhgjhgjh");
        return htmlReporter;
    }

    public static ExtentXReporter createExtentXReporter(ExtentXReporter extentx) {
//        ExtentXReporter extentx = new ExtentXReporter("localhost", 27017);
//        extentx.getTestRunnerLogs();
        extent.setSystemInfo("OS_platform", "centos");
//        extent.setTestRunnerOutput(extentx.getTestRunnerLogs());
//        extent.setSystemInfo("browser_platform","firefox_46");
//        extent.setSystemInfo("browser_platform","chrome_59");
        extentx.config().setProjectName("Ptegnine_数据验证UI部分");
        extentx.config().setReportName("Build-0.02");
        extentx.config().setServerUrl("http://localhost:1337");
        return extentx;
    }
}