

# https://github.com/letsencrypt/website


LIB_NAME=website
LIB=github.com/letsencrypt/$(LIB_NAME)
LIB_BRANCH=desktop
#LIB_BRANCH=flutter_web
#LIB_BRANCH=master
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

code:
	code $(LIB_FSPATH)

run:
	cd $(LIB_FSPATH) && hugo server -F
build:
	cd $(LIB_FSPATH) && hugo server -D
	ls -al $(LIB_FSPATH)/public

open:
	open http://localhost:1313/




