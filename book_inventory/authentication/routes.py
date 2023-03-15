from flask import Blueprint, render_template, request, redirect, url_for, flash
from book_inventory.models import User, check_password_hash
from book_inventory.forms import UserLoginForm
from sqlalchemy import select
from flask_login import login_user, logout_user, current_user, login_required
from book_inventory.database import db_session, engine

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data 
            password = form.password.data
            user = User(email, password = password)
            db_session.add(user)
            db_session.commit()

            flash(f'A user account for {email} has been created successfully', 'user-created')

            return redirect(url_for('site.home'))

    except:
        raise Exception("That didn't work. Please try again.")

    return render_template('signup.html', form = form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            form_email = form.email.data
            password = form.password.data
            stmt = select(User).where(User.email == form_email)
            with engine.connect() as conn:
                user = conn.execute(stmt).first()
                print(user)
                if check_password_hash(user[2], password):
                    # login_user(User(row))
                    login_user(User().user)
                    flash('You were successfully logged in', 'auth-success')
                    # next = request.args.get('next')
                    # if not is_safe_url(next):
                    #     return abort(400)
                    return redirect(url_for('site.home'))
                else:
                    flash('Your email and/or Password is incorrect', 'auth-failed')
                    return redirect(url_for('auth.signin'))
    except:
        raise Exception("That didn't work. Please try again.")

    return render_template('signin.html', form = form)
# def signin():
#     form = UserLoginForm()
#     try:
#         if request.method == 'POST' and form.validate_on_submit():
#             email = form.email.data
#             password = form.password.data
#             print(email, password)
#             stmt = select(User).where(User.email == email)
#             # logged_user = User.query.filter(User.email == email).first()
#             logged_user = db_session.execute(stmt).first()

#             if logged_user and check_password_hash(logged_user.password, password):
#                 login_user(logged_user)
#                 flash('You were successfully logged in', 'auth-success')
#                 return redirect(url_for('site.home'))
#             else:
#                 flash('Your email and/or Password is incorrect', 'auth-failed')
#                 return redirect(url_for('auth.signin'))
#     except:
#         raise Exception("That didn't work. Please try again.")

#     return render_template('signin.html', form = form)

@auth.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('site.home'))