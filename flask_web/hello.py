from flask import Flask, make_response, abort, render_template, session, redirect, url_for, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime


from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')



app = Flask(__name__)
app.config['SECRET_KEY'] = 'HARD TO GUESS STRING'
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    # # 例子 response
    # response = make_response('<h1>这里将会设置一个cookie')
    # response.set_cookie('answer', '42')
    # return response

    # # 例子 render_template
    # return render_template('index.html', current_time=datetime.utcnow())

    # name = None
    # form = NameForm()
    # if form.validate_on_submit():
    #     name = form.name.data
    #     form.name.data = ''
    # return render_template('index.html', form=form, name=name)

    # 前一个版本，局部变量name被用于存储用户在表单中输入的名字。这个变量现在保存在session中，所以在两次请求之间也能记住输入的值。
    # form = NameForm()
    # if form.validate_on_submit():
    #     session['name'] = form.name.data
    #     return redirect(url_for('index'))
    # return render_template('index.html', form=form, name=session.get('name'))

    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


@app.route('/user/<name>')
def user(name):
    # return '<h1>Hello World,%s</h1>' % name
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_sever_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    manager.run()
