from impala import dbapi
import pandas as pd
import pymysql
from singleton import singleton

"""
USER： River
Date： 2018-11-13
数据库连接：单例模式
提供方法：
1. 插入数据：insert
2. 更新数据：update
3. 查询数据：query
4. 通用执行：execute
5. 关闭资源：close
6. 设置mysql连接：set_mysql_conn
7. 设置hive连接：set_hive_conn
8. 设置自定义数据库连接：set_custom_conn

更新记录
2018-11-13：增加对db_name参数的检测
2019-03-12: dataframe中包含有sql关键词，会导致sql执行失败，报错原因为SQL语句有错误。解决方法为给所有列名加上sql引号
2019-03-12: 值为nan时无法插入，先填充空值
2019-03-13: 1. update增加自定义条件字段； 2. 增加数据库多连接功能，一个可以建立多个mysql源连接
2019-05-23: 修改mysql的insert语句为replace语句
2019-09-16: 增加excute方法执行结果的输出和执行是否成功的反馈
"""


@singleton
class DBTool:
    __db_conn = {"mysql": None, "hive": None}

    def __init__(self):
        pass

    def __check(self, db_name):
        """
        检查输入的数据库是否正确
        :param db_name:  待检查的数据库名
        :return:
        """
        if db_name not in self.__db_conn.keys():
            print('Error: db_name "%s" not defined!' % db_name)
            exit(1)
        return True

    def is_connected(self, db_name):
        """
        判断数据库连接的状态
        :param db_name: 查看的数据库，当前可选值为：mysql、hive
        :return: 返回该数据库得到连接状态，已连接返回True，未连接返回False
        """

        if self.__check(db_name):
            if self.__db_conn[db_name] is None:
                return False
            else:
                return True

    def set_custom_conn(self, db_name, db_conn):
        """
        创建自定义数据库连接
        :param db_name: 自定义数据库名
        :param db_conn: 数据库连接
        """
        self.__db_conn[db_name] = db_conn

    def set_mysql_conn(self, host, port, user, passwd, db, db_name='mysql'):
        """
        创建Mysql连接
        :param host: mysql主机IP
        :param port: mysql主机端口
        :param user: mysql用户名
        :param passwd: mysql用户密码
        :param db: mysql连接数据库
        :param db_name: 数据库多连接功能，一个可以建立多个mysql源连接, 通过db_name进行区分
        """
        try:
            self.__db_conn[db_name] = pymysql.Connect(host=host, port=port, user=user, passwd=passwd, db=db,
                                                      charset='utf8')
        except Exception as e:
            print("Warring:" + str(e))
            pass

    def set_hive_conn(self, host, port, user, passwd, db_name='hive'):
        """
        创建Hive连接
        :param host: Hive主机IP
        :param port: Hive主机端口
        :param user: Hive用户名
        :param passwd: Hive用户密码
        :param db_name: 数据库多连接功能，一个可以建立多个mysql源连接, 通过db_name进行区分
        """
        try:
            self.__db_conn[db_name] = dbapi.connect(host=host, port=port, auth_mechanism="PLAIN", user=user,
                                                    password=passwd)
        except Exception as e:
            print("Warring:" + str(e))
            pass

    def __del__(self):
        self.close()

    def close(self):
        for db_name in self.__db_conn.keys():
            if self.__db_conn[db_name] is None:
                continue
            try:
                self.__db_conn[db_name].close()
            except Exception as e:
                print("Warring:" + str(e))
                pass

    def execute(self, sql, db_name):
        """
        通用sql执行方法
        :param sql: 待执行的sql
        :param db_name: 使用的数据库
        """
        self.__check(db_name)
        cursor = self.__db_conn[db_name].cursor()
        try:
            print(cursor.execute(sql))
        except Exception as e:
            cursor.close()
            print("Error: 语句(" + sql + ")执行错误！错误原因：" + str(e))
            return False
            # exit(2)
        self.__db_conn[db_name].commit()
        return True

    def insert(self, db_name, word=None, table=None, insert_values=None, sql=None, filler=None):
        """
        Mysql 数据插入
        注：hive不建议进行大批量的插入
        :param db_name: 待使用的数据库，当前支持mysql、hive，类型：str
        :param word: 要插入的字段集合，类型：list，array
        :param table: 要插入的表，类型：str
        :param insert_values: 要插入的数据，类型：dataframe
        :param sql: 插入sql，若sql不为空，则直接根据sql语句进行插入；否则根据插入内容进行组成sql进行插入
        :param filler: insert_values中有空值时用filkler填充，类型：str
        :return: flag（是否执行成功），code（执行代码：0为正常执行，102为主键冲突，103为其他错误），返回结果（执行报告+影响行数）
        """
        if filler is not None:
            insert_values.fillna(filler, inplace=True)
        # 检查当前输入的db_name是否存在
        self.__check(db_name)
        temp_ = ','.join(['%s'] * len(word))
        if sql is None:
            # pd.DataFrame().to_sql()
            sql = "REPLACE INTO " + table + " (`" + '`,`'.join(word) + "`) VALUES (%s)" % temp_
        cursor = self.__db_conn[db_name].cursor()
        try:
            cursor.executemany(sql, insert_values.values.tolist())
        except Exception as e:
            print("Error: 插入语句(" + sql + ")执行错误！错误原因：" + str(e))
            if "key 'unique'" in str(e):
                return False, 102, "Error: 插入语句(" + sql + ")执行错误！错误原因：" + str(e)
            else:
                return False, 103, "Error: 插入语句(" + sql + ")执行错误！错误原因：" + str(e)
        num_count = cursor.rowcount
        printstr = "SUCCESS: 插入语句(" + sql + ")执行成功，" + str(num_count) + "条记录受影响！"
        # tools.log_print(printstr)
        self.__db_conn[db_name].commit()
        cursor.close()
        return True, 0, [printstr, num_count]

    @staticmethod
    def __query_format(qf_res, qf_des):
        """
        查询结果规整为DataFrame
        :param qf_res: 查询的结果数据
        :param qf_des: 查询结果的字段名
        :return:
        """
        col_li = [item[0] for item in qf_des]
        return pd.DataFrame(list(qf_res), columns=col_li)

    def query(self, db_name, word=None, table=None, condition='', sql=None):
        """
        mysql查询
        :param db_name: 待使用的数据库，当前支持mysql、hive，类型：str
        :param word: list 要查询的字段列表
        :param table: string 要查询的表
        :param condition: String 查询条件
        :param sql: 当sql不为None时，其他参数不生效
        :return: 成功标志, 成功返回值, 查询结果dataframe
        """
        # 检查当前输入的db_name是否存在
        self.__check(db_name)

        if sql is None:
            sql = "SELECT " + ','.join(word) + " FROM " + table + " " + condition
        cursor = self.__db_conn[db_name].cursor()
        try:
            cursor.execute(sql)
        except Exception as e:
            cursor.close()
            return False, 101, "Error: 查询语句(" + sql + ")执行错误！错误原因：" + str(e)
        self.__db_conn[db_name].commit()
        res = cursor.fetchall()
        des = cursor.description
        cursor.close()
        return True, 0, self.__query_format(res, des)

    def update(self, db_name, update_cols=None, condition_cols=None, table=None, update_values=None, sql=None,
               filler='', condition=1):
        """
        mysql 数据更新
        :param db_name: 待使用的数据库，当前支持mysql、hive，类型：str
        :param update_cols: 待更新的列
        :param condition_cols: 条件列
        :param table: 待更新的表
        :param update_values: 待更新的值
        :param sql: 当sql不为None时，其他参数不生效
        :param filler: insert_values中有空值时用filkler填充，类型：str
        :param condition: 额外的，自定义的更新条件
        :return: flag（是否执行成功），code（执行代码：0为正常执行，105为其他错误），返回结果（执行报告+影响行数）
        """
        if filler is not None:
            update_values.fillna(filler, inplace=True)
        # 检查当前输入的db_name是否存在
        self.__check(db_name)
        update_str = []
        for item in update_cols:
            update_str.append('`' + item + '`=%s')
        condition_str = []
        for item in condition_cols:
            condition_str.append('`' + item + '`=%s')
            sql = "UPDATE `" + table + "` SET " + ', '.join(update_str) + " WHERE " + ' and '.join(
                condition_str) + ' and ' + str(condition)
        cursor = self.__db_conn[db_name].cursor()
        try:
            cursor.executemany(sql, update_values.loc[:, update_cols + condition_cols].values.tolist())
        except Exception as e:
            cursor.close()
            return False, 105, "Error: 更新语句(" + sql + ")执行错误！错误原因：" + str(e)
        num_count = cursor.rowcount
        printstr = "SUCCESS: 更新语句(" + sql + ")执行成功，" + str(num_count) + "条记录受影响！"
        self.__db_conn[db_name].commit()
        cursor.close()
        return True, 0, [printstr, num_count]


if __name__ == '__main__':
    dbt = DBTool()
    dbt.set_mysql_conn(host="127.0.0.1", port=3306, user='root', passwd='a123456', db="db_meicloud_ai_data")
    print(dbt.query(db_name='esb', word=["*"], table='cprd_temp2'))
