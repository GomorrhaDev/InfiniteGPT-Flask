from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Students
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Students.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in succesfull', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('False password, try again', category='error')
        else:
            flash('This email does not exist', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        klasse = request.form.get("klasse")
        user = Students.query.filter_by(email=email).first()

        if user:
            flash('This email has already been registered', category='error')
        elif password1 != password2:
            flash('The passwords do not match', category='error')
        elif len(password1) < 6:
            flash("Your password must be at least 6 characters long", category='error')
        else:
            new_user = Students(klasse = klasse, email=email, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
