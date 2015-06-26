from connect import connect
import mysql.connector
from numpy import mean, std

def get_avs():
    db = connect(0)
    cur=db.cursor()

    tests=[]
    vals=[]
    meas=[]
    av=[]
    sd=[]
    out=[]
    cur.execute("Select test_type, has_num_val from Test_Type;")
#    i = 0
#    for type in cur:
#        print "type %d[1]: " % i
#        print type[1]
#        print " type %d[0]: " % i
#        print type[0]
#        i = i + 1
    i = 0
    for type in cur:
        if type[1] != 0:
            tests.append(type[0])
            vals.append([])
            meas.append([])
            av.append([])
            sd.append([])
            out.append([])
            out[i].append(type[0])
            for p in range(0,int(type[1])):
                meas[i].append([])
                av[i].append([])
                sd[i].append([])
            i = i +1

#    print out
#    print tests

    cur.execute("Select test_type_id, vals from Test;")
#    i = 0
#    for test in cur:
#        print " test[0] %d: " % i
#        print test[0]
#        print " test[1] %d:" % i
#        print test[1]
#        i = i + 1
    for test in cur:
        for x in range(0,len(vals)):
            if test[0] == tests[x]:
#                print "test num: "
#                print test[0]
#                print " vals: "
#                print test[1]
                vals[x].append(test[1])
#!!!!                meas[x].append([])
#!!!!                av[x].append([])
#                print " vals[%d]: " % x
#                print str(vals[x])

#    print vals

    for x in range(0,len(vals)):
#        print " val[%d]: " % x
        for val in vals[x]:
            val = val.split(",")
            for i in range(0,len(val)):
                meas[x][i].append(val[i])

#    print meas

    for x in range(0,len(meas)):
        for i in range(0,len(meas[x])):
            for j in range(0,len(meas[x][i])):
                meas[x][i][j] = float(meas[x][i][j])

#    print meas

    for x in range(0,len(meas)):
        for i in range(0,len(meas[x])):
            av[x][i] = mean(meas[x][i])
            sd[x][i] = std(meas[x][i]) 
#            av[x][i] = 0
#            for value in meas[x][i]:
#                 print value
#                 av[x][i] = av[x][i] + float(value)
#            print len(meas[x][i])
#            if len(meas[x][i]) != 0:
#                av[x][i] = av[x][i] / len(meas[x][i])

#    print av
#    print sd

    for x in range(0,len(out)):
        for i in range(0,len(out[x])):
            out[x].append(av[x])
            out[x].append(sd[x])
#        out[x].append(av[x])
#        print av[x]
#        out[x].append(sd[x])
#        print sd[x] 

#    print out

    return out

def fetch_list_tests():
    db = connect(0)
    cur=db.cursor()
    cur.execute("select Test_Type.name,COUNT(*),COUNT(DISTINCT Test.card_id) from Test,Test_Type WHERE Test.successful=1 and Test.test_type_id=Test_Type.test_type  GROUP BY Test.test_type_id ORDER BY Test_Type.relative_order");
    rows = cur.fetchall()
    cur.execute("select Test_Type.name,COUNT(*) from Test,Test_Type WHERE Test.test_type_id=Test_Type.test_type  GROUP BY Test.test_type_id ORDER BY Test_Type.relative_order");
    rows2 = cur.fetchall()
    finalrows = ()
    for i in range (0,len(rows)):
        arow=(rows[i][0], rows[i][1],rows[i][2],rows2[i][1])
        finalrows=finalrows+(arow,)
    return finalrows

def render_list_tests():

    stat = get_avs()

    rows = fetch_list_tests()
    
    print    '<div class="row">'
    print            '<div class="col-md-1"> </div>'
    print            '<div class="col-md-11"><table class="table table-bordered table-striped Portage_table">'
    print            '<tr><th>Test<th>Total Cards Successful<th>Total Cards Failed<th>Average Numerical Value</tr>'
#    print            '<div class="col-md-3"><b>Total Tests</b></div>'
#    print            '<div class="col-md-3"><b>Total Successful Tests</b></div>'
#    print            '<div class="col-md-3"><b>Total Cards with Successful Tests</b></div>'

#    has_vals=[]
    names = []
    db = connect(0)
    cur =  db.cursor()
    cur.execute("Select test_type, name, val_names, val_units from Test_Type;")
#    cur.execute("Select test_type_id, vals from Test;")
    x = 0
    for item in cur:
#        print item
        for s in stat:
            if s[0] == item[0]:
                s[0] = item[1]
                names.append([])
                names[x].append(item[1])
                names[x].append(item[2].split(","))
                names[x].append(item[3].split(","))
                x = x + 1
#    print has_vals
#    print stat
#    print names

    for test in rows:
#            print    '<div class="row">'
            tempstring = ""
            for x in range(0,len(stat)):
                if test[0] == stat[x][0]:
                    incip = 1
                    for i in range(0,len(stat[x][1])):
                        if incip == 1:
                            tempstring = tempstring + names[x][1][i] + ": " + "{0:.2f}".format(stat[x][1][i]) + " +-" + "{0:.2f}".format(stat[x][2][i]) + " " + names[x][2][i]
                            incip = 0
                        else:
                            tempstring = tempstring + ", " + names[x][1][i] + ": " + "{0:.2f}".format(stat[x][1][i]) + " +-" + "{0:.2f}".format(stat[x][2][i]) + " " + names[x][2][i]
#                    print tempstring
#                    test[3] = stat[x][1]
            print            '<tr><td>%s' % (test[0])
            print            '<td>%s' % (test[2])
            print            '<td>%s' % (test[3]-test[2])
            print            '<td>%s' % tempstring
            print    '</tr>'            
    print    '</table></div>'

def fetch_list_module():
    db = connect(0)
    cur = db.cursor()

    cur.execute("SELECT sn, Card_id FROM Card ORDER by Card.sn ASC")
    rows = cur.fetchall()
    return rows


def render_list_module():

    row = fetch_list_module()
    n = 0

    col1=''
    col2=''
    col3=''
    
    for cards in row:
        if n%3 == 0:
            col1+='<li><a href="module.py?card_id=%(id)s&serial_num=%(serial)s"> %(serial)s </h4></li>' %{'serial':cards[0], 'id':cards[1]}
        if n%3 == 1:
            col2+='<li><a href="module.py?card_id=%(id)s&serial_num=%(serial)s"> %(serial)s </h4></li>' %{'serial':cards[0], 'id':cards[1]}
        if n%3 == 2:
            col3+='<li><a href="module.py?card_id=%(id)s&serial_num=%(serial)s"> %(serial)s </h4></li>' %{'serial':cards[0], 'id':cards[1]}
        n += 1
        
    print '<div class="row">'
    print '<div class="col-md-4"><ul>'
    print col1
    print '</ul></div><div class="col-md-4"><ul>'
    print col2
    print '</ul></div><div class="col-md-4"><ul>'
    print col3
    print '</ul></div>'

def add_module_form():
    
    print    '<form method="post" class="sub-card-form" action="add_module2.py">'
    print    '<div class="row">'
    print            '<div class="col-md-12">'
    print                    '<h4><u>Adding a new Test Board</u></h4>'
    print            '</div>'
    print    '</div>'

    print    '<br>'
    print    '<br>'

    print    '<div class="row">'
    print            '<div class = "col-md-6">'
    print                    '<label class="sub-card">Serial Number'
    print                            '<input type="int" name="serial_number">'
    print                    '</label>'
    print            '</div>'
    print    '</div>'

    print    '<br>'

    print    '<div class="row">'
    print            '<div class="col-md-12 sub-card-submit">'
    print                    '<input type="submit">'
    print            '</div>'
    print    '</div>'

    print    '</form>'



def add_module(serial_number):
    try:
        db = connect(1)
        cur = db.cursor()

        cur.execute("INSERT INTO Card set sn = '%s'; " % (serial_number)) 
        #print '<div> INSERT INTO Card set sn = %s; </div>' %(serial_number)
        db.commit()
        db.close()
    except mysql.connector.Error as err:
       print("<h3>Serial number already exists!</h3>")
    
    
