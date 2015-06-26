#!/usr/bin/python

from connect import connect
import mysql.connector
import cgi
import base
import add_test_functions

#cgi header
print "Content-type: text/html\n"

form = cgi.FieldStorage()
person_id = base.cleanCGInumber(form.getvalue("person_id"))
test_type = base.cleanCGInumber(form.getvalue("test_type"))
serial_num = base.cleanCGInumber(form.getvalue("serial_number"))
success = base.cleanCGInumber(form.getvalue("success"))
comments = form.getvalue("comments")

db = connect(0)
cur = db.cursor()

cur.execute("select test_type, name , desc_short, desc_long, has_num_val from Test_Type order by relative_order ASC;")

for test in cur:
    if test[0] == test_type:
        num_vals = test[4]

vals = ""
for x in range(0,num_vals):
    vals = vals + form.getvalue("num_val%d" % x)
    if x != (num_vals-1):
        vals = vals + ","

suggested_test = test_type + 1

carriage_return = chr(13)
new_line = chr(10)
breakoff = carriage_return + new_line
brokenoff = comments.split(breakoff)
new_comments=""
for line in brokenoff:
    new_comments = new_comments + "<p>" + line + "</p>"


#db = connect(0)
#cur = db.cursor()

#print		'<form action="add_test.py" method="post" enctype="multipart/form-data">'
#print 			'<INPUT TYPE="hidden" name="serial_number" value="%d">' % (serial_num)
#print			'<div class="row">'
#print				'<div class="col-md-12">'
#print					'<h1>Add Test Results for Card %d</h1>' %serial_num
#print				'</div>'
#print			'</div>'

print '<html>'
print   '<head>'
print     '<title>redirect</title>'
print     '<META http-equiv="refresh" content="1;URL=/cgi-bin/add_test.py?serial_num=%s&suggested=%s&person_id=%s">' % (serial_num, suggested_test, person_id)
print   '</head>'
print   '<body bgcolor="#ffffff">'
print     '<br><br><br><br><br><br><br></br></br></br></br></br></br></br>'
print     '<center>Add Successful! Redirecting...</a>'
print     '</center>'
print   '</body>'
print '</html>'

#if comments:
#    comments = cgi.escape(comments)

#base.header(title='Add Test Results')
#base.top()

test_id=add_test_functions.add_test(person_id, test_type, serial_num, success, new_comments, vals)

itest = 1
afile = form['attach%d'%(itest)]
if (afile.filename):
    adesc= form.getvalue("attachdesc%d"%(itest))
    if adesc:
        adesc = cgi.escape(adesc)
        brokendesc = adesc.split(breakoff)
        new_adesc=""
        for line in brokendesc:
           new_adesc = new_adesc + "<p>" + line + "</p>"
    else:
        new_adesc = adesc
    add_test_functions.add_test_attachment(test_id,afile,new_adesc)

#for itest in (1,2,3):
#    afile = form['attach%d'%(itest)]
#    if (afile.filename):
#        adesc= form.getvalue("attachdesc%d"%(itest))
#        if adesc:
#            adesc = cgi.escape(adesc)
#        acomment= form.getvalue("attachcomment%d"%(itest))
#        if acomment:
#            acomment = cgi.escape(acomment)
#        add_test_functions.add_test_attachment(test_id,afile,adesc)#,acomment)
    

#base.bottom()

