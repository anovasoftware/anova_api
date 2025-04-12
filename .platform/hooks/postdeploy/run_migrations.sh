#!/bin/bash
echo "Running Django Migrations and Loading Data..."

# Ensure the script exits if any command fails
set -e

# Navigate to the application directory
cd /var/app/current

# Activate the virtual environment
#source ~/venv/bin/activate
source /var/app/venv/staging-LQM1lest/bin/activate


# Run migrations
python manage.py migrate authtoken
python manage.py migrate static
python manage.py migrate base
python manage.py migrate res
python manage.py migrate bridge


# Load data
python manage.py loaddata static.json
python manage.py loaddata static.json
python manage.py loaddata base.json
python manage.py loaddata res.json
python manage.py loaddata bridge.json
python manage.py loaddata authtoken_token.json

echo "Migrations and Data Load Complete!"
