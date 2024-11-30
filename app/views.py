from flask import render_template, redirect, url_for, flash,session
from app import app, db, bcrypt,login_manager
from app.forms import RegisterUser, LoginUser
from app.models import User
from flask_login import login_user, login_required, current_user, logout_user




@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterUser()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'New user {form.username.data}, added successfully', 'success')
        return redirect(url_for('login'))
    else:
        if form.errors:
            print("Form errors:", form.errors)
    return render_template('register.html', form=form)

@app.route('/Login', methods=['POST', 'GET'])
def login():
    form = LoginUser()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                session['username'] = user.username
                flash('Login successfully', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Wrong password, Try again', 'danger')
        else:
            flash('That user doesnt exist', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
