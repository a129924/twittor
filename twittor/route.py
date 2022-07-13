from flask import render_template, redirect, url_for
from twittor.forms import LoginForm

def index():
    name = {"username": "John",}
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
    return render_template("index.html", name=name,rows=rows, posts=posts)

def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        msg = f"username = {form.username.data}, password = {form.password.data}, rememberMe = {form.rememberMe.data}"
        print(msg)
        return redirect(url_for("index"))
    
    return render_template("login.html", title="Login In", form=form)