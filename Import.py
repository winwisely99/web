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
goldenImages = 'wwimages/'

###################################
# Main Functions
###################################

# Copy directory
def placeDirectory(nameDir, srcDir, destDir):
  if not os.path.exists(destDir):
    shutil.copytree(srcDir,destDir)
  else:
    shutil.rmtree(destDir)
    shutil.copytree(srcDir,destDir)
  print(nameDir + 'directory updated successfully!')

# Delete directory
def deleteDirectory(nameDir,rmDir):
  if os.path.exists(rmDir):
    shutil.rmtree(rmDir)
    print(nameDir + 'directory deleted successfuly!')

# Copy file
def placeFile(nameFile, srcFile, destFile):
  from shutil import copyfile
  shutil.copyfile(srcFile,destFile)
  print(nameFile + 'file updated successfully!')

# Replace strings in file
def replaceString(file, oldLine, newLine):
  try:
    with open(file) as f:
      replaceThis = f.read().replace(oldLine, newLine)
    with open(file, 'w') as f:
      f.write(replaceThis)
  except IOError:
    print(file + ' not accessible.')

# Remove HTML element
def deleteElement(file, tag, selector, value):
  with open(file) as f:
    soup = BeautifulSoup(f, 'html.parser')
    removeThis = soup.find(tag, {selector : value})
    status = bool(removeThis)
  if status:
    removeThis.decompose()
    newHtml = str(soup)
    with open(file, 'w') as f:
      f.write(newHtml)

# Append Data
def writeToLine(lines, lineNum, appendText):
  lines[lineNum] = lines[lineNum].replace('\n', '') + appendText + '\n'



###################################
# Directory Structure
###################################

# Replace the Golden WW IMAGE dir into the LE 'static' dir
srcImages = 'golden/wwimages'
destImages = leRoot + 'static/wwimages'
placeDirectory('wwimages',srcImages,destImages)

# Replace the Golden LE CONTENT/EN dir with the WW CONTENT/EN dir only
srcContent = 'golden/content/en'
destContent = leRoot + 'content/en'
placeDirectory('content',srcContent,destContent)

# Replace the Golden LE CONFIG dir with the WW content dir
srcConfig = 'golden/config'
destConfig = leRoot + 'config'
placeDirectory('content',srcConfig,destConfig)

# Delete LE git directory, it doesnt need to be there
gitDir = leRoot + '.git'
deleteDirectory('LE Git folder',gitDir)


###################################
# Layout Only
###################################

# Replace file favicon
srcFavicon = 'golden/wwimages/favicon.ico'
destFavicon = leRoot + 'static/favicon.ico'
placeFile('Favicon', srcFavicon, destFavicon)

### Header Partial #####

# Replace logo and alt text
headerHtml = leRoot + 'layouts/partials/header.html'
oldLogo = '/images/letsencrypt-logo-horizontal.svg'
newLogo = goldenImages + 'logo-main.png'
oldAlt = 'Let\'s Encrypt'
newAlt = 'WinWisely'
replaceString(headerHtml, oldLogo, newLogo)
replaceString(headerHtml, oldAlt, newAlt)

# Remove hideous foundation link
deleteElement(headerHtml, 'div', 'class', 'linux-foundation-link')

# Replace banner on homepage
mainCss = leRoot + 'static/css/main.min.css'
oldBanner = '/images/3.jpg'
newBanner = '../' + goldenImages + 'banners/1-dark.jpg'
replaceString(mainCss, oldBanner, newBanner)

# Replace banner on child pages
heroHtml = leRoot + 'layouts/partials/hero.html'
oldHero = 'images/%d.jpg'
newHero = 'wwimages/banners/%d.jpg'
replaceString(heroHtml, oldHero, newHero)

# Change banner text
i18nEN = leRoot + 'i18n/en.toml'
oldHeroTitle = 'Let&rsquo;s Encrypt is a <span>free</span>, <span>automated</span>, and <span>open</span> Certificate Authority.'
newHeroTitle = '<span>WinWisely</span><br>It&rsquo;s A Numbers Game'
replaceString(i18nEN, oldHeroTitle, newHeroTitle)

### Footer Partial #####

# Replace contact footer text
footerHtml = leRoot + 'layouts/partials/footer.html'
oldAddress1 = '1 Letterman Drive, Suite D4700,'
newAddress1 = '(650) 383 8435 | gary@winwisely.org'
oldAddress2 = 'San Francisco,'
oldAddress3 = 'CA'
oldAddress4 = '94129'
linuxLink = '{{ i18n "linux_foundation_trademark" }}'

replaceString(footerHtml, oldAddress1, newAddress1)
replaceString(footerHtml, oldAddress2, '')
replaceString(footerHtml, oldAddress3, '')
replaceString(footerHtml, oldAddress4, '')
replaceString(footerHtml, linuxLink, '')




###################################
# Homepage Adhoc
###################################

# Append Home Content to Index
homeHtml = 'golden/layouts/home.html'
indexHtml = leRoot + 'layouts/index.html'

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

# Change Button and Link on Banner
oldButtonLink = 'become-a-sponsor'
newButtonLink = 'donate'
oldButtonText = 'home_hero_sponsor'
newButtonText = 'home_hero_donate'
try:
  with open(indexHtml) as i:
    replaceHeader = i.read().replace(oldButtonLink,newButtonLink).replace(oldButtonText, newButtonText)
  with open(indexHtml, 'w') as i:
    i.write(replaceHeader)
except IOError:
  print(indexHtml + ' not accessible.')

replaceString(indexHtml, oldButtonLink, newButtonLink)
replaceString(indexHtml, oldButtonText, newButtonText)


print "done"