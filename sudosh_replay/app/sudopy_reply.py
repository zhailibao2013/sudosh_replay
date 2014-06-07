#!/usr/bin/python
# -*- coding: utf-8 -*-
from contextlib import closing
from math import ceil
from os.path import basename, dirname, exists
from jinja2 import FileSystemLoader, Template
from jinja2.environment import  Environment
from json import dumps
DEFAULT_TEMPLATE    =   '/var/log/bin/flask/sudosh/app/static/static.jinja2'
#DEFAULT_TEMPLATE    =   'static/static.jinja2'
# http://blog.taz.net.au/2012/04/09/getting-the-terminal-size-in-python/
def probeDimensions(fd=1):
    """
    Returns height and width of current terminal. First tries to get
    size via termios.TIOCGWINSZ, then from environment. Defaults to 25
    lines x 80 columns if both methods fail.

    :param fd: file descriptor (default: 1=stdout)
    """
    try:
        import fcntl, termios, struct
        hw = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
    except:
        try:
            hw = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            hw = (24, 80)

    return hw
def escapeString(string):
    try:
        string = string.decode(stdout.encoding).encode('unicode_escape')
        string = string.replace("'", "\\'")
        string = '\'' + string + '\''
    except:
        string = '\'' + string.encode('string_escape') + '\''
    return string
def getTiming(timef):
    timing = None
    with closing(timef):
        timing = [l.strip().split(' ') for l in timef]
        timing = [(int(ceil(float(r[0]) * 1000)), int(r[1])) for r in timing]
    ## if time >2s, set the time==2s
    f= lambda x: x > 2000 and 2000 or x
    timing = [(f(r[0]), r[1]) for r in timing]
    return timing
def scriptToJSON(scriptf, timing=None):
    ret = []

    with closing(scriptf):
        scriptf.readline() # ignore first header line from script file 
        offset = 0
        for t in timing:
            data = escapeString(scriptf.read(t[1]))
            offset += t[0]
            ret.append((data, offset))
    print ret
    return dumps(ret)
def renderTemplate(json, dimensions, templatename, outfname=None):
    fsl = FileSystemLoader(dirname(templatename), 'utf-8')
    e = Environment()
    e.loader = fsl

    templatename = basename(templatename)
    rendered = e.get_template(templatename).render(json=json,
                                                   dimensions=dimensions)

    return rendered

    #with closing(outf):
    #    outf.write(rendered)
def sudo_replay(timef,scriptf):
    tmpname=DEFAULT_TEMPLATE
    timef=open('/var/log/sudosh/root-test-time-1400490705-fqh0AetwIILwiDUT','r')
    scriptf=open('/var/log/sudosh/root-test-script-1400490705-fqh0AetwIILwiDUT','r')
    dimensions = probeDimensions() if not scriptf else (24,80)
    timing = getTiming(timef)
    json = scriptToJSON(scriptf, timing)
    #outf=open('/var/log/sudosh/test.html','w')
    #if tmpname and outf:
     #   renderTemplate(json, dimensions, tmpname, outf)
    if tmpname:
        return renderTemplate(json, dimensions, tmpname)
