from sudopy_list import sudo_list
from werkzeug import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    is_active = db.Column(db.Boolean())
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
    def store_to_db(self):
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


    def __repr__(self):
        return '<User %r>' % (self.username)

class LoginUser(UserMixin):
    def __init__(self, id, name, active=True):
        self.id = id
        self.name = name
        self.active = active

    def is_active(self):
        return self.active

class SudoItem(object):
    def __init__(self,Date, Duration, From, To, ID):
        self.__Date=Date
        self.__Duration = Duration
        self.__From = From
        self.__To = To
        self.__ID = ID
    def getID(self):
        return self.__ID
    def getDate(self):
        return self.__Date
    def getDuration(self):
        return self.__Duration
    def getFrom(self):
        return self.__From
    def getTo(self):
        return self.__To

class Sudos(object):
    def __init__(self,sudoList=None,start=1,p_size=0):
        self.sudos=[]
        self.start = (int(start)-1)*p_size
        self.p_size = int(p_size)
        self.has_prev = False
        self.has_next = False
        self.prev_num = int(start)-1
        self.next_num = int(start)+1
        if sudoList is not None:
            for item in sudoList:
                if len(item) == 6:
                    record = SudoItem(item[0]+" " + item[1],item[2],item[3],item[4],item[5])
                    self.sudos.append(record)
        self.length=len(self.sudos)
    def getSudos(self):
        if self.start < 0 or self.p_size < 0:
            return self.sudos 
        if self.p_size == 0:
            return self.sudos[self.start:]
        else:
            if self.start >= self.length:
                self.has_prev = True
                return []
            elif self.start+self.p_size < self.length:
                if self.start != 0:
                    self.has_prev = True
                self.has_next = True
                return self.sudos[self.start:self.start+self.p_size]
            else:
                self.has_prev = True
                return self.sudos[self.start:]
            
#sudoLists = Sudos(sudo_list())
#myList = sudoLists.getSudos()
#for one in myList:
#    print one.getDate()

