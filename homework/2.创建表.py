import pymysql
import settings

def Maketable() :
    conn = pymysql.Connect(**settings.parameters)

    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    print(cursor)

    # 3 执行sql
    sql = """
    create table  if not exists user(uid int primary key auto_increment,username varchar(30) unique not null ,usertype enum('0','1') default '0' not null ,password char(48) not null,regtime DATE ,email VARCHAR(20) );
    """

    # 返回值是受影响行数
    res = cursor.execute(sql)


    # 5 关闭连接和游标
    cursor.close()
    conn.close()
