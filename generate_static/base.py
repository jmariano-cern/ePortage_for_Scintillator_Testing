#!/usr/bin/env python

import re
from webroot import webroot

def header(title=''):
    print '<head>'
    print '<link  rel="stylesheet" href="%s/static/css/bootstrap.min.css">' % webroot
    print '<link  rel="stylesheet" href="%s/static/css/style.css">' % webroot
    print '<title> %s </title>' %title
    print '</head>'

def top():
    print '<body>'
    print '<div class="container">'
    print '<div class="row">'
    print '<div class="col-md-8"><img src="%s/static/files/UMD_banner.png" class="img-responsive"></div>' % webroot
    print '<div class="col-md-4">'
    print '<br><h2 style="color:blue"> &emsp;&emsp;&emsp; ngCCM Testing  </h2>'
    print '<hr>'
    print '<br>'
    print '</div>'
    print '</div>'

    print                               '<div class ="row">'
    print                                   '<div class = "col-md-12">'
    print                                       '<a href="%s/index.html">' % webroot
    print                                           '<button>  HOME  </button>'
    print                                       '</a>'
    print                                       '<a href="%s/summary.html">' % webroot
    print					    '<button>  Summary  </button>'
    print					'</a>'
#    print					'<a href="testers.py">'
#    print					    '<button>  Testers  </button>'
#    print   				        '</a>'
#    print					'<a href="add_test.py">'
#    print					    '<button>  Add Test Results  </button>'
#    print					'</a>'
    print                                   '</div>'
    print                                   '<br><br><br>'
    print                               '</div>'


def bottom():
    print '</div>'
    print '</body>'
    print '</html>'
    
def cleanCGInumber(cgitext):
    if cgitext is None:
        return 0
    return int(re.sub('[^0-9]','',cgitext))

