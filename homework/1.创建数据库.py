import pymysql
import settings0

def databases() :
    conn = pymysql.Connect(**settings0.parameters)


    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql1 = """
    create database  bbs  default charset=utf8;
    """


    res1 = cursor.execute(sql1)


    if res1 > 0:
        print("创建成功")
    else:
        print("创建失败")



    sql2 = """
    create table  if not exists user(uid int primary key auto_increment,username varchar(30) unique not null ,usertype enum('0','1') default '0' not null ,password char(48) not null,regtime DATE ,email VARCHAR(20) );
    """


    res2 = cursor.execute(sql2)

    print(res2)
    if res2 > 0:
        print("创建成功")
    else:
        print("创建失败")



    cursor.close()
    conn.close()


