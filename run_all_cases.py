import os
import sys
import time
import unittest

sys.path.append(os.path.dirname(__file__))
from common.mysqlDB import MySQLDatabase
from common.HTMLTestRunner import HTMLTestRunner
from common.sendmail import send_mail
from config.config import TEST_REPORT_DIR, TEST_DIR


def run_case(test_path=TEST_DIR, result_path=TEST_REPORT_DIR):
    """执行所有的测试用例"""

    # 初始化接口测试数据
    MySQLDatabase().init_data()

    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = f'{result_path}/{now}result.html'
    with open(filename, 'wb') as f:
        runner = HTMLTestRunner(stream=f, title='发布会系统接口自动化测试报告', description='环境：windows 10')
        runner.run(unittest.defaultTestLoader.discover(test_path, pattern='*API.py'))
    lists = os.listdir(result_path)
    lists.sort(key=lambda fn: os.path.getmtime(result_path + "\\" + fn))
    report = os.path.join(result_path, lists[-1])
    send_mail(report)  # 调用发送邮件模块


if __name__ == "__main__":
    run_case()
