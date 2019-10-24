# WinWisely Squarespace-to-Hugo Migration Project

This is a small business template built with [Hugo](https://github.com/gohugoio/hugo) based on [Let's Encrypt](https://github.com/letsencrypt) using content exported from Squarespace.  

## Getting started

`Download <https://github.com/winwisely99/web/dev>`_ or clone using ``git clone https://github.com/winwisely99/web.git``

- Run 'git fetch' and 'git checkout dev' to be on the correct branch

#### Runtime dependencies
 * `Python <http://python.org/>`_ 2.6, 2.7, ???
 * `Beautiful soup <http://www.crummy.com/software/BeautifulSoup/>`_ : Parsing and downloading of post images/attachments (python)

#### Manually installing dependencies in ubuntu/debian, mac
   ``$ apt-get install python-bs4 (for Python 2)``
   ``$ apt-get install python3-bs4 (for Python 3)``

#### Manually installing dependencies in mac

   ``$ brew install python-bs4``

####  Manually installing Python dependencies using python package installer (pip)

From the checked out root for this project, type:

   ``$ sudo pip install --upgrade  -r Import_requirements.txt``

## Local Development

*Makefile* has all the commands necessary for building, starting server, and deploying to Firebase.  CD into the checked out directory of [WinWisely](https://github.com/winwisely99/web.git)

- Change $GOPATH variable in *Makefile* to match your local checked out directory of [WinWisely](https://github.com/winwisely99/web.git)

- Run `$ make dep` to install all dependencies

- Run `$ make git-clean'` to clean Let's Encrypt base directory when necessary
  - Run `$ make git-upstream` to pull Let's Encrypt repo if base directory is cleaned
- Or run `$ make git-update` to update Let's Encrypt's repo

In checked out root of WinWisely:

- Run `$ make modify` to invoke Import.py script. 

  By default it will try to replace:
    - config files
    - content i18n files
    - images
    - specific strings in the layout directory 

- Run `$ make build` to build after importing WinWisely content into Let's Encrypt base

- Run `$ make run` to start the server

- Run `$ make open` to launch browser to see the build locally

## Modifying Content

**All content changes, adding languages, modifying menu, etc. must be done in _golden_ directory.**

The _golden_ directory contains:
- _hidden:
  - Let's Encrypt files that we are not using
- config:
  - General configuration settings
  - Languages
  - Menu
- content:
  - All the markdown files for the content.  Structure matters. (Please only add directories or files if intended for publishing.)
- images:
  - These images will be copied into the build
- layouts:
  - The files here are used for custom HTML, CSS, Script that need to be injected or appended into appropriate partials. (See Import.py for usage)

## Deployment

- Run `$ make modify` to import all changes into Let's Encrypt base
- Run `$ make build` to rebuild Hugo
- If first time deploying:
  - Run `$ make deploy-fb-init`
- Run `$ make deploy-fb` to deploy build to Dev server located at [https://winwisely-letsencrypt-web.firebaseapp.com/](https://winwisely-letsencrypt-web.firebaseapp.com/)

