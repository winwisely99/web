

# https://github.com/winwisely99/web


LIB_NAME=web
LIB=github.com/winwisely99/$(LIB_NAME)
LIB_BRANCH=master
LIB_FSPATH=$(GOPATH)/src/$(LIB)



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
	cd $(LIB_FSPATH) && cd .. && rm -rf $(LIB_NAME) && git clone ssh://git@$(LIB).git
	cd $(LIB_FSPATH) && git checkout $(LIB_BRANCH)
git-pull:
	cd $(LIB_FSPATH) && git pull
git-clean:
	rm -rf $(LIB_FSPATH)

###

dep:
	# hugo
	brew install hugo

	# firebase cli

	## gcloud
	brew cask install google-cloud-sdk

### deploy
GCLOUD_PROJ_ID=winwisely-web-example-letencrypt
deploy-gc:
	# see: https://stephenmann.io/post/hosting-a-hugo-site-in-a-google-bucket/
	
	# create proj
	gcloud projects create $(GCLOUD_PROJ_ID)
	gcloud config set project $(GCLOUD_PROJ_ID)
	gsutil mb gs://example.winwisely.org/

	#cd $(LIB_FSPATH) && hugo deploy -h


FB_PROJ_ID=winwisely-web-letencrypt
FB_PROJ_CONSOLEURL=https://console.firebase.google.com/project/$(FB_PROJ_ID)
deploy-fb:
	# 1. ONE TIME: make the project here:https://console.firebase.google.com/
	# web console:  https://console.firebase.google.com/project/winwisely-web-letencrypt/overview
	#brew install firebase-cli
	#firebase init 

	firebase login --no-localhost
	
	# 3 deploy
	cd $(LIB_FSPATH) & hugo
	cp $(LIB_FSPATH)/public ./public
