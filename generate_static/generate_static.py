#!/usr/bin/env python

import os
import datetime
import time

os.system("rm /var/www/static/attachments/*")
os.system("rm /var/www/static/modules/*")
os.system("./home_page.py > /var/www/static/index.html")
os.system("./summary.py > /var/www/static/summary.html")
os.system("./generate_modules.py")
os.system("./generate_attachments.py")
date = datetime.date.today()
time = time.strftime("%H-%M")
command = "tar cvzf /var/www/ngCCM_ePortage_%s-%s.tar.gz -C /var/www/static ." % (date,time)
os.system(command)
os.system("cp /var/www/ngCCM_ePortage_*.tar.gz /var/www/archive/")
os.system("mv /var/www/ngCCM_ePortage_*.tar.gz /var/www/ngCCM_ePortage.tar.gz")
os.chdir("/var/www")
os.system("git add ngCCM_ePortage.tar.gz")
command2 = 'git commit -m "%s-%s"' % (date,time)
os.system(command2)
os.system("git push -u origin master")
os.system("rm /var/www/ngCCM_ePortage.tar.gz")
