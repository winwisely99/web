#!/usr/bin/python3

from bs4 import BeautifulSoup
import os.path
import shutil

'''
Super Duper Importer
'''

###################################
# Paths and Directories
###################################

goldenRoot = 'golden/'
leRoot = 'resources/website/'
leImages = 'resources/website/static/images/'


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
  print(nameDir + ' directory updated successfully!')

# Delete directory
def deleteDirectory(nameDir,rmDir):
  if os.path.exists(rmDir):
    shutil.rmtree(rmDir)
    print(nameDir + ' directory deleted successfuly!')

# Copy file
def placeFile(nameFile, srcFile, destFile):
  from shutil import copyfile
  shutil.copyfile(srcFile,destFile)

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

# Copy the Golden IMAGE files into the LE 'static' dir
src = goldenRoot + 'images/'
dest = leImages
srcFiles = os.listdir(src)

for file in srcFiles:
  srcFile = os.path.join(src, file)
  destFile = os.path.join(dest, file)
  shutil.copyfile(srcFile, destFile)
  print(file + ' updated successfully!')

# Replace the Golden LE CONTENT/EN dir with the WW CONTENT/EN dir only
srcContent = 'golden/content/en'
destContent = leRoot + 'content/en'
placeDirectory('Content',srcContent,destContent)

# Replace the Golden LE CONFIG dir with the WW content dir
srcConfig = 'golden/config'
destConfig = leRoot + 'config'
placeDirectory('Config',srcConfig,destConfig)

# Delete LE git directory, it doesnt need to be there
gitDir = leRoot + '.git'
deleteDirectory('LE Git folder',gitDir)


###################################
# Layout Only
###################################

# Replace file favicon
srcFavicon = 'golden/images/favicon.ico'
destFavicon = leRoot + 'static/favicon.ico'
placeFile('Favicon', srcFavicon, destFavicon)

### Head Partial #####

headHtml = leRoot + 'layouts/partials/head.html'
oldMetaTwitter = '@letsencrypt'
newMetaTwitter = '@winwisely'
oldMetaLogo = 'images/le-logo-twitter.png'
newMetaLogo = 'wwimages/logo-main.png'
replaceString(headHtml, oldMetaTwitter, newMetaTwitter)
replaceString(headHtml, oldMetaLogo, newMetaLogo)

### Header Partial #####

# Replace logo and alt text
headerHtml = leRoot + 'layouts/partials/header.html'
footerHtml = leRoot + 'layouts/partials/footer.html'
oldLogo = '/images/letsencrypt-logo-horizontal.svg'
newLogo = '/images/logo-main.png'
oldAlt = 'Let\'s Encrypt'
newAlt = 'GetCourageNow'
replaceString(headerHtml, oldLogo, newLogo)
replaceString(headerHtml, oldAlt, newAlt)

# Remove hideous foundation link
deleteElement(headerHtml, 'div', 'class', 'linux-foundation-link')

# Remove their LE GA link
replaceString(footerHtml,'<script async src="https://www.googletagmanager.com/gtag/js?id=UA-56433935-1&aip=1"></script>','')

# Replace banner on homepage
mainCss = leRoot + 'static/css/main.min.css'
oldBanner = '/images/3.jpg'
newBanner = '/images/1-dark.jpg'
replaceString(mainCss, oldBanner, newBanner)

# Replace banner on child pages
heroHtml = leRoot + 'layouts/partials/hero.html'
# oldHero = 'images/%d.jpg'
# newHero = 'images/%d.jpg'
# replaceString(heroHtml, oldHero, newHero)

# Change banner text
i18nEN = leRoot + 'i18n/en.toml'
oldHeroTitle = 'Let&rsquo;s Encrypt is a <span>free</span>, <span>automated</span>, and <span>open</span> Certificate Authority.'
newHeroTitle = '<span>GetCourageNow</span><br>It&rsquo;s A Numbers Game'
replaceString(i18nEN, oldHeroTitle, newHeroTitle)

### Footer Partial #####

# Replace contact footer text
footerHtml = leRoot + 'layouts/partials/footer.html'
oldAddress1 = '1 Letterman Drive, Suite D4700,'
newAddress1 = '(650) 383 8435 | gary@getcouragenow.org'
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
customFirebase = 'golden/layouts/firebase.txt'

indexPartial = leRoot + 'layouts/index.html'
headPartial = leRoot + 'layouts/partials/head.html'
basePartial = leRoot + 'layouts/_default/baseof.html'
blankPartial = leRoot + 'layouts/_default/blank.html'
postPartial = leRoot + 'layouts/post/baseof.html'

with open(customHome) as home:
  soup = BeautifulSoup(home, 'html.parser')
  newHomeContent = str(soup)
with open(customCss) as css:
  soup = BeautifulSoup(css, 'html.parser')
  newCssContent = str(soup)
with open(customHead) as head:
  soup = BeautifulSoup(head, 'html.parser')
  newHeadContent = str(soup)
with open(customFirebase) as base:
  soup = BeautifulSoup(base, 'html.parser')
  newFirebaseContent = str(soup)

with open(indexPartial) as i:
  soup = BeautifulSoup(i, 'html.parser')
  indexContent = str(soup)
  isDivThere = soup.find('div', {'class': 'home-content'})
  statusDiv = bool(isDivThere)
with open(headPartial) as p:
  soup = BeautifulSoup(p, 'html.parser')
  headContent = str(soup)
  isScriptThere = soup.find('script')
  statusScript = bool(isScriptThere)
with open(basePartial) as p:
  soup = BeautifulSoup(p, 'html.parser')
  baseContent = str(soup)
  isScriptThere = soup.find('script')
  statusScript1 = bool(isScriptThere)
with open(blankPartial) as p:
  soup = BeautifulSoup(p, 'html.parser')
  blankContent = str(soup)
  isScriptThere = soup.find('script')
  statusScript2 = bool(isScriptThere)
with open(postPartial) as p:
  soup = BeautifulSoup(p, 'html.parser')
  postContent = str(soup)
  isScriptThere = soup.find('script')
  statusScript3 = bool(isScriptThere)

if not statusDiv:
  with open(indexPartial, 'r') as i:
    lines = i.readlines()
    # index is 15 for 16th line
    writeToLine(lines, 15, newHomeContent)
  with open(indexPartial, 'w') as i:
    i.writelines(lines)
  appendToFile(customCss, mainCss, newCssContent)

# Import Scripts

if not statusScript:
  with open(headPartial, 'r') as h:
    lines = h.readlines()
    writeToLine(lines, 1, newHeadContent)
  with open(headPartial, 'w') as h:
    h.writelines(lines)

  with open(basePartial, 'r') as h:
    lines = h.readlines()
    writeToLine(lines, 16, newFirebaseContent)
  with open(basePartial, 'w') as h:
    h.writelines(lines)

  with open(blankPartial, 'r') as h:
    lines = h.readlines()
    writeToLine(lines, 4, newFirebaseContent)
  with open(blankPartial, 'w') as h:
    h.writelines(lines)

  with open(postPartial, 'r') as h:
    lines = h.readlines()
    writeToLine(lines, 13, newFirebaseContent)
  with open(postPartial, 'w') as h:
    h.writelines(lines)


# Change Button and Link on Banner
oldButtonLink = 'become-a-sponsor'
newButtonLink = 'donate'
oldButtonText = 'home_hero_sponsor'
newButtonText = 'home_hero_donate'

replaceString(indexPartial, oldButtonLink, newButtonLink)
replaceString(indexPartial, oldButtonText, newButtonText)

print("Done")







