from flask import Flask, escape, url_for, render_template
app = Flask(__name__)

name = 'Sam'
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

# 给函数注册对应的URL
# hello函数是'/' 和 '/hello'的注册时间函数，当这两个URL被访问时，执行hello函数，并将hello函数返回值返回给浏览器
@app.route('/')
def index():
    # 将变量传入模板并渲染
    return render_template('index.html', name = name, movies = movies)

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