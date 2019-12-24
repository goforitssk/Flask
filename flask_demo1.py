# 1、导入flask扩展，模板，
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from flask import request  # 获取参数
from flask_cors import CORS

# 定义表单类
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# 导入文件下载所需要的模块
from flask import send_file, send_from_directory
import os


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')
# 2、创建flask应用程序实例
# 需要传入__name__，作用是确定资源所在的路径
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'  # 必填字段
bootstrap = Bootstrap(app)


server = Flask(__name__)  # 创建一个flask对象
CORS(server)


# 这是一个简单的前后端交互实例
# @server.route('/login', methods=['get', 'post'])
# def login():
#     username = request.values.get('username') # 获取参数
#     password = request.values.get('password')
#     if username and password:
#         # sql = 'select User from user where User="%s"'%username
#         # data = conn_mysql(sql)
#             return '{msg:"无数据"}'


# 服务器端文件上传的编写
@server.route("/upload", methods=["POST"])
def upload():
    file_obj = request.files.get("file")  # "file"对应前端表单name属性
    if file_obj is None:
        # 表示没有发送文件
        return "未上传文件"
    file_obj.save("./upload.txt")
    return "上传成功"

    # 将文件保存到本地
    # # 1. 创建一个文件
    # f = open("./demo.png", "wb")
    # # 2. 向文件写内容
    # data = file_obj.read()
    # f.write(data)
    # # 3. 关闭文件
    # f.close()
    # 直接使用上传的文件对象保存


# 服务器端文件下载的编写
@server.route("/download/<filename>", methods=['GET'])
def download(filename):
    directory = os.getcwd()
    return send_from_directory(directory, filename, as_attachment=True)


# 3、定义路由及视图函数
# flask中定义路由是通过装饰器实现的
@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''    # 把文本框中的内容清空
    return render_template('index.html', form=form, name=name)


@app.errorhandler(404)
def page_not_found(e):  # 注意事件e
    return render_template('404.html'), 404


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

# 4、启动程序
if __name__ == '__main__':
    # 执行了app.run，就会将flask程序运行在一个简易的服务器（由flask提供，用于调试）
    server.run()
