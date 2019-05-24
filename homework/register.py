import pymysql
import settings
import time
import re


def register():

    conn = pymysql.Connect(**settings.parameters)

    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)




    while 1:

        username = input("请输入用户名：")

        sql = "select username from user where username=%s"

        res = cursor.execute(sql, [username])

        if res > 0:
            print('用户名已存在，请重新输入')
        else:
            str1 = username.split()

            if  len(username)<2 or str1 == '':
                print('用户名不能少于两个字符且不能为空')
            else:
                break


    usertype = input('请输入用户类型：0为普通用户，1为管理员:')


    password = input("请输入密码：")


    regtime = time.strftime("%Y-%m-%d")
    while 1:
        email = input('请输入您的邮箱：')
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) == None:
            print('邮箱格式不正确，请重新输入！')
        else:
            break


    sql = """
    insert into user(username,usertype,password,regtime,email) values ('%s','%s',sha1('%s'),'%s','%s')
    """ % (username,usertype,password,regtime,email)

    try:

        res = cursor.execute(sql)
        if res:
            conn.commit()

            print(cursor._executed)
        else:
            conn.rollback()
    except Exception as e:
        print(e)
        conn.rollback()
    finally:

            cursor.close()
            conn.close()

