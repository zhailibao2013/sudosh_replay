Introduction
============
sudosh-replay is a web replay of sudosh. web is base on flask,It is microframework 
for python . sudosh is an auditing shell filter and can be used as a login shell. 
Sudosh records all keystrokes and output and can play 
back the session as just like a VCR. for more infomation of sudosh ,please see 
http://sourceforge.net/projects/sudosh2/?source=navbar.  The web replay is inspired by
TermRecord ,https://github.com/theonewolf/TermRecord


Running Tests
=============
    Install and config sudosh2.
1.down load suosh2 from http://sourceforge.net/projects/sudosh2/
2.make;install
3.vim /etc/sudosh.conf
  # Sudosh Configuration File
  logdir                  = /var/log/sudosh
  default shell           = /bin/sh
  delimiter               = -
  syslog.priority         = LOG_INFO
  syslog.facility         = LOG_LOCAL2
  clearenvironment        = no

  # Allow Sudosh to execute -c arguments?  If so, what?
  -c arg allow = scp
  -c arg allow = rsync
4.modify user login shell    
  vim /etc/password
   root:x:0:0:root:/root:/usr/local/bin/sudosh
5.vim /etc/shells
  /bin/sh
  /bin/bash
  /sbin/nologin
  /bin/dash
  /bin/tcsh
  /bin/csh
  /usr/local/bin/sudosh
6. vim /etc/default/useradd
  # useradd defaults file
  GROUP=100
  HOME=/home
  INACTIVE=-1
  EXPIRE=
  #SHELL=/bin/bash
  SHELL=/usr/local/bin/sudosh
  SKEL=/etc/skel
  CREATE_MAIL_SPOOL=yes
-----------------------------------------------------
    install sudosh-replay
1.install virtualenv,pip install virtualenv
2.mkdir sudosh-replay
3./usr/local/python/bin/envirtualenv env;. env/bin/activate
4.wget https://pypi.python.org/packages/source/p/pbr/pbr-0.8.2.tar.gz --no-check-certificate
5.wget https://pypi.python.org/packages/source/s/sqlalchemy-migrate/sqlalchemy-migrate-0.9.1.tar.gz#md5=5f0237ed55041b9a831d4d18d0a46f53 --no-check-certificate
6.pip install -r requirements.txt
7.pip install sudosh-replay,or python setup.py install
7.run application: sudosh_replay.py
