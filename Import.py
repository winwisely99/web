#!/usr/bin/python

from bs4 import BeautifulSoup

'''
Super Duper Importer

'''

# golden paths and directories
goldenRoot = 'golden/winwisely.org/'
goldenImages = 'golden/assets/images/'

# le paths and directories
leRoot = 'src/github.com/letsencrypt/website/'
leImages = 'src/github.com/letsencrypt/website/static/images/'

# make a copy of the golden folder into the le static folder

import shutil
import errno

src = '/golden/'
dest = '/' + leRoot + 'static/golden/'

print src
 
def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)



####################
# layout 
####################

### replace logo
headerUrl = leRoot + '/layouts/partials/header.html'
logoOld = '/images/letsencrypt-logo-horizontal.svg'
logoNew = goldenImages + 'logo-main.png'

with open(headerUrl) as f:
  replaceLogo=f.read().replace(logoOld, logoNew)
with open(headerUrl, "w") as f:
  f.write(replaceLogo)

### remove foundation link





print "done"