import pymysql
import settings


conn = pymysql.Connect(**settings.parameters)

cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
print(cursor)



while 1:
    username = input("请输入用户名：")
    if  len(username)<2 or username is '':
            print('用户名不能少于两个字符')
    else:
        break

usertype = input('请输入用户类型：')

password = input("请输入密码：")

regtime = input('请输入注册时间：')

email = input('请输入您的邮箱：')



sql = """
insert into user(username,usertype,password,regtime,email) values ('%s','%s',sha1('%s'),'%s','%s')
""" % (username,usertype,password,regtime,email)
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
