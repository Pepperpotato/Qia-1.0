from flask import render_template
from flask_mail import Message
from ext import mail


def send_mail(subject, to, sender, content, *args, **kwargs):
    """
    :param subject: 邮件主题
    :param to: 接收方，格式['user1','user2']
    :param sender: 发送方
    :param content: 邮件模板 ,默认html格式
    :param args: 邮件模板参数
    :param kwargs: 邮件模板参数
    :return:
    """
    if isinstance(to, (list, tuple)):
        reciever = to
    elif isinstance(to, str):
        reciever = to.split(',')
    else:
        raise Exception('邮件接受者参数类型错误')

    msg = Message(subject=subject, recipients=reciever, sender=sender)
    msg.html = render_template(content, *args, **kwargs)
    mail.send(msg)
    return True
