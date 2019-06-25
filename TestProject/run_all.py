# coding=utf-8
import unittest
import time
from common import HTMLTestRunner
from common import sendMessage
import os

# 这个是优化版执行所有用例并发送报告，分四个步骤
# 第一步加载用例
# 第二步执行用例
# 第三步获取最新测试报告
# 第四步发送消息

# 当前脚本所在文件真实路径
cur_path = os.path.dirname(os.path.realpath(__file__))

def add_case(caseName="cases/login", rule="test*.py"):
    '''第一步：加载测试用例'''
    case_path = os.path.join(cur_path, caseName)  # 用例文件夹
    # 如果不存在这个cases文件夹，就自动创建一个
    if not os.path.exists(case_path): os.mkdir(case_path)
    print("test case path:%s"%case_path)
    # 定义discover方法的参数
    discover = unittest.defaultTestLoader.discover(case_path,
                                                  pattern=rule,
                                                  top_level_dir=None)
    print(discover)
    return discover

def run_case(all_case, reportName="report"):
    '''第二步：执行所有的用例, 并把结果写入HTML测试报告'''
    now = time.strftime("%Y_%m_%d_%H_%M_%S")
    report_path = os.path.join(cur_path, reportName)  # 用例文件夹
    # 如果不存在这个report文件夹，就自动创建一个
    if not os.path.exists(report_path):os.mkdir(report_path)
    report_abspath = os.path.join(report_path, "result.html")
    print("report path:%s"%report_abspath)
    fp = open(report_abspath, "wb")
    # retry = 1 执行几次
    # verbosity =1 不显示注释内容，=2 显示注释内容
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                               verbosity=2,
                                               title=u'自动化测试报告,测试结果如下：',
                                               description=u'用例执行情况：')

    # 调用add_case函数返回值
    runner.run(all_case)

    fp.close()

def get_report_file(report_path):
    '''第三步：获取最新的测试报告'''
    lists = os.listdir(report_path)
    lists.sort(key=lambda fn: os.path.getmtime(os.path.join(report_path, fn)))
    print(u'最新测试生成的报告： '+lists[-1])
    # 找到最新生成的报告文件
    report_file = os.path.join(report_path, lists[-1])
    return report_file

def send_message():
    message = '检查失败'
    # Slack频道=【chen_test】，个人调试频道
    slackQaUrl = "https://hooks.slack.com/services/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"
    sendMessage.sendSlack(slackQaUrl, message)

    # 多个接收者用‘|’分隔
    touser = 'ChenChen'
    sendMessage.sendWeixin(touser, message)

if __name__ == "__main__":
    all_case = add_case()   # 1 加载用例
    run_case(all_case)        # 2执行用例
    # # 获取最新的测试报告文件
    report_path = os.path.join(cur_path, "report")  # 用例文件夹
    report_file = get_report_file(report_path)  # 3获取最新的测试报告
    print(report_file)
    send_message()





