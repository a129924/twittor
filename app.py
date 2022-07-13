from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
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

if __name__ == '__main__':
    app.run(debug=True, port=8080)