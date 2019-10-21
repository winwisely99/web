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
goldenImages = '/wwimages/'

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

# Append data to end of file
def appendToFile(source, file, content):
  with open(source) as f:
    soup = BeautifulSoup(f, 'html.parser')
  with open(file, 'a') as f:
    f.write(content)


# Append data to specific line of file
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
newBanner = '..' + goldenImages + 'banners/1-dark.jpg'
replaceString(mainCss, oldBanner, newBanner)

# Replace banner on child pages
heroHtml = leRoot + 'layouts/partials/hero.html'
oldHero = 'images/%d.jpg'
newHero = goldenImages +'banners/%d.jpg'
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

# Replace content in donate footer
enFile = leRoot + 'i18n/en.toml'
oldDonateBox = 'Support a more secure and privacy-respecting Web.'
newDonateBox = 'Support us and help scale courage!'
replaceString(enFile, oldDonateBox, newDonateBox)

###################################
# Homepage Adhoc
###################################

# Append custom home content and css to corresponding files
customHome = 'golden/layouts/home.txt'
customCss = 'golden/layouts/css.txt'
customHead = 'golden/layouts/google.txt'
indexPartial = leRoot + 'layouts/index.html'
headPartial = leRoot + 'layouts/partials/head.html'

with open(customHome) as home:
  soup = BeautifulSoup(home, 'html.parser')
  newHomeContent = str(soup)
with open(customCss) as css:
  soup = BeautifulSoup(css, 'html.parser')
  newCssContent = str(soup)
with open(customHead) as head:
  soup = BeautifulSoup(head, 'html.parser')
  newHeadContent = str(soup)

with open(indexPartial) as i:
  soup = BeautifulSoup(i, 'html.parser')
  indexContent = str(soup)
  isDivThere = soup.find('div', {'class': 'home-content'})
  statusDiv = bool(isDivThere)
with open(headPartial) as h:
  soup = BeautifulSoup(h, 'html.parser')
  headContent = str(soup)
  isHeadThere = soup.find('script')
  statusScript = bool(isHeadThere)

if not statusDiv:
  with open(indexPartial, 'r') as i:
    lines = i.readlines()
    # index is 15 for 16th line
    writeToLine(lines, 15, newHomeContent)
  with open(indexPartial, 'w') as i:
    i.writelines(lines)
  appendToFile(customCss, mainCss, '.pure-g.home {display:none !important;} .pure-menu-children {-webkit-box-shadow: 2px 2px 15px 0px rgba(50,50,50,.1); -moz-box-shadow: 2px 2px 15px 0px rgba(50,50,50,.1); box-shadow: 2px 2px 15px 0px rgba(50,50,50,.1); }')
if not statusScript:
  with open(headPartial, 'r') as h:
    lines = h.readlines()
    writeToLine(lines, 1, newHeadContent)
  with open(headPartial, 'w') as h:
    h.writelines(lines)

# Change Button and Link on Banner
oldButtonLink = 'become-a-sponsor'
newButtonLink = 'donate'
oldButtonText = 'home_hero_sponsor'
newButtonText = 'home_hero_donate'

replaceString(indexPartial, oldButtonLink, newButtonLink)
replaceString(indexPartial, oldButtonText, newButtonText)


print "done"