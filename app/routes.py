from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.forms import RegistrationForm, LoginForm, QuizForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Quiz, History
from werkzeug.urls import url_parse

'''
@app.route decorator creates an association between 
the URL given as an argument and the function
url_for would use function name as parameter
'''
@app.route('/')
@app.route('/intro')
# Protect view funciton against anonymous users
#@login_required
def index():
    return render_template('intro.html', title='How To Mahjong')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # redirect user to index page if current user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # create a new user and add to database
        u = User(username=form.username.data, email=form.email.data)
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()

        # redirect new user to login page and display welcome msg
        flash('Welcome the world of Mahjong, {}! Please Sign In'.format(form.username.data))
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up - How To Mahjong', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # redirect user to index page if current user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        # Find the user
        user = User.get_user_by_email(form.email.data)
        # if user not exists or password not match, back to login page and display error msg
        # else log user in and direct to index page
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Email or Password')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)

        # 'next' is query string argument, is set to the original URL
        # request.args: request content in dictionary format
        # netloc != '': full URL inclues domain name. for security reason, can only direct to relative URL
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In - How To Mahjong', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html', title='Tutorial - How To Mahjong')

@app.route('/quiz')
@login_required
def quiz():
    form = QuizForm()
    return render_template('quiz.html', title='Quiz - How To Mahjong', form=form)

@app.route('/history/<username>')
@login_required
def history(username):
    page = request.args.get('page', 1, type=int)
    user = User.get_user_by_name(username)
    if user.get_history().first() is None:
        flash("Do not have history record yet, please finish a quiz to see history")
        return redirect(url_for('quiz'))
    else: 
        history = user.get_history().paginate(
            page, app.config['HISTORY_PER_PAGE'], False)
        next_url = url_for('history', username=user.username, page=history.next_num) \
            if history.has_next else None
        prev_url = url_for('history', username=user.username, page=history.prev_num) \
            if history.has_prev else None    
        count, avgScore = History.get_aggregate(user.id) # count, sumScore
        return render_template('history.html', title='History - How To Mahjong', 
                                user=user, history=history.items, 
                                count=count, avgScore=avgScore, 
                                next_url=next_url, prev_url=prev_url)

@app.route('/feedback/<hid>')
def feedback(hid):
    feedbacks = History.get_feedbacks(hid)
    return render_template('feedback.html', title='Feedback - How To Mahjong', 
                            feedbacks=feedbacks)

# @app.route('/user/<username>')
# @login_required
# def user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     return render_template('history.html', user = user)

@app.route('/checkAnswer', methods=['POST'])
@login_required
def checkAnswer():
    form = QuizForm()
    if form.validate_on_submit():
        score, wrongQuestion = Quiz.check_answers(request.form)
        History.new_history(score, wrongQuestion, current_user.id)
        return redirect(url_for('history',  username=current_user.username))
    else:
        return redirect(url_for('quiz'))