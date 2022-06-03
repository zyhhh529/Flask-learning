from flask import Flask, escape, url_for
app = Flask(__name__)

# hello函数是'/' 和 '/hello'的注册时间函数，当这两个URL被访问时，执行hello函数，并将hello函数返回值返回给浏览器
@app.route('/') 
@app.route('/hello')
def hello():
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'

@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % escape(name)

@app.route('/test')
def test():
    print(url_for('hello')) # /hello
    print(url_for('user_page', name='Sam')) # /user/Sam
    print(url_for('hello', name='Sam')) # /hello?name=Sam
    return 'Test page, see terminal'