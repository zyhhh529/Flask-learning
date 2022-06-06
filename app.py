import os
import click
from flask import Flask, escape, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

# 连接数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/testing'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# 创建数据库模型（表）
class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字

class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

# 创建自定义命令，在命令行中用 flask forge 调用
@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 全局的两个变量移动到这个函数内
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

# 404错误处理函数
@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    user = User.query.first()
    return render_template('404.html', user=user), 404  # 返回模板和状态码

# 给函数注册对应的URL
# hello函数是'/' 和 '/hello'的注册时间函数，当这两个URL被访问时，执行hello函数，并将hello函数返回值返回给浏览器
@app.route('/')
def index():
    # 将变量传入模板并渲染
    # user = User.query.first() 使用了上下文处理函数就不再需要这里再取一次user了
    movies = Movie.query.all()
    return render_template('index.html', movies = movies) # 这里也不需要再传入user了，模板中可以直接调用

@app.route('/hello')
def hello():
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'

# 可以在URL中加入形参，接收URL传入的参数，可以用converter指定参数类型：<int:var_name>
@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % escape(name) # 使用escape 防止用户恶意输入

@app.route('/test')
def test():
    # url_for 第一个参数是函数名称，后面的参数对应着URL中的变量，再多出来的变量全都作为请求参数
    print(url_for('hello')) # /hello
    print(url_for('user_page', name='Sam')) # /user/Sam
    print(url_for('hello', name='Sam')) # /hello?name=Sam
    return 'Test page, see terminal'