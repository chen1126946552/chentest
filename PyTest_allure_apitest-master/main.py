# -*- coding:utf-8 -*-
# coding:utf-8
import os

import pytest

from config.ConfigLogs import LogConfig

case_path = os.path.join(os.getcwd())
PATH = os.path.split(os.path.realpath(__file__))[0]
failureException = AssertionError

if __name__ == '__main__':
    LogConfig(PATH)
    pytest.main("%s --alluredir report" % case_path)
    # pytest.main()
    os.popen("allure generate report/ -o result/ --clean")
    os.popen("allure open -h 0.0.0.0 -p 8083 result/")
