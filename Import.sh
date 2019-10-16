#!/bin/sh


# Paths

## golden directories
GIMAGES=./golden/assets/images
GROOT=./golden/winwisely.org

## le directories
LEIMAGES=src/github.com/letsencrypt/website/static/images
LEROOT=src/github.com/letsencrypt/website

# Layout Partials

## find & replace main logo
LOGOOLD=/images/letsencrypt-logo-horizontal.svg
LOGONEW=$GIMAGES/logo-main.png
sed -i "" "s|$LOGOOLD|$LOGONEW|g" $LEROOT/layouts/partials/header.html

# remove linx foundation link
STRING_LINUX=


