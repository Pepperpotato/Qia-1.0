# import pymysql
# import settings
#
# def find():
#
#     conn = pymysql.Connect(**settings.parameters)
#
#     cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
#     # print(cursor)
#
#     # 3 执行sql
#     username = input("请输入用户名：")
#     # sql = "select username,password from user where username='%s'" % username
#     sql = "select username,password from user where username=%s"
#
#
#     res = cursor.execute(sql,[username])
#
#     if res > 0:
#         # 4 获取数据
#
#         records = cursor.fetchall()
#         # for rec in records:
#         #     print(rec['username'])
#         print(records)
#
#
#     cursor.close()
#     conn.close()
import  time

t7 = time.strftime("%Y-%m-%d")
print(t7)