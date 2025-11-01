#!/usr/bin/env bash
echo "Running Django migrations and loading data..."
set -e  # exit on any failure

# Navigate to the app directory (Render mounts code at /opt/render/project/src)
cd /opt/render/project/src

# (No venv activation needed — Render already runs inside its own Python environment)

# Run migrations
python manage.py migrate authtoken
python manage.py migrate static
python manage.py migrate base
python manage.py migrate res
python manage.py migrate bridge

# Load data (deduplicate static.json)
python manage.py loaddata static.json
python manage.py loaddata base.json
python manage.py loaddata res.json
python manage.py loaddata bridge.json
python manage.py loaddata authtoken_token.json

echo "Migrations and data load complete!"
