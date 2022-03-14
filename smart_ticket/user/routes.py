from flask import Blueprint, render_template, redirect, render_template, request, flash, session, url_for
from smart_ticket import app, db
from smart_ticket.user.forms import RegisterForm
from smart_ticket.models import User

user_blueprint = Blueprint('user_blueprint', __name__)


@user_blueprint.route('/register', methods=['GET','POST'])
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
        #return redirect()

    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(f'There was an error in User creation: {err_msg[0]}', category='danger')

    return render_template('registration.html', form=form)