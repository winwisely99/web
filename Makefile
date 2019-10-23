



# SOURCE
# https://github.com/letsencrypt/website

#Change this before proceding to reflect environment

# dyan
GOPATH=/Users/dyan/Sites/Clients/winwisely.org
# joe
#GOPATH=/Users/apple/workspace/go/src/github.com/winwisely99/web
# rosie
#GOPATH=/Users/rosiehoberg/workspace/winwisely/web

LIB_NAME=website
LIB=resources/$(LIB_NAME)
LIB_BRANCH=dev
#LIB_BRANCH=flutter_web
LIB_FSPATH=$(GOPATH)/$(LIB)



print:
	@echo
	@echo LIB_NAME: $(LIB_NAME)
	@echo LIB: $(LIB)
	@echo LIB_BRANCH: $(LIB_BRANCH)
	@echo LIB_FSPATH: $(LIB_FSPATH)
	@echo

git-print:
	cd $(LIB_FSPATH) && git status
git-clone:
	mkdir -p $(LIB_FSPATH)
	cd $(LIB_FSPATH) && cd .. && rm -rf $(LIB_NAME) && git clone https://git@$(LIB).git
	cd $(LIB_FSPATH) && git checkout -b $(LIB_BRANCH)
git-pull:
	cd $(LIB_FSPATH) && git pull
git-clean:
	rm -rf $(LIB_FSPATH)

code:
	code $(LIB_FSPATH)

run:
	cd $(LIB_FSPATH) && hugo server -F
build:
	cd $(LIB_FSPATH) && hugo server -D
	ls -al $(LIB_FSPATH)/public

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
	./Import.py


### deploy ( not using )
GCLOUD_PROJ_ID=winwisely-web-example-letencrypt
deploy-gc:
	# see: https://stephenmann.io/post/hosting-a-hugo-site-in-a-google-bucket/
	
	# create proj
	gcloud projects create $(GCLOUD_PROJ_ID)
	gcloud config set project $(GCLOUD_PROJ_ID)
	gsutil mb gs://example.winwisely.org/

	#cd $(LIB_FSPATH) && hugo deploy -h

# Deploy to Firebase ( using this for ease for now )

# PROD
PROD_FB_PROJ_ID=winwisely-getcourage-org
# DEV
FB_PROJ_ID=winwisely-letsencrypt-web

FB_PROJ_CONSOLEURL=https://console.firebase.google.com/project/$(PROD_FB_PROJ_ID)
deploy-fb:
	# 1. ONE TIME: make the project here:https://console.firebase.google.com/
	# web console:  https://console.firebase.google.com/project/winwisely-web-letencrypt/overview
	#

	firebase init 

	firebase login --no-localhost
	
	cd $(LIB_FSPATH)
	hugo
	rm -R ./public
	cp -R $(LIB_FSPATH)/public ./public
	firebase deploy
