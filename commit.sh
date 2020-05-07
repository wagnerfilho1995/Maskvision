#!/bin/bash
  if [ $# -lt 1 ];
  then
   echo "Precisa fornecer a descrição do commit"
   exit 1
 fi
git status
git add .
git commit -am "$*"
git push heroku master