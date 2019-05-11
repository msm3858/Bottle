#! /bin/bash

export WORKON_HOME=~/PycharmProjects/BottleFramework/

source ${WORKON_HOME}/venv/bin/activate

WEB_SERVER_PORT=5000
FS_HOST=localhost


# call
python ${WORKON_HOME}/httpFileManager.py  -i ${FS_HOST} -p ${WEB_SERVER_PORT}