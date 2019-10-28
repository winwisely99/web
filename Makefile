# SOURCE
# https://github.com/letsencrypt/website

#Change this before proceding to reflect environment

# dyan
GOPATH=/Users/dyan/Sites/Clients/getcourage.org

# joe
#GOPATH=/Users/apple/workspace/go/src/github.com/winwisely99/web
# rosie
#GOPATH=/Users/rosiehoberg/workspace/winwisely`/web


LIB_NAME=website
LIB=resources/$(LIB_NAME)
LIB_BRANCH=dev
#LIB_BRANCH=flutter_web
LIB_FSPATH=$(GOPATH)/$(LIB)
LE_REPO=https://github.com/letsencrypt/website.git

print:
	@echo
	@echo LIB_NAME: $(LIB_NAME)
	@echo LIB: $(LIB)
	@echo LIB_BRANCH: $(LIB_BRANCH)
	@echo LIB_FSPATH: $(LIB_FSPATH)
	@echo

git-print:
	cd $(LIB_FSPATH) && git status

git-clean:
	rm -rf $(LIB_FSPATH)

git-upstream:
	cd $(GOPATH)/resources && git clone $(LE_REPO)

git-update:
	cd $(LIB_FSPATH) && git pull origin master
	
code:
	code $(LIB_FSPATH)

run:
	cd $(LIB_FSPATH) && hugo server -F

open:
	open http://localhost:1313/

###

dep:
	# hugo
	brew install hugo

	# firebase cli
	brew install firebase-cli

	## gcloud
	brew cask install google-cloud-sdk

	## python ( https://docs.python-guide.org/starting/install3/osx/)
	brew install python
	# python3 --version
	
	# pip
	pip3 install BeautifulSoup4


modify:
	# This invokes the monster modification script
	python $(GOPATH)/Import.py

build:
	cd $(LIB_FSPATH) && hugo
	ls -al $(LIB_FSPATH)/public


### deploy ( not using )
GCLOUD_PROJ_ID=getcourage-web-example-letencrypt
deploy-gc:
	# see: https://stephenmann.io/post/hosting-a-hugo-site-in-a-google-bucket/
	
	# create proj
	gcloud projects create $(GCLOUD_PROJ_ID)
	gcloud config set project $(GCLOUD_PROJ_ID)
	gsutil mb gs://example.getcouragenow.org/
	#cd $(LIB_FSPATH) && hugo deploy -h

# Deploy to Firebase ( using this for ease for now )

# TOGGLE environment:
# PROD
PROD_FB_PROJ_ID=getcourage-getcourage-org
# DEV
DEV_FB_PROJ_ID=getcourage-letsencrypt-web

FB_PROJ_CONSOLEURL=https://console.firebase.google.com/project/$(PROD_FB_PROJ_ID)

deploy-fb-init:
	# 1. ONE TIME: make the project here:https://console.firebase.google.com/
	# web console:  https://console.firebase.google.com/project/getcourage-web-letencrypt/overview

	#firebase init 
	firebase init 

	# firebase login
	firebase login --no-localhost

deploy-fb-console:
	# opens the web console.
	open $(FB_PROJ_CONSOLEURL)

deploy-fb:
	# rebuilds hugo and copies output directory to root of deployment
	cd $(LIB_FSPATH) && hugo -D
	ls -al $(LIB_FSPATH)/public
	# does the actual push deploy to their server.
	rm -R ./public
	cp -R $(LIB_FSPATH)/public ./public
	firebase deploy


