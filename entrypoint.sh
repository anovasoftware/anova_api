#!/bin/sh

echo "Waiting for PostgreSQL..."
until nc -z postgres 5432; do sleep 2; done

echo "Running migrations..."
python manage.py migrate --noinput
python manage.py migrate authtoken

echo "Loading static data..."
python manage.py loaddata static

echo "Starting Gunicorn..."
exec gunicorn anova_api.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
