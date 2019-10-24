######
WinWisely Squarespace-to-Hugo Migration Project
######

This is a small business template built with [Hugo](https://github.com/gohugoio/hugo) based on [Let's Encrypt](https://github.com/letsencrypt) using content exported from Squarespace.  

## Getting started

Clone [WinWisely](https://github.com/winwisely99/web.git) into your local workspace

- Run 'git fetch' and 'git checkout dev' to be on the correct branch

*Makefile* has all the commands necessary for building, starting server, and deploying to Firebase.  CD into the checked out directory of [WinWisely](https://github.com/winwisely99/web.git)

- Change $GOPATH variable to match your local checked out directory of [WinWisely](https://github.com/winwisely99/web.git)

- Run 'make git-clone' to clone Let's Encrypt's build into checked out directory of [WinWisely](https://github.com/winwisely99/web.git)

## Local Development

- Run 'make modify' to invoke Import.py script. 

By default it will try to replace:

  - config files
  - content i18n files
  - images
  - specific strings in the layout directory 

- Run 'make build' to build after importing WinWisely content into Let's Encrypt base

- Run 'make run' to start the server

- Run 'make open' to launch browser to see the build locally

## Modifying Content

*All content changes, adding languages, modifying menu, etc. must be done in _golden_ directory.*

The _golden_ directory contains:
- _hidden
  - Let's Encrypt files that we are not using
- config
  - General configuration settings
  - Languages
  - Menu
- content
  - All the markdown files for the content.  Structure matters. (Please only add directories or files if intended for publishing.)
- images
  - These images will be copied into the build
- layouts
  - The files here are used for custom HTML, CSS, Script that need to be injected or appened into appropriate partials. (See Import.py for usage)

## Deployment

- Run 'make modify' to import all changes into Let's Encrypt base
- Run 'make build' to rebuild Hugo
- If first time deploying:
  - Run 'make deploy-fb-init'
- Run 'make deploy-fb' to deploy to DEV server located at [WinWisely Firebase](https://winwisely-letsencrypt-web.firebaseapp.com/)

