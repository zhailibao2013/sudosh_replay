from flask_wtf import Form
from wtforms import TextField, BooleanField,PasswordField,SubmitField
from wtforms.validators import Required

class LoginForm(Form):
    username = TextField(U'UserName: ',validators=[Required()])
    password = TextField(U'Password: ',validators=[Required()])
    remember_me = BooleanField('remember_me',)
    submit = SubmitField(u'Login')
class SearchForm(Form):
    username = TextField(U'UserName: ',validators=[Required()])
    password = TextField(U'Password: ',validators=[Required()])
    submit = SubmitField(u'Login')
