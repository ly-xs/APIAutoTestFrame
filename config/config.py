import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

# 配置文件
CONFIG_FILE = os.path.join(BASE_DIR, "config", "config.ini")
# 测试用例模板文件
SOURCE_FILE = os.path.join(BASE_DIR, "database", "DemoAPITestCase.xlsx")
# excel测试用例结果文件
TARGET_FILE = os.path.join(BASE_DIR, "report", "excelReport", "DemoAPITestCase.xlsx")
# 测试报告目录
TEST_REPORT_DIR = os.path.join(BASE_DIR, "report")
# 测试用例目录
TEST_DIR = os.path.join(BASE_DIR, "testcase")
