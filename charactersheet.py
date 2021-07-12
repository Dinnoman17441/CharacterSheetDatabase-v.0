from flask import Flask, render_template, session, redirect, url_for, request, Blueprint, flash
from random import randint, choice
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Column, Integer, String, Boolean
import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import Config
import math

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

#████████████████████████████████████████████████████████████████████████████████████
#Classes

class Sheet(db.Model):
    __tablename__ = "Sheet"
    CharID = db.Column(db.Integer, primary_key = True)

    #Section One | Main Info
    CharacterName = db.Column(db.String)
    CharacterClass = db.Column(db.String)
    Level = db.Column(db.Integer)
    Background = db.Column(db.String)
    Race = db.Column(db.String)
    Alignment = db.Column(db.String(2))
    OwnerID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=False)

    owner = db.relationship("User", backref="sheets")

    #Section Two | Character Stats
    STR = db.Column(db.Integer)
    STRMod = db.Column(db.Integer)
    DEX = db.Column(db.Integer)
    DEXMod = db.Column(db.Integer)
    CON = db.Column(db.Integer)
    CONMod = db.Column(db.Integer)
    INT = db.Column(db.Integer)
    INTMod = db.Column(db.Integer)
    WIS = db.Column(db.Integer)
    WISMod = db.Column(db.Integer)
    CHA = db.Column(db.Integer)
    CHAMod = db.Column(db.Integer)

    #Section Three | Prof Bonus and Inspiration
    ProfBonus = db.Column(db.Integer)

    #Section Four | Saving Throws
    STRSave = db.Column(db.Integer)
    STRSaveProf = db.Column(db.Integer)
    DEXSave = db.Column(db.Integer)
    DEXSaveProf = db.Column(db.Integer)
    CONSave = db.Column(db.Integer)
    CONSaveProf = db.Column(db.Integer)
    INTSave = db.Column(db.Integer)
    INTSaveProf = db.Column(db.Integer)
    WISSave = db.Column(db.Integer)
    WISSaveProf = db.Column(db.Integer)
    CHASave = db.Column(db.Integer)
    CHASaveProf = db.Column(db.Integer)

    #Section Five | Skills
    #Skills
    Acrobatics = db.Column(db.Integer) #DEX
    Animal_Handling = db.Column(db.Integer) #WIS
    Arcana = db.Column(db.Integer) #INT
    Athletics = db.Column(db.Integer) #STR
    Deception = db.Column(db.Integer) #CHA
    History = db.Column(db.Integer) #INT
    Insight = db.Column(db.Integer) #WIS
    Intimidation = db.Column(db.Integer) #CHA
    Investigation = db.Column(db.Integer) #INT
    Medicine = db.Column(db.Integer) #WIS
    Nature = db.Column(db.Integer) #INT
    Perception = db.Column(db.Integer) #WIS
    Performance = db.Column(db.Integer) #CHA
    Persuasion = db.Column(db.Integer) #CHA
    Religion = db.Column(db.Integer) #INT
    Sleight_Of_Hand = db.Column(db.Integer) #DEX
    Stealth = db.Column(db.Integer) #DEX
    Survival = db.Column(db.Integer) #WIS

    #Skill Proficiency
    AcrobaticsProf = db.Column(db.Integer)
    Animal_HandlingProf = db.Column(db.Integer)
    ArcanaProf = db.Column(db.Integer)
    AthleticsProf = db.Column(db.Integer)
    DeceptionProf = db.Column(db.Integer)
    HistoryProf = db.Column(db.Integer)
    InsightProf = db.Column(db.Integer)
    IntimidationProf = db.Column(db.Integer)
    InvestigationProf = db.Column(db.Integer)
    MedicineProf = db.Column(db.Integer)
    NatureProf = db.Column(db.Integer)
    PerceptionProf = db.Column(db.Integer)
    PerformanceProf = db.Column(db.Integer)
    PersuasionProf = db.Column(db.Integer)
    ReligionProf = db.Column(db.Integer)
    Sleight_Of_HandProf = db.Column(db.Integer)
    StealthProf = db.Column(db.Integer)
    SurvivalProf = db.Column(db.Integer)  
    

class User(db.Model):
    __tablename__ = "User"
    UserID = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50))
    password = db.Column(db.String)

db.create_all()

#███████████████████████████████████████████████████████████████████████████████████


#Login Functions
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

@app.route('/createuser', methods = ['GET', 'POST'])
def createuser():
    if request.method == "POST":
        new_username = request.form["username"]
        new_userpassword = generate_password_hash(request.form.get('password'), salt_length = 10)
        new_user = User(username = new_username, password = new_userpassword)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/")
    return render_template('user/usercreate.html')

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
            return render_template('userlogin.html', error = 'username or password incorrect')
    return render_template('user/userlogin.html')

@app.route('/logout')
def logout():
    try:
        session.pop('useron')
    except:
        return redirect('/login', error = 'not currently logged in')
    return redirect('/')

#Sheet Functions
@app.route('/')
def contents():
    sheets = Sheet.query.all()
    return render_template('contents.html', sheets=sheets)

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

        new_STR = int(request.form["STR"])
        new_DEX = int(request.form["DEX"])
        new_CON = int(request.form["CON"])
        new_INT = int(request.form["INT"])
        new_WIS = int(request.form["WIS"])
        new_CHA = int(request.form["CHA"])

        new_STRMod = math.floor((new_STR - 10)/2)
        new_DEXMod = math.floor((new_DEX - 10)/2)
        new_CONMod = math.floor((new_CON - 10)/2)
        new_INTMod = math.floor((new_INT - 10)/2)
        new_WISMod = math.floor((new_WIS - 10)/2)
        new_CHAMod = math.floor((new_CHA - 10)/2)

        new_ProfBonus = request.form["ProfBonus"]

        new_STRSAVEPROF = request.form["STRSaveProf"]
        new_DEXSAVEPROF = request.form["DEXSaveProf"]
        new_CONSAVEPROF = request.form["CONSaveProf"]
        new_INTSAVEPROF = request.form["INTSaveProf"]
        new_WISSAVEPROF = request.form["WISSaveProf"]
        new_CHASAVEPROF = request.form["CHASaveProf"]

        if new_STRSAVEPROF == 1:
            new_STRSave = new_STRMod + new_ProfBonus
        else:
            new_STRSave = new_STRMod

        if new_DEXSAVEPROF == 1:
            new_DEXSave = new_DEXMod + new_ProfBonus
        else:
            new_DEXSave = new_DEXMod

        if new_CONSAVEPROF == 1:
            new_CONSave = new_CONMod + new_ProfBonus
        else:
            new_CONSave = new_CONMod

        if new_INTSAVEPROF == 1:
            new_INTSave = new_INTMod + new_ProfBonus
        else:
            new_INTSave = new_INTMod

        if new_WISSAVEPROF == 1:
            new_WISSave = new_WISMod + new_ProfBonus
        else:
            new_WISSave = new_WISMod

        if new_CHASAVEPROF == 1:
            new_CHASave = new_CHAMod + new_ProfBonus
        else:
            new_CHASave = new_CHAMod
            
        #Puts new data into variable
        new_character = Sheet(
            CharacterName = new_name, 
            CharacterClass = new_class, 
            Race = new_race, 
            Background = new_background, 
            Level = new_level, 
            Alignment = new_alignment,
            owner=current_user(),

            STR = new_STR,
            DEX = new_DEX,
            CON = new_CON,
            INT = new_INT,
            WIS = new_WIS,
            CHA = new_CHA,

            STRMod = new_STRMod,
            DEXMod = new_DEXMod,
            CONMod = new_CONMod,
            INTMod = new_INTMod,
            WISMod = new_WISMod,
            CHAMod = new_CHAMod,

            ProfBonus = new_ProfBonus,

            STRSaveProf = new_STRSAVEPROF,
            DEXSaveProf = new_DEXSAVEPROF,
            CONSaveProf = new_CONSAVEPROF,
            INTSaveProf = new_INTSAVEPROF,
            WISSaveProf = new_WISSAVEPROF,
            CHASaveProf = new_CHASAVEPROF,

            STRSave = new_STRSave,
            DEXSave = new_DEXSave,
            CONSave = new_CONSave,
            INTSave = new_INTSave,
            WISSave = new_WISSave,
            CHASave = new_CHASave,
        )

        #Adds new data to table
        db.session.add(new_character)

        #Commits the session
        db.session.commit()

        #Returns user to home page
        return redirect("/")
    return render_template('sheet/newsheet.html')

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
    #print(CharID_confirm.owner == current_user())
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
    return render_template("sheet/editsheet.html", sheets = sheets)

@app.route('/view/<int:CharID>', methods = ["GET", "POST"])
def view(CharID):
    if request.method == "GET":
        sheets = Sheet.query.filter_by(CharID = CharID).all()
    return render_template('sheet/viewsheet.html', sheets=sheets)

@app.route('/viewcanvas/<int:CharID>', methods = ["GET", "POST"])
def viewcanvas(CharID):
    if request.method == "GET":
        sheets = Sheet.query.filter_by(CharID = CharID).all()
    return render_template('sheet/sheetcanvas.html', sheets=sheets)


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