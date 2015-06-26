#!/usr/bin/python

import cgi
import base
import home_page_list
import add_test_functions


#cgi header
print "Content-type: text/html\n"

form = cgi.FieldStorage()
#card_id = form.getvalue('card_id')
serial_num = base.cleanCGInumber(form.getvalue('serial_num'))
suggested_test = base.cleanCGInumber(form.getvalue('suggested'))
person_id = base.cleanCGInumber(form.getvalue('person_id'))

base.header(title='Add Test Results')
base.top()

add_test_functions.add_test_template(serial_num,suggested_test,person_id)

base.bottom()
