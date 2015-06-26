import mysql.connector 
def connect( num ):
    if(num==1):
       cnx = mysql.connector.connect(user='Inserter', password='ilovecms', database='ePortage')
    if(num==0):
       cnx = mysql.connector.connect(user='ReadUser', password='ilovecms', database='ePortage')
    return cnx
