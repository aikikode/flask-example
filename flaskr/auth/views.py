import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr import db
from flaskr.models import User

blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@blueprint.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username and password:
            db.session.add(User(username=username, password=generate_password_hash(password)))
            db.session.commit()
            return redirect(url_for("auth.login"))
        flash('Username and password are required.')
    return render_template('auth/register.html')


@blueprint.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is not None and check_password_hash(user.password, password):
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))
        flash('Incorrect username/password combination')
    return render_template('auth/login.html')


@blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.views.login'))
        return view(**kwargs)
    return wrapped_view


@blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()
