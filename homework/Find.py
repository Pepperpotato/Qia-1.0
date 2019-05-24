import pymysql
import settings
import hashlib
def find():

    conn = pymysql.Connect(**settings.parameters)

    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    while 1:
        username = input("请输入用户名：")

        sql1 = "select username from user where username=%s"

        res = cursor.execute(sql1,[username])

        if res == 0 :
            print('用户不存在')

        else :
            break

    sql = "select password from user where username=%s"
    cursor.execute(sql,[username])

    password = cursor.fetchall()[0]["password"]


    for i in range(3):

        inster = input('请输入您的密码：')

        sh1 = hashlib.sha1()
        sh1.update(inster.encode("utf8"))
        passwd = sh1.hexdigest()

        if passwd == password:
            break
        else:
            print('密码错误')
    else:
        print('密码验证失败！')
        return


    sql = "select username,usertype,password,regtime,email from user where username=%s"
    res = cursor.execute(sql, [username])
    if res > 0:

        records = cursor.fetchall()

        print(records)

    cursor.close()
    conn.close()

