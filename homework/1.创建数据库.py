import pymysql
import settings

def databases() :
    conn = pymysql.Connect(**settings.parameters)


    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = """
    create database student02 default charset=utf8;
    """


    res = cursor.execute(sql)

    print(res)
    if res > 0:
        print("创建成功")
    else:
        print("创建失败")



    cursor.close()
    conn.close()
