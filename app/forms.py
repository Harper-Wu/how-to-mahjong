from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo, InputRequired
from app.models import User, Quiz


class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(),
                                        Length(min=2, max=32)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(),
                                                EqualTo('password')])
    submit = SubmitField('Sign Up')

    # validate_<field_name> to build custom validators
    # validate username and email exists or not
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField('Sign In')

class QuizForm(FlaskForm):
    quizs = Quiz.query.all()
    data = []
    for k, quiz in enumerate(quizs):
        dic = {
            "id": quiz.id,
            "question": quiz.question,
            "optionA": quiz.optionA,
            "optionB": quiz.optionB,
            "optionC": quiz.optionC,
            "optionD": quiz.optionD,
            "img":quiz.img
        }
        data.append(dic)
    # question = RadioField()
    submit = SubmitField()