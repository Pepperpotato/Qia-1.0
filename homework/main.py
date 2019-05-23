import pymysql
import settings
import time
# 创建数据库
# def Makedatabase():
#     conn = pymysql.Connect(**settings.parameters)
#
#     cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
#
#     sql = """
#     create database bbs default charset=utf8;
#     """
#
#     res = cursor.execute(sql)
#
#     print(res)
#     if res > 0:
#         print("创建成功")
#     else:
#         print("创建失败")
#
#     cursor.close()
#     conn.close()

# 创建表
def Maketable():
    conn = pymysql.Connect(**settings.parameters)

    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    print(cursor)


    sql = """
    create table  if not exists user(uid int primary key auto_increment,username varchar(30) unique not null ,usertype enum('0','1') default '0' not null ,password char(48) not null,regtime DATE ,email VARCHAR(20) );
    """


    res = cursor.execute(sql)


    cursor.close()
    conn.close()

# 注册
def Register():
    conn = pymysql.Connect(**settings.parameters)

    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    print(cursor)

    while 1:
        username = input("请输入用户名：")
        if len(username) < 2 or username is '':
            print('用户名不能少于两个字符')
        else:
            break

    usertype = input('请输入用户类型：')

    password = input("请输入密码：")

    regtime = time.strftime("%Y-%m-%d")

    email = input('请输入您的邮箱：')

    sql = """
    insert into user(username,usertype,password,regtime,email) values ('%s','%s',sha1('%s'),'%s','%s')
    """ % (username, usertype, password, regtime, email)
    print(sql)
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
        # 5 关闭连接和游标
        cursor.close()
        conn.close()

# 查找
def Find():
    conn = pymysql.Connect(**settings.parameters)

    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # print(cursor)

    # 3 执行sql
    username = input("请输入用户名：")
    # sql = "select username,password from user where username='%s'" % username
    sql = "select username,username,password,regtime ,email from user where username=%s"

    res = cursor.execute(sql, [username])

    if res > 0:
        # 4 获取数据

        records = cursor.fetchall()
        # for rec in records:
        #     print(rec['username'])
        print(records)

    cursor.close()
    conn.close()

if __name__ == '__main__':
    # Makedatabase()
    Maketable()
    Register()
    Find()

