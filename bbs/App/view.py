import datetime
import hashlib
import os

from flask import Blueprint, render_template, request, session, Response, redirect, url_for, current_app
from sqlalchemy import func

from ext import db
from .VerfiCode import VerfiCode
from App.model import Category, Link, User, Details, check_data, check_userGroup, check_level, Web
from flask_mail import Mail
from ext import mail

bbs = Blueprint('bbs', __name__, url_prefix='/bbs')


@bbs.route('/', methods=["GET", "POST"])
@bbs.route('/index', methods=['GET', 'POST'])
@bbs.route('/<int:cid>', methods=["GET", "POST"])
def index(cid=0):

    if cid == 0:
        big_section = Category.query.filter(Category.parentid == cid).all()
    else:
        big_section = Category.query.filter(Category.id == cid).all()
    all_big_sections = Category.query.filter(Category.parentid == 0).all()
    small_sections = Category.query.filter(Category.parentid != 0).all()

    # 友情链接表
    links = Link.query.all()

    # 网站信息表
    web_info = Web.query.get(1)
    print(web_info)

    # 用户表
    users = User.query.all()
    users_count = User.query.with_entities(func.count(User.username)).filter(User.udertype==0).scalar()
    new_vip = User.query.with_entities(User.username).order_by(-User.uid).limit(1).all()

    #  帖子总数
    detail_count = Details.query.with_entities(func.count(Details.first)).filter(Details.first == 1).group_by(
        Details.first).all()
    # 对应板块回复数量
    reply_count = Details.query.with_entities(Details.classid, func.count('*')).filter(Details.first == 0).group_by(Details.classid).all()[0]
    # print(reply_count)
    # 对应板块帖子数量
    detail1_count = Details.query.with_entities(Details.classid,func.count('*')).filter(Details.first == 1).group_by(
        Details.classid).all()
    print(detail1_count)
    username = session.get('username')
    #
    if User.query.filter(User.username == username).all():
        user = User.query.filter(User.username == username).all()[0]

        user_integral = user.grade
        user_tx = user.picture
        print(user_tx)
        user_group = check_userGroup(user)
        return render_template('index.html', **{
            'user_integral': user_integral,
            'user_tx': user_tx,
            'category': big_section,
            'all_big_sections': all_big_sections,
            'small_sections': small_sections,
            'links': links,
            'users': users,
            'users_count': users_count,
            'new_vip': new_vip[0][0],
            'username': username,
            'detail_count': detail_count[0][0],
            'user_group': user_group,
            'web_info': web_info,
            'reply_count': reply_count,
            'detail1s_count': detail1_count
        })

    return render_template('index.html', **{
        'category': big_section,
        'all_big_sections': all_big_sections,
        'small_sections': small_sections,
        'links': links,
        'users': users,
        'users_count': users_count,
        'new_vip': new_vip[0][0],
        'username': username,
        'detail_count': detail_count[0][0],
        'web_info': web_info,
        'reply_count': reply_count,
        'detail1s_count': detail1_count
    })


@bbs.route('/index')
def jump_index():
    return render_template('index.html')


@bbs.route('/list/<int:cid>')
def web_list(cid):
    if cid == 0:
        big_section = Category.query.filter(Category.parentid == cid).all()
    else:
        big_section = Category.query.filter(Category.id == cid).all()
    all_big_sections = Category.query.filter(Category.parentid == 0).all()
    small_sections = Category.query.filter(Category.parentid != 0).all()
    current_category = Category.query.get(cid)

    # 帖子信息
    list_contents = Details.query.filter(Details.first == 1, Details.isdel == 0).all()
    web_info = Web.query.get(1)

    username = session.get('username')

    if User.query.filter(User.username == username).all():
        user = User.query.filter(User.username == username).all()[0]

        user_integral = user.grade
        user_tx = user.picture

        return render_template('list.html', **{
            'user_integral': user_integral,
            'user_tx': user_tx,
            'category': big_section,
            'all_big_sections': all_big_sections,
            'small_sections': small_sections,
            'username': username,
            "current_category": current_category,
            'list_contents': list_contents,
            'web_info': web_info

        })

    return render_template('list.html', **{
        'category': big_section,
        'all_big_sections': all_big_sections,
        'small_sections': small_sections,
        'detail_title': list_contents,
        "current_category": current_category,
        'list_contents': list_contents,
        'web_info': web_info
    })


@bbs.route('/getpassword')
def getpassword():

    big_section = Category.query.filter(Category.parentid == 0).all()
    web_info = Web.query.get(1)
    all_big_sections = Category.query.filter(Category.parentid == 0).all()

    return render_template('getpassword.html', **{
        'category': big_section,
        'all_big_sections': all_big_sections,
        'web_info': web_info
    })


@bbs.route('/search')
def search():

    return render_template('search.html')


@bbs.route('/detail/<int:cid>')
def detail(cid):
    web_info = Web.query.get(1)
    all_big_sections = Category.query.filter(Category.parentid == 0).all()
    small_sections = Category.query.filter(Category.parentid != 0).all()
    # 当前板块id
    current_classid = Details.query.with_entities(Details.classid).filter(Details.id == cid).first()[0]

    current_ss = Category.query.filter(Category.id == current_classid).all()[0]
    current_bs = Category.query.filter(Category.id == current_ss.parentid).all()[0]
    # 当前帖子所有信息
    detail = Details.query.filter(Details.id == cid and Details.first == 1)[0]
    authorid = detail.authorid

    # 发帖人信息
    authorinfo = User.query.filter(User.uid == authorid).all()[0]
    user_group = check_userGroup(authorinfo)
    user_level = check_level(authorinfo)

    # 不使用外键,多表外链接查询回帖信息
    replyinfo = db.session().query(Details, User)
    replyinfo = replyinfo.join(Details, Details.authorid == User.uid)
    replyinfo = replyinfo.filter(Details.first == 0 and Details.tid == cid).all()

    username = session.get('username')
    if username:
        uid = User.query.with_entities(User.uid).filter(User.username == username).first()[0]
        user = User.query.get(uid)
        user_integral = user.grade
        user_tx = user.picture
        user_group = check_userGroup(user)
        if not username or User.query.with_entities(User.udertype).filter(User.username == username).all()[0][0] == 0:
            Guanli = 0

        else:
            Guanli = 1

            current_whatever = Details.query.get(cid)



            # 删除
            isdel = request.args.get('isdel')
            if isdel:
                current_whatever.isdel = int(isdel)
                current_whatever.delete()

            # 屏蔽
            isdisplay = request.args.get('isdisplay')
            if isdisplay:
                current_whatever.isdisplay = int(isdisplay)
                current_tid = current_whatever.tid
                current_whatever.save()
                return redirect(url_for('bbs.detail', cid=current_tid))
            # 置顶
            istop = request.args.get('istop')
            if istop:
                current_whatever.istop = 1
                current_whatever.save()
            # 精华
            elite = request.args.get('elite')
            if elite:
                current_whatever.elite = 1
                current_whatever.save()

            # 高亮
            style = request.args.get('style')
            if style:
                current_whatever.style = 'orange'
                current_whatever.save()

        return render_template('detail.html', **{
            'all_big_sections': all_big_sections,
            'small_sections': small_sections,
            'detail': detail,
            'current_ss': current_ss,
            'current_bs': current_bs,
            'authorinfo': authorinfo,
            'Guanli': Guanli,
            'replysinfo': replyinfo,
            'user_group': user_group,
            'user_level': user_level,
            'user_integral': user_integral,
            'user_tx': user_tx,
            'username': username,
            'web_info': web_info
        })
    else:
        return render_template('detail.html', **{
            'all_big_sections': all_big_sections,
            'small_sections': small_sections,
            'detail': detail,
            'current_ss': current_ss,
            'current_bs': current_bs,
            'authorinfo': authorinfo,
            'replysinfo': replyinfo,
            'user_group': user_group,
            'user_level': user_level,
            'web_info': web_info
        })


@bbs.route('/reply/<int:cid>', methods=["GET", "POST"])
def reply(cid):
    replyname = session.get('username')
    if not replyname:
        return redirect(url_for('bbs.nologin'))
    else:
        reply_content = request.form.get('message')
        reply_id = User.query.with_entities(User.uid).filter(User.username == replyname).first()[0]
        title = '__'
        add_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ip = request.remote_addr
        # 当前帖子的id
        current_id = cid
        # 当前板块id
        current_classid = Details.query.with_entities(Details.classid).filter(Details.id == cid).all()[0][0]
        print(current_classid)

        new_reply = Details(first=0, authorid=reply_id, tid=current_id, title=title, content=reply_content, addtime=add_time,classid=current_classid, replycount=0, hits=0, istop=0, ishot=0, elite=0, rate=0, isdel=0, isdisplay=0, addip=ip)
        new_reply.save()

        return redirect(url_for('bbs.detail', cid=current_id))


@bbs.route('/login', methods=["GET", "POST"])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    password = hashlib.sha1(password.encode('utf8')).hexdigest()
    db_username = User.query.with_entities(User.username).filter(User.username == username).all()
    if db_username:
        db_password = User.query.with_entities(User.password).filter(User.username == username).all()

        if password == db_password[0][0]:
            session['username'] = username

    return redirect(url_for('bbs.index'))


@bbs.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('bbs.index'))


@bbs.route('/nologin', methods=['GET', 'POST'])
def nologin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password = hashlib.sha1(password.encode('utf8')).hexdigest()
        db_username = User.query.with_entities(User.username).filter(User.username == username).all()
        if db_username:
            db_password = User.query.with_entities(User.password).filter(User.username == username).all()

            if password == db_password[0][0]:
                session['username'] = username

        return redirect(url_for('bbs.index'))
    else:
        web_info = Web.query.get(1)
        all_big_sections = Category.query.filter(Category.parentid == 0).all()
        big_section = Category.query.filter(Category.parentid == 0).all()

        return render_template('nologin.html', **{
            'category': big_section,
            'all_big_sections': all_big_sections,
            'web_info': web_info
        })


@bbs.route('/reg', methods=["GET", "POST"])
def reg():
    # 判断是否为空
    web_info = Web.query.get(1)
    big_section = Category.query.filter(Category.parentid == 0).all()

    all_big_sections = Category.query.filter(Category.parentid == 0).all()

    if request.form:
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        email = request.form.get('mail')
        code = request.form.get('yzm')
        result = check_data(username, password, repassword, email, code)

        if result:
            password = hashlib.sha1(password.encode('utf8')).hexdigest()
            reg_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ip = request.remote_addr

            user = User(username=username, password=password, email=email, udertype= 0, regtime=reg_time, lasttime='2019-06-16 13:13:13', regip=ip, picture='13456', allowlogin=0, grade=0)

            user.save()
            print('加入数据库')
            session['username'] = username
            return redirect(url_for('bbs.index'))
    return render_template('reg.html',  **{
        'category': big_section,
        'all_big_sections': all_big_sections,
        'web_info': web_info
    })


@bbs.route('/addc/<int:cid>', methods=['GET', 'POST'])
def addc(cid):
    author_name = session.get('username')
    print(author_name)
    if not author_name:
        return redirect(url_for('bbs.nologin'))
    else:
        if request.method == 'POST':
            current_classid = cid
            author_id = User.query.with_entities(User.uid).filter(User.username == author_name).first()[0]
            title = request.form.get('subject')
            content = request.form.get('content')
            price = request.form.get('price')
            add_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ip = request.remote_addr
            # c初始化插入数据
            new_detail = Details(first=1, authorid=author_id, title=title, content=content, addtime=add_time, classid=current_classid, replycount=0, hits=0, istop=0, ishot=0, elite=0, rate=price, isdel=0, isdisplay=0, addip=ip)

            new_detail.save()
            new_detail.tid = new_detail.id

            new_detail.save()

            return redirect(url_for('bbs.web_list', cid=current_classid))
        else:
            web_info = Web.query.get(1)
            current_classid = cid
            user = User.query.filter(User.username == author_name).all()[0]
            all_big_sections = Category.query.filter(Category.parentid == 0).all()
            big_section = Category.query.filter(Category.parentid == 0).all()
            current_ss = Category.query.filter(Category.id == current_classid).all()[0]
            current_bs = Category.query.filter(Category.id == current_ss.parentid).all()[0]
            detail = Details.query.filter(Details.classid == cid)
            user_integral = user.grade
            user_tx = user.picture

            return render_template('addc.html', **{
                'category': big_section,
                'all_big_sections': all_big_sections,
                'current_ss': current_ss,
                'current_bs': current_bs,
                'detail': detail,
                'user_integral': user_integral,
                'user_tx': user_tx,
                'web_info':web_info
            })


@bbs.route('/verify')
def verify():
    vc = VerfiCode()
    res = vc.output()
    session['yzm'] = vc.code
    response = Response()
    response.status_code = 200
    response.headers['content-type'] = 'image/jpeg'
    response.data = res
    return response


@bbs.route('/home', methods=['GET', 'POST'])
def home():
    web_info = Web.query.get(1)
    if request.method == "POST":
        username = session.get('username')
        if not username:
            return redirect(url_for('bbs.nologin'))
        else:
            uid = User.query.with_entities(User.uid).filter(User.username == username).first()[0]

            # 利用主键uid获取当前登录用户对象
            user = User.query.get(uid)

            realname = request.form.get('realname')
            sex = int(request.form.get('sex'))
            print(sex, type(sex))
            birthyear = request.form.get('birthyear')
            birthmonth = request.form.get('birthmonth')
            birthday = request.form.get('birthday')
            user_birthday = birthyear + '.' + birthmonth + '.' + birthday
            place = request.form.get('place')
            qq = request.form.get('qq')

            user.realname = realname
            user.sex = sex
            user.birthday = user_birthday
            user.place = place
            user.qq = qq
            user.save()
            return redirect(url_for('bbs.index'))
    else:
        all_big_sections = Category.query.filter(Category.parentid == 0).all()
        small_sections = Category.query.filter(Category.parentid != 0).all()
        username = session.get('username')
        if not username:
            return redirect(url_for('bbs.nologin'))
        user = User.query.filter(User.username == username).all()[0]
        user_integral = user.grade
        user_tx = user.picture
        print('#############')
        user_qq = user.qq
        print(user_qq)
        user_group = check_userGroup(user)
        return render_template('home.html', **{
            'all_big_sections': all_big_sections,
            'small_sections': small_sections,
            'user_integral': user_integral,
            'user_tx': user_tx,
            'user_group': user_group,
            'username': username,
            'user_qq': user_qq,
            'web_info': web_info
        })


@bbs.route('/home_tx', methods=['GET', 'POST'])
def home_tx():
    web_info = Web.query.get(1)
    if request.method == "POST":
        username = session.get('username')
        if not username:
            return redirect(url_for('bbs.nologin'))
        else:
            uid = User.query.with_entities(User.uid).filter(User.username == username).first()[0]
            obj = request.files.get('pic')
            if obj:
                # obj.filename 上传文件名
                path = os.path.join(current_app.config['UPLOAD_FOLDER'], obj.filename)
                # 存入app设置的相应目录
                obj.save(path)
                user = User.query.get(uid)
                # 相对于static的路径，存入数据库
                user.picture = "index/upload/" + obj.filename
                user.save()
                return redirect(url_for('bbs.home_tx'))

    else:
        all_big_sections = Category.query.filter(Category.parentid == 0).all()
        small_sections = Category.query.filter(Category.parentid != 0).all()
        username = session.get('username')
        if not username:
            return redirect(url_for('bbs.nologin'))
        user = User.query.filter(User.username == username).all()[0]
        user_integral = user.grade
        user_tx = user.picture
        user_group = check_userGroup(user)
        return render_template('home_tx.html', **{
            'all_big_sections': all_big_sections,
            'small_sections': small_sections,
            'user_integral': user_integral,
            'user_tx': user_tx,
            'user_group': user_group,
            'username': username,
            'web_info': web_info
        })


@bbs.route('/home_qm', methods=['GET', 'POST'])
def home_qm():
    web_info = Web.query.get(1)
    if request.method == "POST":
        username = session.get('username')
        if not username:
            return redirect(url_for('bbs.nologin'))
        else:
            uid = User.query.with_entities(User.uid).filter(User.username == username).first()[0]
            print(uid)
            # 利用主键uid获取当前登录用户对象
            user = User.query.get(uid)
            content = request.form.get('content')
            user.autograph = content
            user.save()
        return render_template('home_qm.html')
    else:
        all_big_sections = Category.query.filter(Category.parentid == 0).all()
        small_sections = Category.query.filter(Category.parentid != 0).all()
        username = session.get('username')
        if not username:
            return redirect(url_for('bbs.nologin'))
        user = User.query.filter(User.username == username).all()[0]
        user_integral = user.grade
        user_tx = user.picture
        user_group = check_userGroup(user)
        return render_template('home_qm.html', **{
            'all_big_sections': all_big_sections,
            'small_sections': small_sections,
            'user_integral': user_integral,
            'user_tx': user_tx,
            'user_group': user_group,
            'username': username,
            'web_info': web_info
        })


@bbs.route('/home_pass', methods=['GET', 'POST'])
def home_pass():
    web_info = Web.query.get(1)
    if request.method == "POST":
        username = session.get('username')
        if not username:
            return redirect(url_for('bbs.nologin'))
        else:
            uid = User.query.with_entities(User.uid).filter(User.username == username).first()[0]
            # 利用主键uid获取当前登录用户对象
            user = User.query.get(uid)
            db_password = User.query.with_entities(User.password).filter(User.username == username).all()
            oldpassword = request.form.get('oldpassword')
            oldpassword = hashlib.sha1(oldpassword.encode('utf8')).hexdigest()

            if oldpassword == db_password[0][0]:
                newpassword = request.form.get('newpassword')
                checkpassword = request.form.get('newpassword2')
                if newpassword == checkpassword:
                    newpassword = hashlib.sha1(newpassword.encode('utf8')).hexdigest()
                    user.password = newpassword
                    user.save()
                    print('1')
                    return redirect(url_for('bbs.index'))
                else:
                    print('2')
                    return redirect(url_for('bbs.home_pass'))
            else:
                print('3')
                return redirect(url_for('bbs.home_pass'))
    else:
        all_big_sections = Category.query.filter(Category.parentid == 0).all()
        small_sections = Category.query.filter(Category.parentid != 0).all()
        username = session.get('username')
        user = User.query.filter(User.username == username).all()[0]
        user_integral = user.grade
        user_tx = user.picture
        user_group = check_userGroup(user)
        return render_template('home_pass.html', **{
            'all_big_sections': all_big_sections,
            'small_sections': small_sections,
            'user_integral': user_integral,
            'user_tx': user_tx,
            'user_group': user_group,
            'username': username,
            'web_info': web_info
        })


