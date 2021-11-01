import os
# define a base directory
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    '''
    Config app token, generate 16 digits secret key using secrets package 
    in python interpretor
    '''
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dbab7738c3d03d53c016c5d9ea21b729'

    # Config database
    # Provide configuration variable or fallback value
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    # Disable tracking modifications, do not signal the application
    # every time a change is about to be made in the database
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    HISTORY_PER_PAGE = 10