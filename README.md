# WinWisely Squarespace-to-Hugo Migration Project

This is a small business template built with [Hugo](https://github.com/gohugoio/hugo) based on [Let's Encrypt](https://github.com/letsencrypt) using content exported from Squarespace.  

## Getting started

`Download <https://github.com/winwisely99/web/>`_ or clone using ``git clone https://github.com/winwisely99/web.git``

- Run `$ git fetch` and `$ git checkout dev` to be on the correct branch

## Local Development

*Makefile* has all the commands necessary for building, starting server, and deploying to Firebase and must be executed in root directory of [WinWisely](https://github.com/winwisely99/web.git)

- Change $GOPATH variable in *Makefile* to match your local checked out path

From the checked out root, type in terminal or command line:

- Run `$ make dep` to install all dependencies 
   
  - #### Runtime dependencies (if 'make dep' fails)
  
    - `Python <http://python.org/>`_ 2.6, 2.7, ???
    - `Beautiful soup <http://www.crummy.com/software/BeautifulSoup/>`_ : Parsing HTML/Text/Css files (python)
    - `Firebase <https://firebase.google.com/>`
    - `Hugo <https://gohugo.io/getting-started/installing/>`

  - #### Manually installing dependencies in ubuntu/debian, mac
  
      ``$ apt-get install python-bs4 (for Python 2)``
   
      ``$ apt-get install python3-bs4 (for Python 3)``

  - #### Manually installing dependencies in mac
  
      ``$ brew install hugo``
      
      ``$ brew install firebase-cli``
      
      ``$ brew install python3``
      
      ``$ pip3 install BeautifulSoup4``      

  - ####  Manually installing Python dependencies using python package installer (pip)
  
      ``$ sudo pip install --upgrade  -r Import_requirements.txt``


- Run `$ make git-clean` to clean Let's Encrypt codebase directory when necessary
  - Run `$ make git-upstream` to pull Let's Encrypt repo if codebase directory is cleaned
- Or run `$ make git-update` to update Let's Encrypt's codebase directory

To import WinWisely content into the Let's Encrypt codebase:

- Run `$ make modify` to invoke Import.py script. 

  By default it will replace, overwrite, or append to Let's Encrypt codebase:
    - config files
    - content i18n files
    - images
    - specific strings in the layout directory 

- Run `$ make build` to build after importing WinWisely content into Let's Encrypt codebase

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
  
After every change, add, or delete:
- Run `$ make modify` to import all changes into Let's Encrypt base

## Deployment

- Run `$ make build` to rebuild Hugo
- If first time deploying:
  - Run `$ make deploy-fb-init`
- Run `$ make deploy-fb` to deploy build to Dev server located at [https://winwisely-letsencrypt-web.firebaseapp.com/](https://winwisely-letsencrypt-web.firebaseapp.com/)

