# -*- coding: utf-8 -*-  
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import render_template, flash,request,url_for, redirect, session,g
from flask_login import login_user, logout_user, current_user, login_required
#from app import app,db,lm,oid
from flask_wtf import Form
from sudopy_list import sudo_list,sudolist_filterbytime
from forms import LoginForm,SearchForm
from models import Sudos,User,LoginUser
from sudopy_reply import *
from config import SUDOSHPATH,PAGE_SIZE
from app import lms,app,db,oid
import copy
#SUDOSHPATH=config.SUDOSHPATH
#PAGE_SIZE=config.PAGE_SIZE
G_SUDOLISTS=sudo_list()

@app.route('/') 
@app.route('/index', methods = ['GET',]) 
@app.route('/index/<int:page>', methods = ['GET',]) 
@login_required
def index(page=1):
    global G_SUDOLISTS
    form = SearchForm()
    sudoLists=Sudos(G_SUDOLISTS,page,PAGE_SIZE)
    #for one in myList:
    #    return  one.getDate()
    return render_template('index.html',sudos=sudoLists,form=form)
@app.route('/search',methods =['POST',])
def search():
    if request.form['filter'] =="":
        filter={'date':''}
    else:
        filter={'date':request.form['filter']}
    global G_SUDOLISTS
    G_SUDOLISTS = sudo_list()
    G_SUDOLISTS = sudolist_filterbytime(G_SUDOLISTS,filter)
    return redirect(url_for("index"))
@app.route('/id/<string:id>')
def replay(id):
    tmpname=DEFAULT_TEMPLATE
    idList=id.split('-')
    timeList=copy.copy(idList)
    scriptList=copy.copy(idList)
    timeList.insert(2,'time')
    timefpath='-'.join(timeList)
    scriptList.insert(2,'script')
    scriptfpath='-'.join(scriptList)

    timef=open(SUDOSHPATH+timefpath,'r')
    scriptf=open(SUDOSHPATH+scriptfpath,'r')
    
    dimensions = probeDimensions() if not scriptf else (24,80)
    timing = getTiming(timef)
    json = scriptToJSON(scriptf, timing)
    return renderTemplate(json, dimensions, tmpname)
@lms.user_loader
def load_user(id):
    return User.query.get(int(id))
@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = 1
        session['remember_me'] = form.remember_me.data
        session['username'] = form.username.data
        session['password'] = form.password.data
        user = User.query.filter_by(username=username).first()
        if not len(form.errors):
            loginuser = LoginUser(user.id, user.username)
            if login_user(loginuser, remember=remember):
               
                return redirect(url_for("index"))
        else:
            flash(u"not found user!")  
    if('remember_me' in session and session['remember_me']):
        form.remember_me.data = 1
        form.username.data = session['username']
        form.password.data = session['password']
        
    return render_template('login.html', 
        title = 'Sign In',
        form = form,
        )
@oid.after_login
def after_login(resp):
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))
@app.before_request
def before_request():
    g.user = current_user
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
