import os

from flask import Flask, Response, redirect, url_for, make_response, request
from flask_script import Manager
from App.view import bbs
from App.admin_view import admin
from flask_sqlalchemy import SQLAlchemy

from ext import db,Mail

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@127.0.0.1:3306/bbs'
app.config['SECRET_KEY'] = '77777'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smmtp.qq.com'
app.config['MAIL_USERNAME'] = '815540246@qq.com'
app.config['MAIL_PASSWORD']='pxptizyonjncbcce'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static/index/upload')
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(os.getcwd(), 'static/index/upload')
# 初始化数据库实例
db.init_app(app)


manager = Manager(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


app.register_blueprint(bbs)
app.register_blueprint(admin)



if __name__ == '__main__':
    # app.run()
    manager.run()
