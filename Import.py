#!/usr/bin/python

from bs4 import BeautifulSoup
import os.path
import shutil

'''
Super Duper Importer
'''

########################
# paths and directories
########################

leRoot = 'source/github.com/letsencrypt/website/'
leImages = 'source/github.com/letsencrypt/website/static/images/'

# make a copy of the golden image folder into the LE 'static' folder
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

# make a copy of the golden content folder into LE site root
srcContentDir = 'golden/content'
destContentDir = leRoot + 'content'
if not os.path.exists(destContentDir):
    shutil.copytree(srcContentDir,destContentDir)
    print('Golden content directory updated successfully!')
else:
    shutil.rmtree(destContentDir)           
    shutil.copytree(srcContentDir,destContentDir)
    print('Golden content directory updated successfully!')

# make a copy of the config folders
srcConfigDir = 'golden/config'
destConfigDir = leRoot + 'config'
if not os.path.exists(destConfigDir):
    shutil.copytree(srcConfigDir,destConfigDir)
    print('Golden config directory updated successfully!')
else:
    shutil.rmtree(destConfigDir)           
    shutil.copytree(srcConfigDir,destConfigDir)
    print('Golden config directory updated successfully!')

# make a copy of the i18n folders
srcI18nDir = 'golden/i18n'
destI18nDir = leRoot + 'i18n'
if not os.path.exists(destI18nDir):
    shutil.copytree(srcI18nDir,destI18nDir)
    print('Golden i18n directory updated successfully!')
else:
    shutil.rmtree(destI18nDir)           
    shutil.copytree(srcI18nDir,destI18nDir)
    print('Golden i18n directory updated successfully!')

# delete LE git directory, it doesnt need to be there
gitDir = leRoot + '.git'
if os.path.exists(gitDir):
    shutil.rmtree(gitDir) 

# replace favicon
srcFavicon = 'golden/wwimages/favicon.ico'
destFavicon = leRoot + 'static/favicon.ico'
from shutil import copyfile
shutil.copyfile(srcFavicon,destFavicon)

########################
# layout replacements
########################

srcIndex = 'golden/layouts/index.html'
destIndex = leRoot + '/layouts/index.html'
from shutil import copyfile
shutil.copyfile(srcIndex,destIndex)

srcIndex = 'golden/layouts/partials/footer.html'
destIndex = leRoot + '/layouts/partials/footer.html'
from shutil import copyfile
shutil.copyfile(srcIndex,destIndex)

headerHtml = leRoot + '/layouts/partials/header.html'
oldLogo = '/images/letsencrypt-logo-horizontal.svg'
newLogo = goldenImages + 'logo-main.png'
try:
  with open(headerHtml) as header:
    replaceLogo = header.read().replace(oldLogo, newLogo)
  with open(headerHtml, 'w') as header:
    header.write(replaceLogo)
except IOError:
  print(headerHtml + ' not accessible.')

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

headerHtml = leRoot + '/layouts/partials/header.html'
oldLogo = '/images/letsencrypt-logo-horizontal.svg'
newLogo = goldenImages + 'logo-main.png'
try:
  with open(headerHtml) as header:
    replaceLogo = header.read().replace(oldLogo, newLogo)
  with open(headerHtml, 'w') as header:
    header.write(replaceLogo)
except IOError:
  print(headerHtml + ' not accessible.')

oldAlt = 'Let\'s Encrypt'
newAlt = 'WinWisely'
try:
  with open(headerHtml) as header:
    replaceAlt = header.read().replace(oldAlt, newAlt)
  with open(headerHtml, 'w') as header:
    header.write(replaceAlt)
except IOError:
  print(headerHtml + ' not accessible.')

heroHtml = leRoot + '/layouts/partials/hero.html'
oldHero = 'images/%d.jpg'
newHero = 'wwimages/banners/%d.jpg'
try:
  with open(heroHtml) as header:
    replaceHero = header.read().replace(oldHero, newHero)
  with open(heroHtml, 'w') as header:
    header.write(replaceHero)
except IOError:
  print(heroHtml + ' not accessible.')


########################
# content replacements
########################

try:
  with open(headerHtml) as header:
    soup = BeautifulSoup(header, 'html.parser')
    removeFundLink = soup.find("div", {'class': 'linux-foundation-link'})
    removeFundLink.decompose()
    goneFundLink = str(soup)
  with open(headerHtml, 'w') as header:
    header.write(goneFundLink)
except IOError:
  print(headerHtml + ' not accessible.')

print "done"