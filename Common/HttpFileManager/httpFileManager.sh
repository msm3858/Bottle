#! /bin/bash

export WORKON_HOME=/home/msm/Programming/Bottle/venv
export PYTHONPATH="${PYTHONPATH}:/home/msm/Programming/Bottle/"

source ${WORKON_HOME}/mediapadBackend/bin/activate

WEB_SERVER_PORT=5000
FS_HOST=localhost


python /home/msm/PycharmProjects/BottleNew/Common/HttpFileManager/httpFileManager.py -i ${FS_HOST} -p ${WEB_SERVER_PORT}

exit $?