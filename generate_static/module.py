#!/usr/bin/python

import sys
import cgi
import base
import home_page_list
import module_functions
from connect import connect

#cgi header
print "<html>"


form = cgi.FieldStorage()
card_id = int(sys.argv[1])
serial_num = int(sys.argv[2])
base.header(title='ngCCM ePortage')
base.top()
#print 'card_id = ', card_id
#print  'serial_num = ', serial_num

module_functions.add_test_tab(serial_num,card_id)

#print    '<div class="row">'
#print            '<div class="col-md-12">'
#print            '<h2>Test Results for ngCCM %s</h2>' % serial_num 
#print            '</div>'
#print    '</div>'

revokes=module_functions.Portage_fetch_revokes(serial_num)

db = connect(0)
cur = db.cursor()

cur.execute("select test_type, name, desc_long from Test_Type where required = 1 order by relative_order ASC")
for test_type in cur:
	module_functions.ePortageTest(test_type[0], serial_num, test_type[1], revokes, test_type[2])


base.bottom()
