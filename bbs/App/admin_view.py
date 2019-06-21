import hashlib

from flask import Blueprint, render_template, request, session, Response, redirect, url_for, current_app
from sqlalchemy import func
from App.model import Category, Link, User, Details, Web
from ext import db

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.before_request
def is_login():
    if request.path.rstrip('/') == '/admin':
        return
    elif not session.get('username'):
        return redirect('/admin/')


@admin.route('/', methods=["GET", "POST"])
# @admin.route('/index', methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template('admin.html')

    else:

        admin_username = request.form.get('admin_username')

        # 查询用户名是否在数据库中
        db_username = User.query.filter(User.username == admin_username).all()

        if not db_username:
            return redirect(url_for('bbs.index'))

        # 查询用户类型是否为管理员
        user_type = User.query.with_entities(User.udertype).filter(User.username == admin_username).first()[0]
        if user_type != 1:
            return redirect(url_for('bbs.index'))

        # 判断密码
        admin_password = request.form.get('admin_password')
        admin_password = hashlib.sha1(admin_password.encode('utf8')).hexdigest()
        db_password = User.query.with_entities(User.password).filter(User.username == admin_username).all()
        if not admin_password == db_password[0][0]:
            return render_template('admin.html')

        # admin_questionid = request.form.get('admin_questionid')
        # admin_answer = request.form.get('admin_answer')
        session['username'] = admin_username
        return redirect(url_for('admin.to_main'))


@admin.route('/index', methods=["GET", "POST"])
def to_main():
    username = session.get('username')

    return render_template('admin_index.html', **{
        'username': username
    })


@admin.route('/link', methods=["GET", "POST"])
def link():
    links = Link.query.order_by(Link.displayorder).all()
    ords = Link.query.with_entities(Link.displayorder).all()

    print(ords)
    if request.method == 'GET':
        return render_template('admin_link.html', **{
            'links': links
        })
    else:

        # 被删除链接的lid
        dellinks_lid = request.form.getlist('delete')
        if dellinks_lid:
            for delink_lid in dellinks_lid:
                delink = Link.query.get(int(delink_lid))
                delink.delete()
        # 排序方法
        # orders = request.form.getlist('displayorder')
        # if orders:
        #     print('################')
        #     print(orders,type(orders))
        #     for order in orders:
        #         order = Link.query.get(int(order))
        #         print(order)
        #         order.save()

        return redirect('/admin/link')


@admin.route('/lockip')
def lockip():
    return render_template('admin_lock_ip.html')


@admin.route('/addcategory', methods=["GET", "POST"])
def addcategory():
    if request.method == 'GET':
        return render_template('admin_category_add.html')
    else:
        classname = request.form.get('classname')

        parentid = request.form.get('parentid')
        # 获取新板块对象
        new_category = Category()
        new_category.classname = classname
        new_category.parentid = parentid
        new_category.save()
        new_category.orderby = new_category.id
        new_category.save()
        return redirect(url_for('admin.category'))


@admin.route('/reply', methods=["GET", "POST"])
def reply():
    if request.method == 'GET':
        reply_count = Details.query.with_entities(func.count(Details.first)).filter(Details.first == 0 and Details.isdisplay == 0).group_by(Details.first).all()
        replys = db.session.execute("select d.id,d.content,u.username,d.tid,d.classid,c.classname,d.addtime from bbs_details as d join bbs_category as c on d.classid=c.id join bbs_user as u on d.authorid=u.uid where first=0 and isdisplay=0").fetchall()

        return render_template('admin_detail_hf.html', **{
            'reply_count': reply_count,
            'replys': replys
        })
    else:
        tidarray = request.form.getlist('tidarray')
        for i in tidarray:
            del_reply = Details.query.get(int(i))
            del_reply.isdisplay = 1
            del_reply.save()
        return redirect(url_for('admin.reply'))


@admin.route('/recyle',  methods=["GET", "POST"])
def recyle():
    if request.method == 'GET':
        reply_count = Details.query.with_entities(func.count(Details.first)).filter(Details.first == 0 and Details.isdisplay == 1).group_by(Details.first).all()
        replys = db.session.execute("select d.id,d.content,u.username,d.tid,d.classid,c.classname,d.addtime from bbs_details as d join bbs_category as c on d.classid=c.id join bbs_user as u on d.authorid=u.uid where first=0 and isdisplay=1").fetchall()

        return render_template('admin_detail_hf_del.html', **{
            'reply_count': reply_count,
            'replys': replys
        })
    else:
        # 获取到勾选框中帖子回复的id
        tidarray = request.form.getlist('tidarray')
        print(tidarray)

        delsubmit = request.form.get('delsubmit')

        if delsubmit:
            for i in tidarray:
                del_reply = Details.query.get(int(i))
                del_reply.delete()

        undelsubmit = request.form.get('undelsubmit')

        if undelsubmit:
            for j in tidarray:
                del_detail = Details.query.get(int(j))
                del_detail.isdisplay = 0
                del_detail.save()
        return redirect(url_for('admin.recyle'))


@admin.route("/adminstrate")
def adminstrate():
    return "adminstrate"


@admin.route('/logout')
def logout():
    session.pop('username')
    return redirect('/admin')


@admin.route('/dolink')
def dolink():
    return '退出登录'


@admin.route('/member', methods=["GET", "POST"])
@admin.route('/member/<int:uid>/<int:value>', methods=["GET", "POST"])
def member(uid=None, value=None):
    if request.method == 'GET':
        users_count = User.query.with_entities(func.count(User.username)).filter(User.udertype == 0).scalar()
        users_info = User.query.all()
    # 当前操作用户
        if uid:
            user = User.query.get(uid)
            if value == 1:
                user.allowlogin = 1
                user.save()
            else:
                user.allowlogin = 0
                user.save()
        return render_template('admin_member.html', **{
            'users_count': users_count,
            'users_info': users_info
        })
    else:
        uidarray = request.form.getlist('uidarray')
        print(uidarray)
        for i in uidarray:
            deluser = User.query.get(int(i))
            deluser.delete()
        return redirect(url_for('admin.member'))


@admin.route('/member_show/<int:uid>', methods=["GET", "POST"])
def member_show(uid):
    user = User.query.filter(User.uid == uid).all()[0]
    if request.method == 'GET':
        return render_template('admin_member_show.html', **{
            'user': user
        })
    else:
        # 得到奖惩积分数值，正数为+，负数为-
        rpgrade = int(request.form.get('grade'))
        if rpgrade >= 0:
            user.grade += rpgrade
            user.save()
        else:
            user.grade -= rpgrade
            user.save()


@admin.route('/category', methods=["GET", "POST"])
def category():
    big_sections = Category.query.filter(Category.parentid == 0).order_by(Category.orderby).all()
    small_sections = Category.query.filter(Category.parentid != 0).order_by(Category.orderby).all()
    if request.method == 'GET':

        return render_template('admin_category.html', **{
            'big_sections': big_sections,
            'small_sections': small_sections
        })
    else:

        for name in request.form:

            record = request.form.getlist(name)

            for big_section in big_sections:
                if int(record[0]) == big_section.id:

                    big_section.classname = record[2]
                    big_section.orderby = record[1]
                    big_section.save()
                    break
            for small_section in small_sections:
                if int(record[0]) == small_section.id:
                    small_section.orderby = record[1]
                    small_section.classname = record[2]
                    small_section.compere = record[3]
                    small_section.save()
                    break

        return redirect(url_for("admin.category"))


@admin.route('detail', methods=["GET", "POST"])
def detail():
    if request.method == 'GET':
        detail_count = Details.query.with_entities(func.count(Details.first)).filter(Details.first == 1 and Details.isdel == 0).group_by(
            Details.first).all()
        details = db.session.execute("select d.id,d.title,u.username,d.classid,c.classname,d.replycount,d.hits,d.addtime from bbs_details as d join bbs_category as c on d.classid=c.id join bbs_user as u on d.authorid=u.uid where first=1 and isdel=0").fetchall()

        return render_template('admin_detail.html', **{
            'detail_count': detail_count,
            'details': details
        })
    else:
        tidarray = request.form.getlist('tidarray')
        for i in tidarray:
            del_detail = Details.query.get(int(i))
            del_detail.isdel =1
            del_detail.save()
            return redirect(url_for('admin.detail'))


@admin.route('/deletepost', methods=["GET", "POST"])
def deletepost():
    if request.method == 'GET':
        detail_count = Details.query.with_entities(func.count(Details.first)).filter(
            Details.first == 1 and Details.isdel == 1).group_by(
            Details.first).all()
        details = db.session.execute("select d.id,d.title,u.username,d.classid,c.classname,d.replycount,d.hits,d.addtime from bbs_details as d join bbs_category as c on d.classid=c.id join bbs_user as u on d.authorid=u.uid where first=1 and isdel=1").fetchall()

        return render_template('admin_detail_del.html', **{
            'detail_count': detail_count,
            'details': details
        })

    else:
        tid = request.form.getlist('tid')

        operate1 = request.form.get('operate1')
        if operate1:
            for i in tid:
                del_detail = Details.query.get(int(i))
                del_detail.delete()

        operate2 = request.form.get('operate2')
        if operate2:
            for j in tid:
                del_detail = Details.query.get(int(j))
                del_detail.isdel = 0
                del_detail.save()
        return redirect(url_for('admin.detail'))


@admin.route('main', methods=["GET", "POST"])
def main():
    web = Web.query.get(1)
    if request.method == 'GET':

        return render_template('admin_main.html', **{
            'web_info': web
        })
    else:
        web.sitename = request.form.get('WEB_NAME')
        web.webname = request.form.get('WEB_BTM')
        web.url = request.form.get('WEB_URL')
        web.webcode = request.form.get('WEB_ICP')
        web.status = request.form.get('WEB_ISCLOSE')
        web.save()
        return render_template('admin_main.html', **{
            'web_info': web
        })


