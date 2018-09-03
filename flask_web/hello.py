from flask import Flask, make_response, abort, render_template, session, redirect, url_for, flash
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate, MigrateCommand


from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')



basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'HARD TO GUESS STRING'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/'+os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/data'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
bootstrap = Bootstrap(app)
moment = Moment(app)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __trepr__(self):
        return '<Role%r' % self.name

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.INTEGER, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.INTEGER, db.ForeignKey('roles.id'))

    def __repr__(self):
        return 'User%r' % self.username



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

    # form = NameForm()
    # if form.validate_on_submit():
    #     old_name = session.get('name')
    #     if old_name is not None and old_name != form.name.data:
    #         flash('Looks like you have changed your name!')
    #     session['name'] = form.name.data
    #     return redirect(url_for('index'))
    # return render_template('index.html', form=form, name=session.get('name'))



    # 在这个修改后的版本中，提交表单后，程序会使用查询过滤器在数据库中查找提交的名字。
    # 变量known被写入用户会话中，因此重定向之后，可以把数据传给模板，用来显示自定义的欢迎消息。
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
        form = form, name=session.get('name'),
        known = session.get('known', False))


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
