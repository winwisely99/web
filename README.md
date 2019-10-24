######
WinWisely Squarespace-to-Hugo Migration Project
######

Import.py is for migrating original WinWisely squarespace content into the Let's Encrypt Hugo Template `<https://github.com/letsencrypt/website>`

By default it will try to replace:
- config files
- content i18n files
- images
- specific strings in the layout directory

Getting started
===============
 * Run Makefile in the console from the checked out root of WinWisely

Runtime dependencies
====================
 * `Python <http://python.org/>`_ 2.6, 2.7, ???
 * `Beautiful soup <http://www.crummy.com/software/BeautifulSoup/>`_ : Parsing and downloading of post images/attachments (python)

Installing dependencies in ubuntu/debian, mac terminal
----------------------------------------

   ``sudo apt-get install python-bs4``

Installing Python dependencies using python package installer (pip)
-------------------------------------------------------------------

From the checked out root for this project, type:

   ``sudo pip install --upgrade  -r Import_requirements.txt``

Configuration/Customization
===========================

All content edits should be done in 'golden' folder only.
Run 'Makefile modify' in console to see in local installation


