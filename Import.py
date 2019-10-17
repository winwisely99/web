#!/usr/bin/python

from bs4 import BeautifulSoup
import os.path
import shutil

'''
Super Duper Importer
'''

# le paths and directories
leRoot = 'source/github.com/letsencrypt/website/'
leImages = 'source/github.com/letsencrypt/website/static/images/'

# make a copy of the golden image folder into the LE 'static' folder
srcImgDir = 'golden/wwimages'
destImgDir = leRoot + 'static/wwimages'
if not os.path.exists(destImgDir):
  shutil.copytree(srcImgDir,destImgDir)

# new golden image path
goldenImages = 'wwimages/'

# # make a copy of the golden content folder into LE site root
# srcContentDir = 'golden/content'
# destContentDir = leRoot + 'content'
# if os.path.exists(destContentDir):
#   destContentDir.rmdir() ##### check if correct method
#   shutil.copytree(srcContentDir,destContentDir)

# # make a copy of the config folders
# srcConfigDir = 'golden/config'
# destConfigDir = leRoot + 'config'
# if os.path.exists(destConfigDir):
#   destConfigDir.rmdir() ##### check if correct method
#   shutil.copytree(srcConfigDir,destConfigDir)

########################
# layout replacements
########################

headerHtml = leRoot + '/layouts/partials/header.html'
oldLogo = '/images/letsencrypt-logo-horizontal.svg'
newLogo = goldenImages + 'logo-main.png'

with open(headerHtml) as header:
  replaceLogo = header.read().replace(oldLogo, newLogo)
with open(headerHtml, 'w') as header:
  header.write(replaceLogo)

mainCss = leRoot + 'static/css/main.min.css'
oldBanner = '/images/3.jpg'
newBanner = '../' + goldenImages + 'banners/paddle-seattle.jpg'

with open(mainCss) as css:
  replaceBanner = css.read().replace(oldBanner, newBanner)
with open(mainCss, 'w') as css:
  css.write(replaceBanner)

########################
# content replacements
########################

homePageEn = leRoot + 'i18n/en.toml'
oldHeadline = 'Let&rsquo;s Encrypt is a <span>free</span>, <span>automated</span>, and <span>open</span> Certificate Authority.'
newHeadline = '<span>WinWisely</span><br>Help Scale Courage Now'

with open(homePageEn) as en:
  replaceHeadline = en.read().replace(oldHeadline, newHeadline)
with open(homePageEn, 'w') as en:
  en.write(replaceHeadline)


# with open(headerHtml) as f:
#   elementToDelete = BeautifulSoup(f.read()).find('div', {'class': 'linux-foundation-link'})
#   removeTheElement = elementToDelete.decompose()
# with open(headerHtml, 'w') as f:
#   f.write(removeTheElement) 

# with open(headerHtml) as header:
#   replaceLogo = header.read().replace(oldLogo, newLogo)
# with open(headerHtml, 'w') as header:
#   header.write(replaceLogo)

# with open(headerHtml) as header:
#   oldFundLink = BeautifulSoup(header.read()).find("div", {'class': 'linux-foundation-link'})
#   removeFundLink = oldFundLink.decompose()

#   print removeFundLink

# with open(headerHtml) as header:
#   soup = BeautifulSoup(header, 'html.parser')
#   removeFundLink = soup.find("div", {'class': 'linux-foundation-link'})
#   removeFundLink.decompose()
#   print(soup)
# # with open(headerHtml, 'w') as header:
# #   header.write(removeFundLink)


print "done"