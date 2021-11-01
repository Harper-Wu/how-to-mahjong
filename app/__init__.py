from flask            import Flask 
from config           import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate    import Migrate
from flask_login      import LoginManager # Manage logged-in state, provides remember me
from dotenv           import load_dotenv
from flask_moment     import Moment

app = Flask(__name__)
# initialized Flask-Login
login = LoginManager(app)
login.login_view = 'login' # tell Flask-Login which view function handles logings

# Tell Flask to read and apply config file
app.config.from_object(Config)

# Configure database
# Object db represents the database
db = SQLAlchemy(app)
# Object migrate represents the migration engine
migrate = Migrate(app, db)

# add Moment extension
moment = Moment(app)

from app import routes, models, errors