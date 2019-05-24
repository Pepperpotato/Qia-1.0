import pymysql
import settings

def Maketable() :
    conn = pymysql.Connect(**settings.parameters)

    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    print(cursor)


    sql = """
    create table  if not exists user(uid int primary key auto_increment,username varchar(30) unique not null ,usertype enum('0','1') default '0' not null ,password char(48) not null,regtime DATE ,email VARCHAR(20) );
    """


    res = cursor.execute(sql)



    cursor.close()
    conn.close()
