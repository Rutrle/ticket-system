from flask import Blueprint, Response, redirect, render_template, flash, url_for
from smart_ticket import db
from werkzeug.datastructures import FileStorage
import smart_ticket
from smart_ticket.user_bp.forms import RegisterForm, LoginForm, UserContactsUpdateForm, UserProfilePictureForm, UserPasswordUpdateForm, PasswordResetForm
from smart_ticket.models import User, UserRole
from smart_ticket.email.send_email import send_registration_email, send_password_reset_email
from flask_login import current_user, login_user, logout_user, login_required
import secrets
import os
from PIL import Image


user_bp = Blueprint('user_bp', __name__, template_folder='templates')


@user_bp.route('/register', methods=['GET', 'POST'])
def registration_page() -> Response:
    """
    page for user registration
    """
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password1.data,
            user_role=db.session.query(UserRole).filter_by(name="user").first()
        )
        db.session.add(new_user)
        db.session.commit()
        send_registration_email(new_user.email, new_user.username)
        flash(f'Your account was succesfully created, you can login now.', category='success')
        return redirect(url_for('user_bp.login_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error in User creation: {err_msg[0]}', category='danger')

    return render_template('user_bp/registration.html', form=form)


@user_bp.route('/login', methods=['GET', 'POST'])
def login_page() -> Response:
    """
    page for logging in users 
    """
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.check_attempted_password(form.password.data):
                if user.is_active == True:

                    login_user(user)
                    flash("You have succesfully logged in!", category='success')

                    return redirect(url_for('user_bp.landing_page'))

        flash('Wrong Username or password! Please try again.', category='danger')

    return render_template('user_bp/login.html', form=form)


@user_bp.route('/logout')
@login_required
def logout_page() -> Response:
    """
    route for logging out user and redirecting them to home page
    """
    logout_user()
    flash('You have logged out. Thanks for visiting!', category='info')
    return redirect(url_for('home_page'))


@user_bp.route('/detail/<int:id>')
@login_required
def user_detail_page(id: int) -> Response:
    """
    page for showing info about user with given 'id'
    """
    user = User.query.get_or_404(id)
    profile_picture_path = url_for(
        'static', filename=f"images/profile_pictures/{current_user.profile_picture_file}")
    return render_template('user_bp/user_detail.html', user=user, profile_picture_path=profile_picture_path)


@user_bp.route('/landing')
@login_required
def landing_page() -> Response:
    """
    Landing page to which are users redirected after login containing tickets that the user i currently solving or are on his watchlist
    """
    user = current_user
    return render_template('user_bp/landing.html', user=user)


@user_bp.route('/update')
@login_required
def update_account_settings_page() -> Response:
    """
    page for displaying forms for updating user account
    POST requests from those forms is handled in different routes
    """
    forms = {
        'contacts_update_form': UserContactsUpdateForm(),
        'profile_picture_form': UserProfilePictureForm(),
        'password_update_form': UserPasswordUpdateForm()
    }

    profile_picture_path = url_for('static', filename=f"images/profile_pictures/{current_user.profile_picture_file}")

    return render_template('user_bp/update_user.html', **forms, profile_picture_path=profile_picture_path)


@user_bp.route('/update/update_user_info', methods=['POST'])
@login_required
def update_basic_account_settings() -> Response:
    '''
    route for handling post requests for changing user settings and
    then redirecting them back to update_account_settings_page
    '''
    contacts_update_form = UserContactsUpdateForm()

    if contacts_update_form.validate_on_submit():
        phone_number = contacts_update_form.phone_number.data
        phone_number = "".join(phone_number.split())
        current_user.email = contacts_update_form.email.data
        current_user.phone_number = phone_number

        db.session.add(current_user)
        db.session.commit()
        flash("Your contact details were succesfully updated", category="success")

    elif contacts_update_form.errors != {}:
        for err_msg in contacts_update_form.errors.values():
            flash(
                f'There was an error in updating your profile: {err_msg[0]}', category='danger')

    return redirect(url_for('user_bp.update_account_settings_page'))


def save_picture(form_picture: FileStorage) -> str:
    '''
    saves picture passed by WTForms form under random filename and returns the filename
    '''
    random_hex = secrets.token_hex(8)
    name, f_extension = os.path.splitext(form_picture.filename)

    picture_filename = random_hex + str(current_user.id) + f_extension
    picture_path = os.path.join(
        smart_ticket.app.root_path, 'static\images\profile_pictures', picture_filename)

    output_size = (255, 255)
    image_to_save = Image.open(form_picture)
    image_to_save.thumbnail(output_size)
    image_to_save.save(picture_path)

    return picture_filename


@user_bp.route('/update/update_profile_picture', methods=['POST'])
@login_required
def update_profile_picture() -> Response:
    """
    route for handling POST request for updating profile picture 
    and then redirecting user back to update_account_settings_page
    """
    profile_picture_form = UserProfilePictureForm()
    if profile_picture_form.validate_on_submit():
        picture_filename = save_picture(
            profile_picture_form.profile_picture.data)
        current_user.profile_picture_file = picture_filename
        db.session.add(current_user)
        db.session.commit()

        flash("Your profile pictore was succesfully changed", category="success")

    elif profile_picture_form.errors != {}:
        for err_msg in profile_picture_form.errors.values():
            flash(
                f'There was an error in updating your profile picture: {err_msg[0]}', category='danger')
    return redirect(url_for('user_bp.update_account_settings_page'))


@user_bp.route('/update/update_password', methods=['POST'])
@login_required
def update_password() -> Response:
    '''
    route for handling POST request for updating password
    and then redirecting user back to update_account_settings_page
    '''
    password_update_form = UserPasswordUpdateForm()

    if password_update_form.validate_on_submit():

        old_password = password_update_form.old_password.data
        new_password = password_update_form.password1.data

        if current_user.check_attempted_password(old_password):
            current_user.password = new_password
            db.session.add(current_user)
            db.session.commit()

            logout_user()

            flash("Your password was succesfully updated, please use it to log in",
                  category="success")
            return redirect(url_for('user_bp.login_page'))

        else:
            flash("You entered invalid old password", category='danger')

    elif password_update_form.errors != {}:
        for err_msg in password_update_form.errors.values():
            flash(
                f'There was an error in changing your password: {err_msg[0]}', category='danger')

    return redirect(url_for('user_bp.update_account_settings_page'))


@user_bp.route('/password_reset', methods=['GET', 'POST'])
def password_reset_page() -> Response:
    '''
    page for reseting password and sending it to users e-mail
    '''
    password_reset_form = PasswordResetForm()

    if password_reset_form.validate_on_submit():
        email = password_reset_form.email.data
        user = db.session.query(User).filter_by(email=email).first()

        if user:
            new_password = secrets.token_urlsafe(15)
            user.password = new_password
            send_password_reset_email(user.email, user, new_password)
            db.session.add(user)
            db.session.commit()
        #flash is here to not disclose corretness of entered email address
        flash("Password reset succesfull, e-mail with new password should arrive shortly in your e-mail box", category="success")

    elif password_reset_form.errors != {}:
        for err_msg in password_reset_form.errors.values():
            flash(
                f'There was an error in resetting your password: {err_msg[0]}', category='danger')

    return render_template("user_bp/reset_password.html", password_reset_form=password_reset_form)
