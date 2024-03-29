from flask import render_template, redirect, url_for, request, abort, current_app, flash
from flask_login import login_user, current_user, logout_user, login_required

from twittor.forms import LoginForm, RegisterForm, EditProfileForm, TweetForm, PasswordResetRequestForm, PasswordResetForm
from twittor.models.user import User
from twittor.models.tweet import Tweet
from .models.ext import db

from twittor.email import send_email

@login_required
def index():
    tweet_form = TweetForm()
    if tweet_form.validate_on_submit():
        tweet = Tweet(body=tweet_form.tweet.data, author=current_user)
        db.session.add(tweet)
        db.session.commit()
        
        return redirect(url_for("index"))

    tweets = current_user.own_and_followed_tweets()
    page_num = int(request.args.get("page") or 1)
    tweets = tweets.paginate(page=page_num, per_page=current_app.config["TWEET_PER_PAGE"], error_out=False)
    next_url = url_for("index", page=tweets.next_num) if tweets.has_next else None
    prev_url = url_for("index", page=tweets.prev_num) if tweets.has_prev else None
    
    return render_template(
        "index.html", tweets=tweets.items, tweet_form=tweet_form, next_url=next_url, prev_url=prev_url
        )

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
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    
    register_form = RegisterForm()
    
    if register_form.validate_on_submit():
        user = User(username=register_form.username.data,email=register_form.email.data)
        user.set_password(register_form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    
    msg = f"username = {register_form.username.data}, password = {register_form.password.data}, email = {register_form.email.data}"
    print(msg)
    
    return render_template("register.html", title="Registration", form=register_form)

@login_required # 必須登入
def user_view(username): # 點選user profile回傳的username
    user = User.query.filter_by(username=username).first() 
    if user is None:
        abort(404)
        
    # tweets = Tweet.query.filter_by(author = user)
    page_num = int(request.args.get('page') or 1)
    tweets = user.tweets.order_by(Tweet.create_date.desc()).paginate(
        page=page_num, 
        per_page=current_app.config["TWEET_PER_PAGE"], 
        error_out=False)
    
    next_url = url_for(
        "profile", page=tweets.next_num, username=username) if tweets.has_next else None
    prev_url = url_for(
        "profile", page=tweets.prev_num, username=username) if tweets.has_prev else None
    
    print(tweets)
    if request.method == "POST":
        if request.form["request_botton"] == "Follow": # request.form 取得點擊按鈕的{name:value}
            current_user.follow(user)
            db.session.commit()
        else:
            current_user.unfollow(user)
            db.session.commit()
            
    return render_template("user.html", title="Profile", tweets=tweets.items, user=user, prev_url=prev_url, next_url=next_url)

def page_not_found(error):
    return render_template("404.html"), 404

@login_required
def edit_profile():
    edit_profile_form = EditProfileForm()
    
    if request.method == "GET":
        edit_profile_form.about_me.data = current_user.about_me
    elif request.method == "POST":
        current_user.about_me = edit_profile_form.about_me.data
        db.session.commit()
        
        return redirect(url_for("profile", username=current_user.username))
    return render_template("edit_profile.html",form=edit_profile_form)

def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash(
                """
                You should soon receive an email allowing you to reset your password.
                Please make sure to check your spam and trash if you can't find the email.
                """
                )
            
            token = user.get_jwt_token()
            url_password_reset = url_for("password_reset", token=token, _external=True)
            url_password_request = url_for("reset_password_request",_external=True) 

            
            url_password_reset = url_for(
                "password_reset",
                token = token, 
                _external = True
            )
            
            url_password_reset_request = url_for(
                "reset_password_request",
                _external = True
            )

            send_email(
                subject=current_app.config["MAIL_SUBJECT_RESET_PASSWORD"],
                recipients=[user.email],
                text_body=render_template(
                    "email/passwd_reset.txt",
                    url_password_reset=url_password_reset,
                    url_password_reset_request=url_password_reset_request
                ),
                html_body=render_template(
                    "email/passwd_reset.html",
                    url_password_reset_request=url_password_reset_request,
                    url_password_reset=url_password_reset,
                ),
            )

            
            return redirect(url_for('login'))
    return render_template("password_reset_request.html",form=form)

def password_reset(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    print(token)
    user = User.verify_jwt_token(token)
    print(user)
    
    if not user:
        return redirect(url_for('login'))
    form = PasswordResetForm()
    
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template('password_reset.html', title="Password Reset", form=form)