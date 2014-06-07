import os
from flask import Flask
from flask_login import LoginManager
from flask.ext.openid import OpenID
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
from config import basedir
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lms = LoginManager()
lms.init_app(app)
CsrfProtect(app)
lms.login_view ='login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))
from app import views,models

