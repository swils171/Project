# imports
import os  # os is used to get environment variables IP & PORT

import bcrypt as bcrypt
from flask import Flask, request, redirect, url_for  # Flask is the web app that we will customize
from flask import render_template
from flask import session
from database import db
from models import Note as Note
from models import User as User
from models import Comment as Comment
from models import Report as Report
from forms import RegisterForm
from forms import LoginForm
from forms import CommentForm

app = Flask(__name__)  # create an app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SE3155'
#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)
# Setup models
with app.app_context():
    db.create_all()  # run under the app context


# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page

@app.route('/')
@app.route('/index')
def index():
    # check if a user is saved in session
    if session.get('user'):
        return render_template("index.html", user=session['user'])
    return render_template("index.html")


@app.route('/notes')
def get_notes():
    # check if a user us saved in session
    if session.get('user'):
        # retrieve notes from database
        my_notes = db.session.query(Note).all()  # .filter_by(user_id=session['user_id'])

        return render_template('notes.html', notes=my_notes, user=session['user'], id=session['user_id'])
    else:
        return redirect(url_for('login'))


# show peers function
@app.route('/peers')
def get_peers():
    # check if a user us saved in session
    if session.get('user'):
        # retrieve notes from database
        my_notes = db.session.query(User).all()  # .filter_by(user_id=session['user_id'])

        return render_template('peers.html', users=my_notes, user=session['user'], id=session['user_id'])
    else:
        return redirect(url_for('login'))


@app.route('/notes/<note_id>')
def get_note(note_id):
    # check if a user saved in session
    if session.get('user'):
        # retrieve note from database
        my_note = db.session.query(Note).filter_by(id=note_id).one()  # , user_id=session['user_id']

        # create a comment form object
        form = CommentForm()

        return render_template('note.html', note=my_note, user=session['user'], form=form)
    else:
        return redirect(url_for('login'))


@app.route('/notes/new', methods=['GET', 'POST'])
def new_note():
    # check if a user is saved in session
    if session.get('user'):
        # check method used for request
        if request.method == 'POST':
            # get title data
            title = request.form['title']
            # get note data
            text = request.form['noteText']
            # create data stamp
            from datetime import date
            today = date.today()
            # format date mm/dd/yyyy
            today = today.strftime("%m-%d-%Y")
            new_record = Note(title, text, today, session['user_id'])
            db.session.add(new_record)
            db.session.commit()

            return redirect(url_for('get_notes'))
        else:
            # GET request - show new note form
            return render_template('new.html', user=session['user'])
    else:
        # user is not in session redirect to login
        return redirect(url_for('login'))


@app.route('/notes/edit/<note_id>', methods=['GET', 'POST'])
def update_note(note_id):
    # check if a user is saved in session
    note = db.session.query(Note).filter_by(id=note_id).one()

    if session.get('user'):
        if session.get("user_id") == note.user_id:
            if request.method == 'POST':
                # get title data
                title = request.form['title']
                # get note data
                text = request.form['noteText']
                # update note data
                note.title = title
                note.text = text
                # update note int DB
                db.session.add(note)
                db.session.commit()
                return redirect(url_for('get_notes'))

            else:
                # GET request - show new note form to edit note

                # retrieve note from database
                my_note = db.session.query(Note).filter_by(id=note_id).one()
                return render_template('new.html', note=my_note, user=session['user'])
        else:
            return redirect(url_for('get_notes'))
    else:
        # user is not in session redirect to login
        return redirect(url_for('login'))


@app.route('/notes/delete/<note_id>', methods=['POST'])
def delete_note(note_id):
    my_note = db.session.query(Note).filter_by(id=note_id).one()
    # check if a user is saved in session
    if session.get('user'):
        if session.get("user_id") == my_note.user_id:
            # retrieve note from database
            db.session.delete(my_note)
            db.session.commit()

            return redirect(url_for('get_notes'))
        else:
            return redirect(url_for('get_notes'))
    else:
        # user is not in session redirect to login
        return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # get entered user data
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        # create user model
        new_user = User(first_name, last_name, request.form['email'], h_password)
        # add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        session['user'] = first_name
        session['user_id'] = new_user.id  # access id value from user model of this newly added user
        # show user dashboard view
        return redirect(url_for('get_notes'))

    # something went wrong - display register view
    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    # validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # we know user exists. We can use one()
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        # user exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id
            # render view
            return redirect(url_for('get_notes'))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:
        # form did not validate or GET request
        return render_template("login.html", form=login_form)


@app.route('/logout')
def logout():
    # check if a user is saved in session
    if session.get('user'):
        session.clear()

    return redirect(url_for('index'))


@app.route('/notes/<note_id>/comment', methods=['POST'])
def new_comment(note_id):
    if session.get('user'):
        comment_form = CommentForm()
        # validate_on_submit only validates using POST
        if comment_form.validate_on_submit():
            # get comment data
            comment_text = request.form['comment']
            new_record = Comment(comment_text, int(note_id), session['user_id'])
            db.session.add(new_record)
            db.session.commit()

        return redirect(url_for('get_note', note_id=note_id))

    else:
        return redirect(url_for('login'))


@app.route('/notes/<note_id>/LikeNote', methods=['POST'])
def like_note(note_id):
    # check if a user is saved in session
    if session.get('user'):
        # retrieve note from database
        note = db.session.query(Note).filter_by(id=note_id).one()
        note.score = note.score + 1
        db.session.commit()
        return redirect(url_for('get_note', note_id=note_id))
    else:
        # user is not in session redirect to login
        return redirect(url_for('login'))


"""
@app.route('/notes/<note_id>/DislikeNote', methods=['POST'])
def dislike_note(note_id):
    # check if a user is saved in session
    if session.get('user'):
        # retrieve note from database
        note = db.session.query(Note).filter_by(id=note_id).one()
        note.score = note.score - 1
        db.session.commit()
        return redirect(url_for('get_note', note_id=note_id))
    else:
        # user is not in session redirect to login
        return redirect(url_for('login'))
"""


@app.route('/notes/<note_id>/LikeComment/<comment_id>', methods=['POST'])
def like_comment(note_id, comment_id):
    # check if a user is saved in session
    if session.get('user'):
        # retrieve note from database
        updateComment = db.session.query(Comment).filter_by(id=comment_id).one()
        updateComment.score = updateComment.score + 1
        db.session.commit()
        return redirect(url_for('get_note', note_id=note_id))
    else:
        # user is not in session redirect to login
        return redirect(url_for('login'))


"""
@app.route('/notes/<note_id>/DislikeComment/<comment_id>', methods=['POST'])
def dislike_comment(note_id, comment_id):
    # check if a user is saved in session
    if session.get('user'):
        # retrieve note from database
        updateComment = db.session.query(Comment).filter_by(id=comment_id).one()
        updateComment.score = updateComment.score - 1
        db.session.commit()
        return redirect(url_for('get_note', note_id=note_id))
    else:
        # user is not in session redirect to login
        return redirect(url_for('login'))
"""


@app.route('/notes/<note_id>/new_report', methods=['GET', 'POST'])
def new_report(note_id):
    # check if a user is saved in session
    if session.get('user'):
        # check method used for request
        if request.method == 'POST':
            # get title data
            title = request.form['title']
            # get note data
            text = request.form['reportText']
            # create data stamp
            from datetime import date
            today = date.today()
            # format date mm/dd/yyyy
            today = today.strftime("%m-%d-%Y")
            report = Report(int(note_id), title, text, today, session['user_id'])
            db.session.add(report)
            db.session.commit()

            return redirect(url_for('get_notes'))
        else:
            # GET request - show new request form
            return render_template('new_report.html', user=session['user'])
    else:
        # user is not in session redirect to login
        return redirect(url_for('login'))


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
