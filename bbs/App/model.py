import re
from datetime import datetime

from flask import session

from ext import db

# 板块模型


class DBBase:
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    @staticmethod
    def save_all(*args):
        try:
            db.session.add_all(args)
            db.session.commit()
        except :
            db.session.rollback()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()


class Category(db.Model, DBBase):
    id = db.Column(db.Integer, primary_key=True)
    classname = db.Column(db.String(60), nullable=False)
    parentid = db.Column(db.Integer, nullable=False)
    classpath = db.Column(db.String(20))
    replycount = db.Column(db.Integer)
    motifcount = db.Column(db.Integer)
    compere = db.Column(db.String(10))
    classpic = db.Column(db.String(200))
    description = db.Column(db.String(1000))
    orderby = db.Column(db.Integer)
    lastpost = db.Column(db.String(600))
    namestyle = db.Column(db.String(10))
    ispass = db.Column(db.SmallInteger, nullable=False, default=1)
    # details = db.relationship('Details', backref='data', lazy='dynamic')
    __tablename__ = 'bbs_category'


class Link(db.Model, DBBase):
    lid = db.Column(db.SmallInteger, primary_key=True, autoincrement=True, nullable=False)
    displayorder = db.Column(db.SmallInteger, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    addtime = db.Column(db.Integer, nullable=False)
    __tablename__ = 'bbs_link'


class User(db.Model, DBBase):
        uid = db.Column(db.Integer, primary_key=True,autoincrement=True)
        username = db.Column(db.String(16), nullable=False)
        password = db.Column(db.String(64), nullable=False)
        email = db.Column(db.String(30), nullable=False)
        udertype = db.Column(db.SmallInteger, nullable=False)
        regtime = db.Column(db.DateTime, nullable=False)
        lasttime = db.Column(db.DateTime, nullable=False, default=datetime.now)
        allowlogin = db.Column(db.SmallInteger, default=0)
        regip = db.Column(db.Integer, nullable=False)
        picture = db.Column(db.String(255), nullable=False)
        grade = db.Column(db.Integer)
        autograph = db.Column(db.String(500))
        realname = db.Column(db.String(50), default='未知用户')
        sex = db.Column(db.SmallInteger, default=2)
        place = db.Column(db.String(50))
        qq = db.Column(db.String(13))
        # 指定表名
        __tablename__ = "bbs_user"


class Details(db.Model, DBBase):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    first = db.Column(db.SmallInteger, nullable=False)
    tid = db.Column(db.Integer)
    authorid = db.Column(db.Integer, nullable=False)
    title=db.Column(db.String(600), nullable=False)
    content=db.Column(db.TEXT(3000), nullable=False)
    addtime=db.Column(db.DateTime, nullable=False)
    addip=db.Column(db.Integer, nullable=False)
    classid=db.Column(db.Integer, nullable=False)
    replycount=db.Column(db.Integer, nullable=False)
    hits=db.Column(db.Integer, nullable=False)
    istop=db.Column(db.SmallInteger, nullable=False)
    elite=db.Column(db.SmallInteger, nullable=False)
    ishot=db.Column(db.SmallInteger, nullable=False)
    rate=db.Column(db.SmallInteger, nullable=False)
    attachment=db.Column(db.Integer)
    isdel=db.Column(db.Integer, nullable=False)
    style=db.Column(db.String(10))
    isdisplay=db.Column(db.Integer, nullable=False)

    __tablename__ = 'bbs_details'


class Web(db.Model, DBBase):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    sitename = db.Column(db.String(20), nullable=False)
    webname = db.Column(db.String(20), nullable=False)
    url = db.Column(db.String(20), nullable=False)
    webcode = db.Column(db.String(30), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    __tablename__ = 'bbs_web'

# 登录数据校验
def check_data(username, password, repassword, email, yzm):
    # print(username,password,repassword,email,yzm)

    if not re.search(r'^.{3,12}$', str(username)):
        return None
    tmp_username = User.query.with_entities(User.username).filter(User.username == username).all()
    if tmp_username:
        print('1')
        return None

    if not re.search(r'^.{3,12}$', str(password)):
        print('2')
        return None

    if password != repassword:
        print('3')
        return None

    if not re.search(r'^.+@.+$', str(email)):
        print('4')
        return None
    if yzm != session.get('yzm'):
        print('5')
        return None
    return True


# 检查用户的用户组
def check_userGroup(userinfo):

    if userinfo.udertype ==1:
        userGroup = '管理员'
        return userGroup
    else:
        userGroup = '普通用户'
        return userGroup


# 检查用户等级
def check_level(userinfo):
    if userinfo.grade <= 1000:
        level = '黑铁'
        return level
    elif userinfo.grade <= 2000:
        level = '青铜'
        return level
    elif userinfo.grade <= 3000:
        level = '白银'
        return level
    elif userinfo.grade <= 4000:
        level = '黄金'
        return level
    else:
        level = '钻石'
        return level


# 用户性别判断：
def sex_judge(sexvalue):
    if sexvalue == '男':
        return '1'
    else:
        return '2'



