from flask import Flask, g, render_template, redirect, request, url_for, flash
from flask_login.mixins import UserMixin
from flask_login.utils import login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user
import sqlite3

app = Flask(__name__)
app.secret_key = "1234567890qwertyuiopasdfghjklzxcvbnmokayherewego121234asdeRTFeDRAtAtygvdtygyatg7615287yGAsdTGAo7821g273gh87td9wyd678gyGFUAYdgouy9"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DATABASE = 'charactersheets.db'
login_manager = LoginManager(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        #we posted the form- try to login
        #get the user from the forms username field
        user = User.query.filter_by(username=request.form.get("username")).first()
        #chek if we got one and that the password's match- MUST USE HASHED PASSWORDS!!! THIS IS JUST A DEMO!!
        if user and user.check_password(request.form.get("password")):
            login_user(user)
            #now current_user is set to this user- redirect back to home
            return redirect("/")
        #else flash a message?
        else:
            flash("Username and password not recognised")
    return render_template("login.html")

@app.route('/createuser', methods=["GET", "POST"])
def usercreate():
    if request.method == "POST":
        cursor = get_db().cursor()
        new_username = request.form["user_name"]
        new_password = request.form["user_password"]
        sql = "INSERT INTO user(Username, Password) VALUES (?, ?)"
        cursor.execute(sql,(new_name, new_class))
        get_db().commit()
    return render_template('createuser.html')

@app.route('/')
def contents():
    cursor = get_db().cursor()
    sql = "SELECT * FROM sheet"
    cursor.execute(sql)
    sheets = cursor.fetchall()
    return render_template('contents.html', sheets=sheets)

@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        cursor = get_db().cursor()
        new_name = request.form["character_name"]
        new_class = request.form["character_class"]
        new_race = request.form["character_race"]
        sql = "INSERT INTO sheet(CharacterName, Class, Race) VALUES (?, ?, ?)"
        cursor.execute(sql,(new_name, new_class, new_race))
        get_db().commit()
    return render_template('newsheet.html')

@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        cursor = get_db().cursor()
        id = int(request.form["c_id"])
        sql = "DELETE FROM sheet WHERE CharID = ?"
        cursor.execute(sql, (id, ))
        get_db().commit()
    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST", "UPDATE"])
def edit(id):
    if request.method == "POST":
        cursor = get_db().cursor()
        edit_name = request.form["edit_character_name"]
        edit_class = request.form["edit_character_class"]
        edit_race = request.form["edit_character_race"]
        sql = '''UPDATE sheet 
        SET CharacterName = ?, Class = ?, Race = ?
        WHERE CharID = ?'''
        cursor.execute(sql, (edit_name, edit_class, edit_race, id))
        get_db().commit()
        return redirect("/")
    return render_template('editsheet.html')

if __name__ == "__main__":
    app.run(debug=True)