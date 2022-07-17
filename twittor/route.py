from flask import render_template, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required

from twittor.forms import LoginForm ,RegisterForm
from twittor.models import User, Tweet
from twittor.ext import db

@login_required
def index():
    rows = [
        {"name": "Python","age":27},
        {"name": "Python","age":27},
        {"name": "Python","age":27},
        {"name": "Python", "age": 27},
        {"name": "Python", "age": 27},
        {"name": "Python", "age": 27},
    ]
    posts = [
        {
            "author":{"username": "root"},
            "body": "hi I'm root!"
        },
        {
            "author":{"username": "test"},
            "body": "hi I'm test!"
        }
    ]
    return render_template("index.html", rows=rows, posts=posts)

def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            username = User.query.filter_by(username = form.username.data).first()

            if username is None or username.check_password(form.password.data):
                print("invalid username or password!")
                # error = "invalid username or password!"
                return redirect(url_for("login"))
            
            login_user(username, remember=form.rememberMe.data)
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            msg = f"username = {form.username.data}, password = {form.password.data}, rememberMe = {form.rememberMe.data}"
            print(msg)
        
        return render_template("login.html", title="Login In", form=form)

def logout():
    logout_user()
    return redirect(url_for("login"))

def register():
    print("re123")
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegisterForm()

    print(f"re: {form.validate_on_submit()}")
    if form.validate_on_submit():
        print("re456")
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        # db.session.add(user)
        # db.session.commit()
        return redirect(url_for("login"))
    
    return render_template("register.html",title="Registration", form=form)
