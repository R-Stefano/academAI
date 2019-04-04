'''
This file is used only to update the DB tables
'''
from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from dbManager import *

app = Flask(__name__)

DATABASE_URL='postgres://zvooegvhaqwbne:aba6c4f9bc784483820d76ff32a1b3bb7abdc87edf95f1eeaa1ec8643aa460c4@ec2-23-23-173-30.compute-1.amazonaws.com:5432/d1p8og4frpej6q'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

db.init_app(app)

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()