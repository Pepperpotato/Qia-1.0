import datetime
import socket

# t1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#
# print(t1)
#
# hostname = socket.gethostname()
# regip = socket.gethostbyname(hostname)
#
# print(regip)
# from flask import request
#
# ip = request.remote_addr
#
# print(ip)


def sex_judge(sexvalue):
    if sexvalue == '男':
        s = 1
        return s
    else:
        s = 2
        return s


sexvalue = '男'

sex = sex_judge(sexvalue)

print(sex)

