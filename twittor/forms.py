from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length

from twittor.models import User

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    rememberMe = BooleanField("Remember Me")
    submit = SubmitField("Login")
    
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_repeat = PasswordField("Password Repeat", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("please use different username")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("please use different email")

class EditProfileForm(FlaskForm):
    about_me = TextAreaField("About Me", validators=[Length(min=0, max=120)])
    submit = SubmitField("Save")
        
class TweetForm(FlaskForm):
    tweet = TextAreaField("Tweet", validators=[DataRequired(), Length(min=0, max=140)])
    submit = SubmitField("Tweet")
    
class PasswordResetRequestForm(FlaskForm):
    email = EmailField("Email Address", validators=[DataRequired(),Email()])
    submit = SubmitField("Password Reset")
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError(
                "You do not an account for this email address")
            
class PasswordResetForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    password_reset = PasswordField("Password Reset", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Submit")