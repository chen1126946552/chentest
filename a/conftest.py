import time
from selenium import webdriver
import pytest

result = ''
driver = None

def pytest_terminal_summary(terminalreporter):
    '''收集测试结果'''
    print(terminalreporter.stats)
    total = terminalreporter._numcollected
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    error = len(terminalreporter.stats.get('error', []))
    print("total:", total)
    print('passed:', passed)
    print('failed:', failed)
    print('error:', error)
    # print('skipped:', len(terminalreporter.stats.get('skipped', [])))
    # terminalreporter._sessionstarttime 会话开始时间
    duration = time.time() - terminalreporter._sessionstarttime
    print('total times:', duration, 'seconds')
    # if(total > 0):
    #     print(sys.argv[0]);
    #     print(sys.argv[1]);
        # print(sys.argv[2]);
        # a("****----yongli******")

@pytest.fixture(scope='session', autouse=True)
def browser(request):
    global driver
    if driver is None:
        chromedrive = "/Users/ptmind/Desktop/pt-gitlab/chromedriver"
        chrome_opt = webdriver.ChromeOptions()
        # chrome_opt.add_argument("--headless")
        chrome_opt.add_argument('--no-sandbox')
        chrome_opt.add_argument('--disable-gpu')
        chrome_opt.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(chromedrive, chrome_options=chrome_opt)
    def end():
        driver.quit()
    request.addfinalizer(end)
    return driver

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    #当测试失败的时候，自动截图，展示到html报告中
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            screen_img = _capture_screenshot()
            if file_name:
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:600px;height:300px;" ' \
                           'onclick="window.open(this.src)" align="right"/></div>' % screen_img
                extra.append(pytest_html.extras.html(html))
        report.extra = extra

def _capture_screenshot():
        '''
        截图保存为base64，展示到html中
        '''
        return driver.get_screenshot_as_base64()

