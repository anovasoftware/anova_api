@echo off
echo Running Django Migrations and Loading Data...
cd /d C:\projects3\anova_api  REM Change to the correct path of your Django app

REM Activate virtual environment
call c:\Projects3\anova_api\.venv\Scripts\activate.bat   REM Adjust to your actual venv path

REM Run migrations
python manage.py migrate static
python manage.py migrate base

REM Load data
python manage.py loaddata static.json
python manage.py loaddata base.json

echo Migrations and Data Load Complete!
