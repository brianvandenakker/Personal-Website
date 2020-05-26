from flask import Blueprint, render_template, session, redirect, request, url_for, flash
from portfolio.extensions import db
from portfolio.models import User
from portfolio.user.forms import LoginForm
from flask_login import login_required
from flask_login import UserMixin, login_user, login_required, logout_user

user_blueprint = Blueprint('user', __name__, template_folder = 'templates/user')

#LOGIN
@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user.check_password(form.password.data) and user is not none:
            login_user(user)
            flash('Successful Login')
            return redirect('index')
    return render_template('login.html', form=form)


#LOGOUT
@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've logged out")
    return redirect(url_for('index'))
