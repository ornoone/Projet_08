#!/bin/sh

cd Projet_08
git pull
python3.8 manage.py collectstatic
python3.8 manage.py migrate
/usr/bin/supervisorctl restart projet_08-gunicorn

