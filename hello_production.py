from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html', current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name)


@app.route('/comments')
def comment():
	comments = ['a', 'b', 'c']
	return render_template('comment.html', comments=comments)


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500


if __name__ == '__main__':
	bootstrap = Bootstrap(app)
	moment = Moment(app)
	app.run(host='0.0.0.0', port='5000', debug=True)
