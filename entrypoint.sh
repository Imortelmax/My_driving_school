#!/bin/sh
set -e

mkdir -p /app/data

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py loaddata school/fixtures/initial_data.json || true

exec gunicorn driving_school.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --timeout 120
