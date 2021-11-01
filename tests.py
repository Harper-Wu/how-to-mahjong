from datetime   import datetime, timedelta
import unittest
from app        import app, db
from app.models import User, Quiz, History

class FormCase(unittest.TestCase):
    def setUp(self):
        
        app.config['TESTING'] = True            # Config app to testing
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF
        # Changing app.config to 'sqlite://' to use in-memory SQLite database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        self.app = app.test_client()            # Create a client for unittest
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    #  regi function to mock registration form
    def regi(self, email, username, password):
        return self.app.post('/register', data=dict(
            username=username,
            email=email,
            password=password,
            confirm_password=password,

        ), follow_redirects=True) 

    # login function to mock login form
    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email=email,
            password=password,
            remember_me=False
        ), follow_redirects=True)
    
    # submit funciton to mock quiz form
    def submit_quiz(self):
        return self.app.post('/checkAnswer', data={'csrf_token': 'Pretend.To.Be.Token', 
                    '1': 'A', 
                    '2': 'B', 
                    '3': 'C', 
                    'submit': 'Submit'}, follow_redirects=True)

    

    def test_regi_login(self):
        # test registration correctlly, redirect to login page instead of Sign Up page
        rv = self.regi('test@test.com','test', 'car')
        self.assertIn(b'<title>Sign In - How To Mahjong</title>', rv.data)
        self.assertFalse(b'<title>Sign Up - How To Mahjong</title>' in rv.data)

        # test registration incorrectlly, redirect to Sign Up page instead of login page
        rv = self.regi('test','test', 'car')
        self.assertIn(b'<title>Sign Up - How To Mahjong</title>', rv.data)
        self.assertFalse(b'<title>Sign In - How To Mahjong</title>' in rv.data)

        rv = self.login('test@test.com','car')
        self.assertIn(b'<title>How To Mahjong</title>', rv.data)

    # test submit quiz form, should return to history page
    def test_submit_quiz(self):
        q1 = Quiz(correctAnswer='A', feedback="Q1's answer is A")
        q2 = Quiz(correctAnswer='B', feedback="Q2's answer is B")
        q3 = Quiz(correctAnswer='C', feedback="Q3's answer is C")
        
        db.session.add(q1)
        db.session.add(q2)
        db.session.add(q3)
        db.session.commit()

        # quiz page is login_required, need to register and login user first
        self.regi('test@test.com','test', 'car')
        self.login('test@test.com','car')

        rv = self.submit_quiz()
        # print(rv.data)
        self.assertTrue(b'<title>History - How To Mahjong</title>' in rv.data)
        self.assertFalse(b'<title>Sign In - How To Mahjong</title>' in rv.data)



class ModelCase(unittest.TestCase):
    def setUp(self):
        # Changing app.config to 'sqlite://' to use in-memory SQLite database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        # Creates all DB tables
        db.create_all()
    
    def tearDown(self):
        # Remove DB session and drop all tables after test finished
        db.session.remove()
        db.drop_all()

    # Test User set_password
    def test_pw_hasing(self):
        u = User(username='John')
        u.set_password('Qaz')

        db.session.add(u)
        db.session.commit()

        self.assertFalse(u.check_password('qaz'))
        self.assertTrue(u.check_password('Qaz'))
    
    # Test User avatar
    def test_avatar(self):
        u = User(username='Jane', email='jane@asdf.com')
        # from hashlib import md5
        # 'https://www.gravatar.com/avatar/' + md5(b'jane@asdf.com').hexdigest()
        # default size:80x80 pixels, add size ?s=128 add the end to set size
        self.assertEqual(u.avatar(128),
                        'https://www.gravatar.com/avatar/1c2be6b9af81fc770825a966ac12c3e0?d=identicon&s=128')


    # Test History Model
    # test one answer of a question
    def test_is_answer(self):
        q = Quiz(correctAnswer='A')

        self.assertTrue(q.is_answer('A'))
        self.assertFalse(q.is_answer('B'))

    # test quiz submitted form answers, check if the score and wrongQuestion are right
    def test_check_answers(self):
        # Add quiz correctAnswer
        q1 = Quiz(correctAnswer='A', feedback="Q1's answer is A")
        q2 = Quiz(correctAnswer='B', feedback="Q2's answer is B")
        q3 = Quiz(correctAnswer='C', feedback="Q3's answer is C")

        db.session.add(q1)
        db.session.add(q2)
        db.session.add(q3)
        db.session.commit()

        # persudo form submitted data
        quizData = {'csrf_token': 'Pretend.To.Be.Token', 
                    '1': 'A', 
                    '2': 'C', 
                    '3': 'B', 
                    'submit': 'Submit'}
        score, wrongQuestion = Quiz.check_answers(quizData)
        
        # test score
        self.assertEqual(score, 1)
        self.assertNotEqual(score, 0)
        self.assertNotEqual(score, 2)
        self.assertNotEqual(score, 3)
        # test wrongQuestion
        self.assertEqual(wrongQuestion, '2, 3, ')
        self.assertNotEqual(wrongQuestion, '2')
        self.assertNotEqual(wrongQuestion, '3')

        # test new_history()    
        History.new_history(score, wrongQuestion, 1)
        h = History.query.first()
        self.assertEqual(h.score, 1)
        self.assertNotEqual(h.score, 0)
        self.assertNotEqual(h.score, 2)
        self.assertNotEqual(h.score, 3)

        self.assertEqual(h.wrongQuestion, '2, 3, ')
        self.assertNotEqual(h.wrongQuestion, '2')
        self.assertNotEqual(h.wrongQuestion, '3')

        # Test Feedback
        f = History.get_feedbacks(1)
        self.assertEqual(f[0][1], "Q2's answer is B")
        self.assertEqual(f[1][1], "Q3's answer is C")
        
    

if __name__ == '__main__':
    unittest.main(verbosity=2)