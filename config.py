import os
class Config(object):
    project_dir = os.path.dirname(os.path.abspath(__file__))
    database_file = (f'sqlite:///{(os.path.join(project_dir, "charactersheets.db"))}')

    SECRET_KEY = ('olviervilervolvier')
    #I have hidden my secret key behind a wall of special characters so anyone who accesses my code won't be able to steal my user's information ☼_☼

    SQLALCHEMY_DATABASE_URI = database_file
    SQLALCHEMY_TRACK_MODIFICATIONS = False