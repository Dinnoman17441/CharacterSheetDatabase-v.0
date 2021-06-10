from flask import Flask, render_template, session, redirect, url_for, request, Blueprint, flash
from random import randint, choice
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Column, Integer, String
import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

#████████████████████████████████████████████████████████████████████████████████████
#Classes

class Sheet(db.Model):
    CharID = db.Column(db.Integer, primary_key = True)
    CharacterName = db.Column(db.String)
    CharacterClass = db.Column(db.String)
    Level = db.Column(db.Integer)
    Background = db.Column(db.String)
    Race = db.Column(db.String)
    Alignment = db.Column(db.String(2))
    OwnerID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable = False)

    owner = db.relationship("User", backref="sheets")

class User(db.Model):
    __tablename__ = "User"
    UserID = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50))
    password = db.Column(db.String)

#███████████████████████████████████████████████████████████████████████████████████


def current_user():
    if session.get('useron'):
        return User.query.get(session['useron'])
    else:
        return False

@app.context_processor
def add_current_user():
    if session.get('useron'):
        return dict(current_user = User.query.get(session['useron']))
    return dict(current_user = None)

@app.route('/')
def contents():
    sheets = Sheet.query.all()
    return render_template('contents.html', sheets=sheets)

@app.route('/createuser', methods = ['GET', 'POST'])
def createuser():
    if request.method == "POST":
        new_username = request.form["username"]
        new_userpassword = generate_password_hash(request.form.get('password'), salt_length = 10)
        new_user = User(username = new_username, password = new_userpassword)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/")
    return render_template('createuser.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if session.get('useron'):
        return redirect('/')
    if request.method == "POST":
        useron = User.query.filter(User.username == request.form.get('login_username')).first()
        if useron and check_password_hash(useron.password, request.form.get('login_password')):
            session['useron'] = useron.UserID
            return redirect("/")
        else:
            return render_template('login.html', error = 'username or password incorrect')
    return render_template('login.html')

@app.route('/logout')
def logout():
    try:
        session.pop('useron')
    except:
        return redirect('/login', error = 'not currently logged in')
    return redirect('/')

@app.route('/add', methods = ["GET", "POST"])
def add():
    if request.method == "POST":
        #Collects new data from form
        new_name = request.form["character_name"]
        new_class = request.form["character_class"]
        new_race = request.form["character_race"]
        new_background = request.form["character_background"]
        new_level = request.form["character_level"]
        new_alignment = request.form["character_alignment"]

        #Puts new data into variable
        new_character = Sheet(
            CharacterName = new_name, 
            CharacterClass = new_class, 
            Race = new_race, 
            Background = new_background, 
            Level = new_level, 
            Alignment = new_alignment,
            owner=current_user()
        )

        #Adds new data to table
        db.session.add(new_character)

        #Commits the session
        db.session.commit()

        #Returns user to home page
        return redirect("/")
    return render_template('newsheet.html')

@app.route('/delete', methods = ["GET", "POST"])
def delete():
    if request.method == "POST":
        id = request.form["c_id"]

        #Selects row by ID and deletes it
        Sheet.query.filter_by(CharID = id).delete()

        #Commits the session
        db.session.commit()
    return redirect("/")

@app.route('/edit/<int:CharID>', methods = ["GET", "POST", "UPDATE"])
def edit(CharID):
    CharID_confirm = Sheet.query.filter_by(CharID = CharID).first()
    print(CharID_confirm.owner == current_user())
    if CharID_confirm.owner != current_user():
        return redirect("/")
    if request.method == "POST":
        sheets = Sheet.query.filter_by(CharID = CharID).all()

        #Collects edit data from form
        edit_name = request.form["edit_character_name"]
        edit_class = request.form["edit_character_class"]
        edit_race = request.form["edit_character_race"]
        edit_background = request.form["edit_character_background"]
        edit_level = request.form["edit_character_level"]
        edit_alignment = request.form["edit_character_alignment"]
            
        Sheet.query.filter_by(CharID = CharID).update(dict(
            CharacterName = edit_name, 
            CharacterClass = edit_class, 
            Race = edit_race, 
            Background = edit_background, 
            Level = edit_level, 
            Alignment = edit_alignment
        ))
        
        #Commits the session
        db.session.commit()
        return redirect("/")
    sheets = Sheet.query.filter_by(CharID = CharID).all()
    return render_template("editsheet.html", sheets = sheets)

@app.route('/view/<int:CharID>', methods = ["GET", "POST"])
def view(CharID):
    if request.method == "GET":
        sheets = Sheet.query.filter_by(CharID = CharID).all()
    return render_template('viewsheet.html', sheets=sheets)

#the following code is pre-SQLALCHEMY

"""
@app.route('/')
def contents():
    #cursor = get_db().cursor()
    #sql = "SELECT * FROM sheet"
    #cursor.execute(sql)
    #sheets = cursor.fetchall()
    #return render_template('contents.html', sheets=sheets)

@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        #cursor = get_db().cursor()
        new_name = request.form["character_name"]
        new_class = request.form["character_class"]
        new_race = request.form["character_race"]
        new_background = request.form["character_background"]
        new_level = request.form["character_level"]
        new_alignment = request.form["character_alignment"]
        sql = "INSERT INTO sheet(CharacterName, CharacterClass, Race, Background, Level, Alignment) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(sql,(new_name, new_class, new_race, new_background, new_level, new_alignment))
        #get_db().commit()
        return redirect("/")
    return render_template('newsheet.html')

@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        #cursor = get_db().cursor()
        id = int(request.form["c_id"])
        sql = "DELETE FROM sheet WHERE CharID = ?"
        cursor.execute(sql, (id, ))
        #get_db().commit()
    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST", "UPDATE"])
def edit(id):
    if request.method == "POST":
        #cursor = get_db().cursor()
        edit_name = request.form["edit_character_name"]
        edit_class = request.form["edit_character_class"]
        edit_race = request.form["edit_character_race"]
        edit_background = request.form["character_background"]
        edit_level = request.form["character_level"]
        edit_alignment = request.form["character_alignment"]
        sql = '''UPDATE sheet 
        SET CharacterName = ?, CharacterClass = ?, Race = ?, Background = ?, Level = ?, Alignment = ?,
        WHERE CharID = ?'''
        cursor.execute(sql, (edit_name, edit_class, edit_race, edit_background, edit_level, edit_alignment, id))
        #get_db().commit()
        return redirect("/")
    return render_template('editsheet.html')

@app.route("/view/<int:id>", methods=["GET", "POST"])
def view(id):
    if request.method == "GET":
        #cursor = get_db().cursor()
        sql = "SELECT * FROM sheet WHERE CharID = ?"
        cursor.execute(sql, (id, ))
        sheets = cursor.fetchall()
        #get_db().commit()
        return render_template('viewsheet.html', sheets=sheets) """

if __name__ == "__main__":
    app.run(debug=True)

# For when git doesn't remember my email (everytime)
# git config --global user.email "17441@burnside.school.nz"