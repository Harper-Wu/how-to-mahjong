# CITS5505Project2

## Web Application Purpose and Assessement Mechanism
This web application provides an introduction and tutorial about Mahjong which is a tile-based game and also a formative assessement quiz for users to test their understanding of this game. The Formative assessement is consists of 10 multiple choice questions and one score for each question. Users can view their quiz history with average score and times they have done the quiz, as well as feedback for the questions they have done wrong.

## The Architecture of the Web Application
This application is constists of 6 modules: Sign In/Sign Up, Introduction, Tutorial, Quiz, History and Feedback. Users can view content of Introduction and   Tutorial, and required to login to take quiz, see history and feedback as these section are related to individual user.

## Getting Started
To activate python virtual environment: `$source venv\bin\activate`  
To run the app: `$python run.py`  
To stop the app: `$ctrl c`  
Te deactivate virtual environment: `$deactivate`  

## Unit tests
FormCase tests all the form's submission, including login, registration and quiz.  
ModelsCase tests funcitons in the models.py, including get user history and feedback, etc.  
To run unit tests: `python tests.py`

## Git Commit Logs
This project is done by 23052765 Harper Wu and 23067035 Ethan Chen.

```
ee300cf by Harper, 61 seconds ago, message: fix bug: modified test.py for adding question # at feedback
679b1a9 by Ethan-Chen, 36 minutes ago, message: style all forms
eb39e7e by Harper, 2 hours ago, message: Add question # to feedback
ec04075 by Ethan-Chen, 5 hours ago, message: Update app.db
b1614b8 by Ethan-Chen, 13 hours ago, message: change the logic of save progress feature
6697d85 by Ethan-Chen, 13 hours ago, message: some fix
eb7054a by Ethan-Chen, 13 hours ago, message: styling flask form
325b6bb by Ethan-Chen, 14 hours ago, message: add content to tutorial
a934a57 by Ethan-Chen, 2 days ago, message: partial work of tutorial
38db600 by Ethan-Chen, 2 days ago, message: add content to tutorial
4649d78 by Ethan-Chen, 2 days ago, message: testing the save progress feature
cb30b50 by Harper, 2 days ago, message: edit database and clean some code
531c0b2 by Harper, 2 days ago, message: adjust quiz photo size
5b39544 by Harper, 2 days ago, message: add photo to quiz
c471942 by Harper, 2 days ago, message: Add error handling
7d3b42b by Ethan-Chen, 3 days ago, message: bug fix
0b6b156 by Ethan-Chen, 3 days ago, message: stuck for save progress feature
9868b89 by Ethan-Chen, 3 days ago, message: clean up base and form
1fbc091 by Harper, 3 days ago, message: add form test
413a9ac by Harper, 4 days ago, message: Paginated History
5363ada by Harper, 4 days ago, message: Add unit test
f68e28f by Harper, 4 days ago, message: re-write quiz, history & feedback's functions
b8971c6 by Harper, 4 days ago, message: renamed test to quiz
5cef0a1 by Harper, 5 days ago, message: Finish Feedback
c554cf6 by Harper, 5 days ago, message: Finish history
aa35b8a by Harper, 5 days ago, message: finish quiz
7bc3fbf by Ethan-Chen, 5 days ago, message: clean up some of the code
21d4613 by Harper, 6 days ago, message: Update quiz
74533ff by Harper, 7 days ago, message: Add quiz and history add app.db file update requirements.txt and readme.md
057f0d3 by Harper, 12 days ago, message: Combined template files into templates folder Modified Readme
0773aea by Ethan-Chen, 2 weeks ago, message: created template for each page
a74133b by Harper, 2 weeks ago, message: add login and registration
907bc47 by Harper, 2 weeks ago, message: restructure
29461a5 by Ethan-Chen, 2 weeks ago, message: Create some placeholder
56f4b39 by Harper, 2 weeks ago, message: add password methods and update gitignore file
0637cf6 by Harper, 2 weeks ago, message: Set up database
256e419 by Harper, 3 weeks ago, message: 1. add requirements.txt 2. add login and register, intro page
7b21169 by Harper, 3 weeks ago, message: add venv and pycache to gitignore
1e221f8 by theHarper, 3 weeks ago, message: Delete Requirement.md
585592c by 23067035, 3 weeks ago, message: The requirement for readme document
8808e4c by theHarper, 3 weeks ago, message: Documentations
60aaf9e by theHarper, 3 weeks ago, message: Initial commit```
