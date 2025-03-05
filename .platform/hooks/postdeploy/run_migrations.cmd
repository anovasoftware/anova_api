@echo off
echo Running Django Migrations and Loading Data...
cd /d C:\cfn\cfn-init  REM Change to the correct path of your Django app

REM Activate virtual environment
call C:\cfn\Python39\Scripts\activate.bat  REM Adjust to your actual venv path

REM Run migrations
python manage.py migrate static
python manage.py migrate base

REM Load data
python manage.py loaddata static.json
python manage.py loaddata base.json

echo Migrations and Data Load Complete!
