from flask import Flask, g, render_template, request, redirect, session, url_for, escape, Blueprint, flash
from random import randint, choice
import os
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "1234567890qwertyuiopasdfghjklzxcvbnmokayherewego121234asdeRTFeDRAtAtygvdtygyatg7615287yGAsdTGAo7821g273gh87td9wyd678gyGFUAYdgouy9"
DATABASE = 'charactersheets.db'
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

#def get_db():
#    db = getattr(g, '_database', None)
#    if db is None:
#        db = g._database = sqlite3.connect(DATABASE)
#    return db

@app.context_processor
def add_current_user():
    if session.get('user'):
        return dict(current_user=Userinfo.query.get(session['user']))
    return dict(current_user=None)

@app.route('/login', methods = ['GET', 'POST'])
def login():
   if request.method == 'POST':
        session['username'] = request.form['username']
        return render_template('login.html')

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect('/login')

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
        new_background = request.form["character_background"]
        new_level = request.form["character_level"]
        new_alignment = request.form["character_alignment"]
        sql = "INSERT INTO sheet(CharacterName, Class, Race, Background, Level, Alignment) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(sql,(new_name, new_class, new_race, new_background, new_level, new_alignment))
        get_db().commit()
        return redirect("/")
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
        edit_background = request.form["character_background"]
        edit_level = request.form["character_level"]
        edit_alignment = request.form["character_alignment"]
        sql = '''UPDATE sheet 
        SET CharacterName = ?, Class = ?, Race = ?, Background = ?, Level = ?, Alignment = ?,
        WHERE CharID = ?'''
        cursor.execute(sql, (edit_name, edit_class, edit_race, edit_background, edit_level, edit_alignment, id))
        get_db().commit()
        return redirect("/")
    return render_template('editsheet.html')

@app.route("/view/<int:id>", methods=["GET", "POST"])
def view(id):
    if request.method == "GET":
        cursor = get_db().cursor()
        sql = "SELECT * FROM sheet WHERE CharID = ?"
        cursor.execute(sql, (id, ))
        sheets = cursor.fetchall()
        get_db().commit()
        return render_template('viewsheet.html', sheets=sheets)

if __name__ == "__main__":
    app.run(debug=True)