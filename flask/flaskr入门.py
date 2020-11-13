from flask import Flask, url_for, redirect, request


app = Flask(__name__)

@app.route('/')
def test_1():
    return 'this is my first flask'

@app.route('/test/<user>') #url传递参数
def test_u(user):
    return user

@app.route('/test_url') #url反转url
def test_url():
    return url_for('test_url', page = 1, _external = True)

def test_add_url(): #另一种路由方式
    return 'another url'
app.add_url_rule('/test_add_url', view_func = test_add_url)

@app.route('/test_redirect')
def test_redirect():
    url = url_for('test_url')
    return redirect(url)

@app.route('/test_args', methods = ['GET', 'POST'])
def transfer_args():
    if request.method == 'GET':
        data = request.args.get('username')
    if request.method == 'POST':
        data = request.form['username']
        # data = request.get_data()
    print(data)
    return data

if __name__ == '__main__':
    app.run(debug=False)