import os
CRSF_ENABLED=False
SECRET_KEY = 'you-will-never-guess'
SUDOSHPATH='/var/log/sudosh/'
PAGE_SIZE=5
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
