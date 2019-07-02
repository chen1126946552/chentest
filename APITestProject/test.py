import time
import os

now = time.strftime("%Y_%m_%d_%H_%M_%S")
filename = "auto_cases_login_" + now + ".html"
report_path = os.path.dirname(os.path.realpath(__file__))
report_abspath = os.path.join(report_path, filename)
print(filename)
print(report_abspath)