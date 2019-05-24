import pymysql
import settings

def Maketable() :
    conn = pymysql.Connect(**settings.parameters)

    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    print(cursor)



    res = cursor.execute(sql)



    cursor.close()
    conn.close()
