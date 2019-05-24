import pymysql
import settings
import register
import Find
import Maketable
import time


if __name__ == '__main__':

    print('***用户注册(1)***')
    print('***用户登录(2)***')

    do = input('请输入您的操作：')
    if do == '1':
        register.register()
    if do == '2':
        Find.find()

