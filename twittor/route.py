from flask import render_template, redirect, url_for, request, abort
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
        login_form = LoginForm()
        if login_form.validate_on_submit():
            username = User.query.filter_by(username=login_form.username.data).first()

            if username is None or username.check_password(login_form.password.data):
                print("invalid username or password!")
                # error = "invalid username or password!"
                return redirect(url_for("login"))
            
            login_user(username, remember=login_form.rememberMe.data)
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            msg = f"username = {login_form.username.data}, password = {login_form.password.data}, rememberMe = {login_form.rememberMe.data}"
            print(msg)
        
        return render_template("login.html", title="Login In", form=login_form)

def logout():
    logout_user()
    return redirect(url_for("login"))

def register():
    print("re123")
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    register_form = RegisterForm()

    print(f"re: {register_form.validate_on_submit()}")
    
    if register_form.validate_on_submit():
        print("re456")
        user = User(username=register_form.username.data,email=register_form.email.data)
        user.set_password(register_form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    
    msg = f"username = {register_form.username.data}, password = {register_form.password.data}, email = {register_form.email.data}"
    print(msg)
    
    return render_template("register.html", title="Registration", form=register_form)

@login_required # 必須登入
def user_view(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
        
    posts = [
        {
            "author": {"username": user.username},
            "body": f"hi I'm {user.username}!"
        },
        {
            "author": {"username": user.username},
            "body": f"hi I'm {user.username}!"
        }
    ]

    return render_template("user.html",title="Profile",posts=posts,user=user)

def page_not_found(error):
    return render_template("404.html"), 404
