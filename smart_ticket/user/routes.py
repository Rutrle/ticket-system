from flask import Blueprint, render_template, redirect, render_template, request, flash, session, url_for
from smart_ticket import app, db
from smart_ticket.user.forms import RegisterForm, LoginForm
from smart_ticket.models import User
from flask_login import login_user, logout_user, login_required

user_bp = Blueprint('user_bp', __name__, template_folder='templates')


@user_bp.route('/register', methods=['GET','POST'])
def registration_page():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(
            username = form.username.data,
            email=form.email.data,
            password = form.password1.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash(f'Your account was succesfully created, you can login now.', category='success')
        return redirect(url_for('user_bp.login_page'))

    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(f'There was an error in User creation: {err_msg[0]}', category='danger')

    return render_template('user_bp/registration.html', form=form)

@user_bp.route('/login', methods=['GET','POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.check_attempted_password(form.password.data):
                login_user(user)
                flash("You have succesfully logged in!", category='success')
                return redirect(url_for('home_page'))   ###### temporary, needs to change!
        
        flash('Wrong Username or password! Please try again.', category='danger')

    return render_template('user_bp/login.html', form=form)


@user_bp.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash('You have logged out. Thanks for visiting!', category='info')
    return redirect(url_for('home_page'))

@user_bp.route('/detail/<int:id>')
@login_required
def user_detail_page(id:int):
    user = User.query.get_or_404(id)

    return render_template('user_bp/user_detail.html', user=user)