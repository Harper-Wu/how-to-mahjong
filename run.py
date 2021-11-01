from app import app, db
from app.models import User, History, Quiz


# If this file run directly, run app
if __name__ == '__main__':
    app.run(debug=True) 

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'History': History, 'Quiz': Quiz}