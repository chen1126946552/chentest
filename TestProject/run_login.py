# -*- coding: utf-8 -*-

import os
from common.run_case import add_case
from common.run_case import run_case
from common.run_case import get_report_file
from common.run_case import send_message
import config.config


cur_path = os.path.dirname(os.path.realpath(__file__))
message = "登录心跳服务异常, 报告地址： "
caseName = "cases/login"

if __name__ == "__main__":
    all_case = add_case(cur_path, caseName)   # 1 加载用例
    s = run_case(cur_path, all_case)        # 2执行用例
    # # 获取最新的测试报告文件
    report_path = os.path.join(cur_path, "report")  # 用例文件夹
    report_file = get_report_file(report_path)  # 3获取最新的测试报告
    message2 = message + config.config.REPORT_URL + report_file
    if s.failure_count + s.error_count > 0:
        send_message(message, config.config.SLACK_CHANNEL, config.config.WEIXI_TOUSER)





