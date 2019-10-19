#!/usr/bin/python

from bs4 import BeautifulSoup
import os.path
import shutil

'''
Super Duper Importer
'''

###################################
# Paths and Directories
###################################

leRoot = 'source/github.com/letsencrypt/website/'
leImages = 'source/github.com/letsencrypt/website/static/images/'

# Replace the Golden WW IMAGE dir into the LE 'static' dir
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

# Replace the Golden LE CONTENT/EN dir with the WW CONTENT/EN dir only
srcContentDir = 'golden/content/en'
destContentDir = leRoot + 'content/en'
if not os.path.exists(destContentDir):
    shutil.copytree(srcContentDir,destContentDir)
    print('Golden content directory updated successfully!')
else:
    shutil.rmtree(destContentDir)           
    shutil.copytree(srcContentDir,destContentDir)
    print('Golden content directory updated successfully!')

# Replace the Golden LE CONFIG dir with the WW content dir
srcConfigDir = 'golden/config'
destConfigDir = leRoot + 'config'
if not os.path.exists(destConfigDir):
    shutil.copytree(srcConfigDir,destConfigDir)
    print('Golden config directory updated successfully!')
else:
    shutil.rmtree(destConfigDir)           
    shutil.copytree(srcConfigDir,destConfigDir)
    print('Golden config directory updated successfully!')

# Delete LE git directory, it doesnt need to be there
gitDir = leRoot + '.git'
if os.path.exists(gitDir):
    shutil.rmtree(gitDir) 


###################################
# Layout Only
###################################

# Replace file favicon
srcFavicon = 'golden/wwimages/favicon.ico'
destFavicon = leRoot + 'static/favicon.ico'
from shutil import copyfile
shutil.copyfile(srcFavicon,destFavicon)

### Header Partial #####

# Replace logo and alt text
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

# Remove hideous foundation link
with open(headerHtml) as header:
  soup = BeautifulSoup(header, 'html.parser')
  removeFundLink = soup.find("div", {'class': 'linux-foundation-link'})
  statusLink = bool(removeFundLink)
if statusLink:
  removeFundLink.decompose()
  goneFundLink = str(soup)
  with open(headerHtml, 'w') as header:
    header.write(goneFundLink)

# Replace banner on homepage
mainCss = leRoot + 'static/css/main.min.css'
oldBanner = '/images/3.jpg'
newBanner = '../' + goldenImages + 'banners/1-dark.jpg'
try:
  with open(mainCss) as css:
    replaceBanner = css.read().replace(oldBanner, newBanner)
  with open(mainCss, 'w') as css:
    css.write(replaceBanner)
except IOError:
  print(mainCss + ' not accessible.')

# Replace banner on child pages
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

# Change banner text
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

### Footer Partial #####

# Replace contact footer text
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
# Homepage Adhoc
###################################

# Append Home Content to Index
homeHtml = 'golden/layouts/home.html'
indexHtml = leRoot + 'layouts/index.html'

def writeToLine(lines, lineNum, appendText):
    lines[lineNum] = lines[lineNum].replace('\n', '') + appendText + '\n'

with open(homeHtml) as home:
  soup = BeautifulSoup(home, 'html.parser')
  homeContent = str(soup)

with open(indexHtml) as index:
  soup2 = BeautifulSoup(index, 'html.parser')
  indexContent = str(soup)
  isDivThere = soup2.find("div", {'class': 'home-content'})
  statusDiv = bool(isDivThere) 
if not statusDiv:
  with open(indexHtml, 'r') as txtfile:
    lines = txtfile.readlines()
    # index is 15 for 16th line
    writeToLine(lines, 15, homeContent)
  with open(indexHtml, 'w') as txtfile:
    txtfile.writelines(lines)
  with open(mainCss, 'a') as c:
    c.write('.pure-g.home {display:none !important}')


print "done"