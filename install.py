#!/usr/bin/env python

import os
import sys
import subprocess 
import mysql.connector
import getpass
import random
import subprocess

#rand_num = random.randint(0,999999999)

#hostname = "localhost%d" % rand_num
hostname = "localhost"

#proc = subprocess.Popen(["hostname", "/etc/services"], stdout=subprocess.PIPE, shell=True)
#(host_bak, host_err) = proc.communicate()

#os.system('sudo hostname %s' % hostname)
#os.system(" sudo bash -c ' echo %s >> /etc/hostname ' " % hostname)

testerfile=open('ePortage_testers')
testers = testerfile.readlines()
testerfile.close()

testfile=open('ePortage_tests')
lines = testfile.readlines()
testfile.close()

title=[]
short_desc=[]
long_desc=[]
has_num_vals=[]
vals_names=[]
vals_units=[]

for x in range(0,len(lines)):
    if (x%7) == 1:
        title.append(lines[x].rstrip())
    if (x%7) == 2:
        short_desc.append(lines[x].rstrip())
    if (x%7) == 3:
        long_desc.append(lines[x].rstrip())
    if (x%7) == 4:
        has_num_vals.append(int(lines[x].rstrip()))
    if (x%7) == 5:
        vals_names.append(lines[x].rstrip())
    if (x%7) == 6:
        vals_units.append(lines[x].rstrip())
        
## Add tester in test DB
def add_tester( db, user ) : 
    try:
       cur = db.cursor()
       #print user
       cmd_user = 'INSERT INTO People set person_name="%s"' % (user)
       cur.execute(cmd_user) 
       db.commit()
    except mysql.connector.Error as err:
       print("<h3>lost DB connection!</h3>")

## Add test 
def add_test( db, nu, testName, testDesShort, testDesLong, has_num_val, val_names, val_units ) : 
    try:
       cmd_test = 'insert into Test_Type set name="%s", required=1, desc_short="%s",desc_long="%s", relative_order=%d, has_num_val=%d, val_names="%s", val_units="%s"' % ( testName, testDesShort, testDesLong, nu, has_num_val, val_names, val_units )

       cur = db.cursor()
       cur.execute(cmd_test) 
       db.commit()
    except mysql.connector.Error as err:
       print("<h3>lost DB connection!</h3>")
#       print "ERROR ON: %s" % testName

## Grant Access 
def grant_access( db ) :
    try:

       cur = db.cursor()

       print 'DB Inserter Password'
       print '---------------------'
       inpw = getpass.getpass()
       cmd_gt  = "CREATE USER 'Inserter'@'%s' IDENTIFIED BY '%s'" % (hostname, inpw)

       cur.execute(cmd_gt)

       db.commit()
       cur.execute("GRANT INSERT ON ePortage.* TO 'Inserter'@'%s'" % hostname)
       db.commit()
       cur.execute("GRANT SELECT ON ePortage.* TO 'Inserter'@'%s'" % hostname)
       db.commit()

       print 'DB Reader Password'
       print '-------------------'
       rdpw = getpass.getpass()
       cmd_gt  = "CREATE USER 'ReadUser'@'%s' IDENTIFIED BY '%s'" % (hostname, rdpw)
       cur.execute(cmd_gt) 
       db.commit()
       cur.execute("GRANT SELECT ON ePortage.* TO 'ReadUser'@'%s'" % hostname)
       db.commit()

#       os.system=("touch connect.py")
       text_file = open("connect.py", "w")
       text_file.write("import mysql.connector \n")
       text_file.write("def connect( num ):\n")
       text_file.write("    if(num==1):\n")
       text_file.write("       cnx = mysql.connector.connect(user='Inserter', password='%s', database='ePortage')\n" % inpw )
       text_file.write("    if(num==0):\n")
       text_file.write("       cnx = mysql.connector.connect(user='ReadUser', password='%s', database='ePortage')\n" % rdpw )

       text_file.write("    return cnx\n") 

       text_file.close()

    except mysql.connector.Error as err:
       print("<h3>lost DB connection!</h3>")



## Setup area
#os.system("mkdir hcalDB")
#dbhome = subprocess.check_output("pwd")
os.chdir( os.getenv("HOME") )
#os.chdir("public_html")
dbhome = os.getcwd() 
print dbhome 
#os.system("git clone https://github.com/UMN-CMS/ePortage.git")
thePath = '%s%s' % (dbhome.rstrip() , "/ePortage/cgi-bin")
#print thePath
os.chdir(thePath) 
os.system("chmod a+x *.py")
os.chdir("../sql") 

#
#os.chdir("sql/") 
print 'MySQL Root password '
pw = getpass.getpass()
db = mysql.connector.connect(user='root', password= pw , database='')

cur = db.cursor()
### BE CAREFUL ###
#cur.execute("drop database ePortage")
### BE CAREFUL ###
cur.execute("create database ePortage")
db.commit()
cur.execute("use ePortage")
db.commit()

source_cmd = "mysql -u root --password=" + pw + " ePortage < schema.sql " 
#print source_cmd 
os.system( source_cmd )

for x in range(0,len(testers)):
    add_tester( db, testers[x].rstrip() )

for x in range(0,len(title)):
    add_test( db, x, title[x], short_desc[x], long_desc[x], has_num_vals[x], vals_names[x], vals_units[x] )

grant_access( db )
os.system('chmod a+x connect.py')
os.system("mv connect.py ../cgi-bin/")
#os.system("sudo rm -f /var/www/html/test/connect.py")
#os.system("sudo cp ../cms-cgi-scripts-v1/cgi-bin/connect.py /var/www/html/test/connect.py")

#os.chdir("../cms-cgi-scripts-v1")
#os.system("cp ../html/files/cmslogo.jpg static/files/")
#os.system("cp ../html/files/us-cms.gif static/files/")

db.close()

#os.system('sudo hostname %s' % host_bak)
