# -*- coding:utf-8 -*-
import unittest
from utils.HTMLTestRunner import HTMLTestRunner
from utils.sendmail import *

# 加载指定目录下的所有case
test_dir = os.path.abspath('..') + "\\testcase"
discover = unittest.defaultTestLoader.discover(test_dir, pattern='test*.py', top_level_dir=None)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    # 生成测试报告
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = os.path.abspath('..') + "\\report\\" + now + " result.html"
    fp = open(filename, "wb")
    runner = HTMLTestRunner(stream=fp,
                            title=u'自动化测试报告',
                            description=u'用例执行情况：')
    runner.run(discover)
    fp.close()
    # 邮件发送最新测试报告
    send_report()
