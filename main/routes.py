from main import app
from flask import render_template, redirect, url_for, flash
from main.models import Item, User
from main.forms import RegisterForm, LoginForm
from main import db
from flask_login import login_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def homepage():
    return render_template('home.html')

@app.route('/market')
@login_required
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)

@app.route('/register', methods=['POST', 'GET'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email=form.email.data, password=form.password1.data)
        
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! You are now logged in as {user_to_create.username}', category='success')

        return redirect(url_for('market_page'))
    
    if form.errors != {}: 
        for err_msg in form.errors.values():
            flash(err_msg, category='danger')    

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempting_user = User.query.filter_by(username=form.username.data).first()

        if attempting_user and attempting_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempting_user)
            flash(f'Success! You are logged in as: {attempting_user.username}', category='success')
            
            return redirect(url_for('market_page'))
        else:
            flash('Invalid credentials! Please try again', category='danger')



    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()

    flash('You have been logged out!', category='info')
    return redirect(url_for('homepage'))