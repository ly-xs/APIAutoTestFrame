import os
import sys
import configparser

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import config as cf
from pymysql import connect, cursors
from pymysql.err import MySQLError

# --------- 读取config.ini配置文件 ---------------
config = configparser.ConfigParser()
config.read(cf.CONFIG_FILE, encoding='UTF-8')
host = config.get("mysql conf", "host")
port = config.get("mysql conf", "port")
user = config.get("mysql conf", "user")
password = config.get("mysql conf", "password")
database = config.get("mysql conf", "db_name")


class MySQLDatabase:
    def __init__(self):
        try:
            self.connection = connect(user=user,
                                      password=password,
                                      host=host,
                                      database=database,
                                      port=int(port),
                                      cursorclass=cursors.DictCursor
                                      )
            print("Connection successful")
        except MySQLError as e:
            print(f"Error connecting to MySQL: {e}")
            self.connection = None

    def insert(self, table, data):
        """
        Insert data into the specified table.
        :param table: Table name.
        :param data: Dictionary of column-value pairs to insert.
        """
        if not self.connection:
            print("Connection not established")
            return False

        for key in data:
            data[key] = "'" + str(data[key]) + "'"
        key = ','.join(data.keys())
        value = ','.join(data.values())

        query = f"INSERT INTO {table} ({key}) VALUES ({value})"

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
            self.connection.commit()
            print("Insert successful")
            return True
        except MySQLError as e:
            print(f"Error inserting data: {e}")
            return False

    def query(self, table, conditions=None):
        """
        Query data from the specified table.
        :param table: Table name.
        :param conditions: Dictionary of column-value pairs for WHERE clause.
        :return: List of rows matching the query.
        """
        if not self.connection:
            print("Connection not established")
            return None

        query = f"SELECT * FROM {table}"
        values = []

        if conditions:
            placeholders = ' AND '.join([f"{col} = %s" for col in conditions.keys()])
            query += f" WHERE {placeholders}"
            values = list(conditions.values())

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, values)
                result = cursor.fetchall()
            return result
        except MySQLError as e:
            print(f"Error querying data: {e}")
            return None

    def clear(self, table):
        """
        Clear all data from the specified table.
        :param table: Table name.
        """
        if not self.connection:
            print("Connection not established")
            return False

        query = f"DELETE FROM {table}"

        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SET FOREIGN_KEY_CHECKS=0")
                cursor.execute(query)
            self.connection.commit()
            print(f"All data cleared from {table}")
            return True
        except MySQLError as e:
            print(f"Error clearing data: {e}")
            return False

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed")

    def init_data(self, datas):
        print(datas)
        for table, data in datas.items():
            self.clear(table)
            for d in data:
                self.insert(table, d)
        self.close()


if __name__ == '__main__':
    db = MySQLDatabase()
    # 定义过去时间
    import time
    past_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - 100000))
    # 定义将来时间
    future_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 10000))

    # 创建测试数据
    datas = {
        # 发布会表数据
        'sign_event': [
            {'id': 1, 'name': '红米Pro发布会', '`limit`': 2000, 'status': 1, 'address': '北京会展中心', 'start_time': future_time},
            {'id': 2, 'name': '苹果iphon6发布会', '`limit`': 1000, 'status': 1, 'address': '宝安体育馆', 'start_time': future_time},
            {'id': 3, 'name': '华为荣耀8发布会', '`limit`': 2000, 'status': 0, 'address': '深圳福田会展中心', 'start_time': future_time},
            {'id': 4, 'name': '苹果iphon8发布会', '`limit`': 2000, 'status': 1, 'address': '深圳湾体育中心', 'start_time': past_time},
            {'id': 5, 'name': '小米5发布会', '`limit`': 2000, 'status': 1, 'address': '北京国家会议中心', 'start_time': future_time},
        ],
        # 　嘉宾表数据
        'sign_guest': [
            {'id': 1, 'realname': 'Tom', 'phone': 13511886601, 'email': 'alen@mail.com', 'sign': 0, 'event_id': 1},
            {'id': 2, 'realname': 'Jason', 'phone': 13511886602, 'email': 'sign@mail.com', 'sign': 1, 'event_id': 1},
            {'id': 3, 'realname': 'Jams', 'phone': 13511886603, 'email': 'tom@mail.com', 'sign': 0, 'event_id': 5},
        ],
    }
    db.init_data(datas)
