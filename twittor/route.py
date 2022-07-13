from flask import render_template

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
    return render_template("login.html")