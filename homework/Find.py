import pymysql
import settings

def find():

    conn = pymysql.Connect(**settings.parameters)

    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)



    username = input("请输入用户名：")

    sql = "select username,usertype,password,regtime,email from user where username=%s"


    res = cursor.execute(sql,[username])

    if res > 0:


        records = cursor.fetchall()

        print(records)


    cursor.close()
    conn.close()
