#!../../env/bin/python
import os,sys
from distutils.sysconfig import get_python_lib
dir=get_python_lib()+'/sudosh_replay/'
os.chdir(dir)
sys.path.append(dir)
from app import app
app.run(host='0.0.0.0',debug = True)
