#!/usr/bin/env python

from connect import connect
import mysql.connector
import os

def fetch_list_module():
    db = connect(0)
    cur = db.cursor()

    cur.execute("SELECT attach_id FROM Attachments ORDER by Attachments.attach_id ASC")
    rows = cur.fetchall()
    return rows

row = fetch_list_module()
n = 0

for attach in row:
    command = "python get_attach.py %s" % (attach[0])
    os.system(command)

