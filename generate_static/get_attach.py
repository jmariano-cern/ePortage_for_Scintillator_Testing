#!/usr/bin/python

import cgi
import base
import module_functions
from connect import connect
import settings
import os.path
import sys

form = cgi.FieldStorage()
#attach_id = base.cleanCGInumber(form.getvalue('attach_id'))
attach_id = int(sys.argv[1])

db=connect(0)
cur=db.cursor()

cur.execute("SELECT test_id, attachmime, originalname FROM Attachments WHERE attach_id=%d" % (attach_id));

if not cur.with_rows:
#    print "Content-type: text/html\n"
#    base.header("Attachment Request Error")
#    base.top()
#    print "<h1>Attachment not available</h1>"
#    base.bottom()
    print "Error: Attachment not found! (ID: %s)" % attach_id
else:    
    thevals=cur.fetchall();
    attpath=settings.getAttachmentPathFor(thevals[0][0],attach_id)
    if not os.path.isfile(attpath):
#        print "Content-type: text/html\n"
#        base.header("Attachment Request Error")
#        base.top()
#        print "<h1>Attachment not found</h1>"
#        base.bottom()        
        print "Error: Attachment not found! (ID: %s)" % attach_id
    else:
#        statinfo = os.stat(attpath)
#        print 'Content-type: %s \r\nContent-length: %d \r\nContent-Disposition: INLINE; filename="%s" \n' % (thevals[0][1],statinfo.st_size,thevals[0][2])
#        sys.stdout.write(file(attpath,"rb").read() )
        name,extension = os.path.splitext(thevals[0][2])
        f = open("/var/www/static/attachments/get_attach_id%d%s" % (attach_id, extension),'w')
        f.write(file(attpath,"rb").read() )
        f.close
