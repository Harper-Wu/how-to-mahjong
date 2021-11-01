'''
Werkzeug: core dependency, already installed in virtual environment
user its two method to secure the password withour storing original passwords
'''

from app               import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login       import UserMixin
from app               import login
from datetime          import datetime
from hashlib           import md5

# Create clasee above inherits from db.Model, a base class for all models
class User(UserMixin, db.Model):
    # db.Column creates field
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(64), index=True, unique = True)
    email    = db.Column(db.String(128), index=True, unique = True)

    password_hash = db.Column(db.String(128))

    history = db.relationship('History', backref='user', lazy='dynamic')

    # How to print Objects of thish class, useful for debugging
    def __repr__(self):
        return '<User id:{} username:{} email:{}>'.format(
                self.id, self.username, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_user_by_name(username):
        return User.query.filter_by(username=username).first_or_404()

    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    # request an image for a given user, return URL of the user's avatar image
    # encode('utf-8'): variable-wideth character encoding, bc MD5 in Python works on bytes and not on strings
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def get_history(self):
        return History.query.filter_by(user_id=self.id).order_by(History.timestamp.desc())

@login.user_loader
def load_user(id):
    return User.query.get(int(id)) # argument passed in by Flask-Login is String

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer) 
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    wrongQuestion = db.Column(db.String)

    

    def __repr__(self):
        return '<History id:{} score:{} user:{} wq:{}>'\
            .format(self.id, self.score, self.user_id, self.wrongQuestion)
    
    def get_aggregate(userid):
        aggregate = db.session.query(
            db.func.sum(History.score).label('scoreSum'),
            db.func.count(History.id).label('count')
            ).filter(History.user_id==userid
            ).group_by(History.user_id
            ).all()
        count = aggregate[0][1]
        sumScore = aggregate[0][0]
        avgScore = round(sumScore/count, 2)
        return count, avgScore
    
    def new_history(score, wrongQuestion, userid):
        h = History(score = score, wrongQuestion = wrongQuestion, user_id = userid)
        db.session.add(h)
        db.session.commit()

    def get_feedbacks(hid):
        wrongLst = History.query.filter_by(id=hid).first().wrongQuestion[:-2].split(", ")
        feedbacks = []
        
        for x in wrongLst:
            if Quiz.query.filter_by(id=x).first() is None:
                feedback = "You've done a great job!"  
            else:
                feedback = Quiz.query.filter_by(id=x).first().feedback 
            feedbacks.append((x, feedback))

        return feedbacks

class Quiz(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500))
    optionA = db.Column(db.String(120))
    optionB = db.Column(db.String(120))
    optionC = db.Column(db.String(120))
    optionD = db.Column(db.String(120))
    correctAnswer = db.Column(db.String(10))
    feedback = db.Column(db.String(500))
    img = db.Column(db.String(100))
    

    def __repr__(self):
        return '<Quiz id:{} Q:{} A:{} B: {} C:{} D: {} ca:{} Feedback:{}>'\
            .format(self.id, self.question, self.optionA, self.optionB, \
                self.optionC, self.optionD, self.correctAnswer, self.feedback)

    def is_answer(self, chosenAnswer):
        return self.correctAnswer == chosenAnswer

    def check_answers(chosenAnswers):
        score = 0
        wrongQuestion = ""
        for key in chosenAnswers:
            if key != 'csrf_token' and key != 'submit':
                q = Quiz.query.filter_by(id = int(key)).first()
                chosenAnswer = chosenAnswers[key]
                if q.is_answer(chosenAnswer):
                    score += 1
                else:
                    wrongQuestion += key + ", "
            else:
                pass
        return score, wrongQuestion