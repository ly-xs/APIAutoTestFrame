import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from common.sendrequests import send_requests
from ddt import ddt, data
from common.readexcel import ExcelReader
from common.writeexcel import ExcelWriter
from config.config import SOURCE_FILE, TARGET_FILE
import unittest
import requests

testData = ExcelReader(SOURCE_FILE)
testData.load_data()


@ddt
class Demo_API(unittest.TestCase):
    """发布会系统"""

    def setUp(self):
        self.s = requests.session()

    def tearDown(self):
        pass

    @data(*testData.get_all_data())
    def test_api(self, excel_data):
        # 获取ID字段数值，截取结尾数字并去掉开头0
        rowNum = int(excel_data['ID'].split("_")[2])
        print(f"******* 正在执行用例 ->{excel_data['ID']} *********")
        print(f"请求方式: {excel_data['method']}，请求URL: {excel_data['url']}")
        print(f"请求参数: {excel_data['params']}")
        print(f"post请求body类型为：{excel_data['type']} ,body内容为：{excel_data['body']}")
        # 发送请求
        re = send_requests(self.s, excel_data)
        # 获取服务端返回的值
        self.result = re.json()
        print(f"页面返回信息：{re.content.decode()}")
        # 获取excel表格数据的状态码和消息
        readData_code = int(excel_data["status_code"])
        readData_msg = excel_data["msg"]
        if readData_code == self.result['status'] and readData_msg == self.result['message']:
            OK_data = "PASS"
            print(f"用例测试结果:  {excel_data['ID']}---->{OK_data}")
            ExcelWriter(TARGET_FILE).write_data(rowNum + 1, OK_data)
        if readData_code != self.result['status'] or readData_msg != self.result['message']:
            NOT_data = "FAIL"
            print(f"用例测试结果:  {excel_data['ID']}---->{NOT_data}")
            ExcelWriter(TARGET_FILE).write_data(rowNum + 1, NOT_data)
        self.assertEqual(self.result['status'], readData_code, f"返回实际结果是->:{self.result['status']}")
        self.assertEqual(self.result['message'], readData_msg, f"返回实际结果是->:{self.result['message']}")
