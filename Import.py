#!/usr/bin/python

from bs4 import BeautifulSoup
import os.path
import shutil

'''
Super Duper Importer
'''

###################################
# paths and directories
###################################

leRoot = 'source/github.com/letsencrypt/website/'
leImages = 'source/github.com/letsencrypt/website/static/images/'

# make a copy of the GOLDEN image dir into the LE 'static' dir
srcImgDir = 'golden/wwimages'
destImgDir = leRoot + 'static/wwimages'

if not os.path.exists(destImgDir):
    shutil.copytree(srcImgDir,destImgDir)
    print('Golden image directory updated successfully!')
else:
    shutil.rmtree(destImgDir)           
    shutil.copytree(srcImgDir,destImgDir)
    print('Golden image directory updated successfully!')

goldenImages = 'wwimages/'

# replace the LE CONTENT dir with the WW content dir
srcContentDir = 'golden/content'
destContentDir = leRoot + 'content'

if not os.path.exists(destContentDir):
    shutil.copytree(srcContentDir,destContentDir)
    print('Golden content directory updated successfully!')
else:
    shutil.rmtree(destContentDir)           
    shutil.copytree(srcContentDir,destContentDir)
    print('Golden content directory updated successfully!')

# replace the LE CONFIG dir with the WW content dir
srcConfigDir = 'golden/config'
destConfigDir = leRoot + 'config'

if not os.path.exists(destConfigDir):
    shutil.copytree(srcConfigDir,destConfigDir)
    print('Golden config directory updated successfully!')
else:
    shutil.rmtree(destConfigDir)           
    shutil.copytree(srcConfigDir,destConfigDir)
    print('Golden config directory updated successfully!')

# delete LE git directory, it doesnt need to be there
gitDir = leRoot + '.git'

if os.path.exists(gitDir):
    shutil.rmtree(gitDir) 

srcIndex = 'golden/layouts/index.html'
destIndex = leRoot + 'layouts/index.html'

from shutil import copyfile
shutil.copyfile(srcIndex,destIndex)

###################################
# layout only
###################################

### header partial #####

# replace favicon
srcFavicon = 'golden/wwimages/favicon.ico'
destFavicon = leRoot + 'static/favicon.ico'

from shutil import copyfile
shutil.copyfile(srcFavicon,destFavicon)

# replace logo and alt text
headerHtml = leRoot + 'layouts/partials/header.html'
oldLogo = '/images/letsencrypt-logo-horizontal.svg'
newLogo = goldenImages + 'logo-main.png'
oldAlt = 'Let\'s Encrypt'
newAlt = 'WinWisely'

try:
  with open(headerHtml) as header:
    replaceHeader = header.read().replace(oldLogo, newLogo).replace(oldAlt, newAlt)
  with open(headerHtml, 'w') as header:
    header.write(replaceHeader)
except IOError:
  print(headerHtml + ' not accessible.')

# remove funding link
with open(headerHtml) as header:
  soup = BeautifulSoup(header, 'html.parser')
  removeFundLink = soup.find("div", {'class': 'linux-foundation-link'})
  statusLink = bool(removeFundLink)
if statusLink:
  removeFundLink.decompose()
  goneFundLink = str(soup)
  with open(headerHtml, 'w') as header:
    header.write(goneFundLink)

#replace banner on homepage
mainCss = leRoot + 'static/css/main.min.css'
oldBanner = '/images/3.jpg'
newBanner = '../' + goldenImages + 'banners/1.jpg'

try:
  with open(mainCss) as css:
    replaceBanner = css.read().replace(oldBanner, newBanner)
  with open(mainCss, 'w') as css:
    css.write(replaceBanner)
except IOError:
  print(mainCss + ' not accessible.')

#replace banner child pages
heroHtml = leRoot + 'layouts/partials/hero.html'
oldHero = 'images/%d.jpg'
newHero = 'wwimages/banners/%d.jpg'

try:
  with open(heroHtml) as header:
    replaceHero = header.read().replace(oldHero, newHero)
  with open(heroHtml, 'w') as header:
    header.write(replaceHero)
except IOError:
  print(heroHtml + ' not accessible.')

### footer partial #####

# replace contact footer text
footerHtml = leRoot + 'layouts/partials/footer.html'
oldAddress1 = '1 Letterman Drive, Suite D4700,'
newAddress1 = '(650) 383 8435 | gary@winwisely.org'
oldAddress2 = 'San Francisco,'
oldAddress3 = 'CA'
oldAddress4 = '94129'
linuxLink = '{{ i18n "linux_foundation_trademark" }}'

try:
  with open(footerHtml) as footer:
    replaceFooter = footer.read().replace(oldAddress1,newAddress1).replace(oldAddress2,'').replace(oldAddress3,'').replace(oldAddress4,'').replace(linuxLink,'')
  with open(footerHtml, 'w') as footer:
    footer.write(replaceFooter)
except IOError:
  print(footerHtml + ' not accessible.')


###################################
# 118n files - EN only
###################################

i18nEN = leRoot + 'i18n/en.toml'
oldHeroTitle = 'Let&rsquo;s Encrypt is a <span>free</span>, <span>automated</span>, and <span>open</span> Certificate Authority.'
newHeroTitle = '<span>WinWisely</span><br>It&rsquo;s A Numbers Game'
try:
  with open(i18nEN) as en:
    replaceEN = en.read().replace(oldHeroTitle,newHeroTitle)
  with open(i18nEN, 'w') as en:
    en.write(replaceEN )
except IOError:
  print(i18nEN + ' not accessible.')


print "done"