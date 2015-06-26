#!/usr/bin/env python

from connect import connect
import mysql.connector
import os

def fetch_list_module():
    db = connect(0)
    cur = db.cursor()

    cur.execute("SELECT sn, Card_id FROM Card ORDER by Card.sn ASC")
    rows = cur.fetchall()
    return rows

row = fetch_list_module()
n = 0

for cards in row:
    command = "python module.py %s %s > /var/www/static/modules/module_card_id%s_serial_num%s.html" % (cards[1], cards[0], cards[1], cards[0])
    os.system(command)
        
