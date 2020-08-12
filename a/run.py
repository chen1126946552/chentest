import os
from config.config import conf
from conftest import *

# cur_path = os.path.dirname(os.path.realpath(__file__))
# print(cur_path);
#
# # 执行命令 pytest run.py case
# message = sys.argv[1] + ' ' + " 异常,请查看。 报告地址： "
# print(message);
#
# caseName = "cases/" + sys.argv[1]
#
# # filename = sys.argv[2] + '.csv'
# # 生成报告的路径
# report_dir = conf.REPORT_DIR
#
# now = time.strftime("%Y_%m_%d_%H_%M_%S")
# filename = now + ".html"
# pytest.main(["--html=/Users/ptmind/Desktop/" + now + ".html", "case/" + sys.argv[1]])
# print("结束")

if __name__ == '__main__':
    count = 0
    while count < 20:
        pytest.main(['case/ui_engage_jp/test_create_data.py'])
        count = count+1
        print(count);
