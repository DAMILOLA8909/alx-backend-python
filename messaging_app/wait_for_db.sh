#!/bin/bash
# Wait for MySQL
echo "Waiting for MySQL..."
while ! nc -z db 3306; do
  sleep 1
done
echo "MySQL is ready!"

# Run Django commands
python manage.py migrate
python manage.py collectstatic --noinput
exec gunicorn messaging_app.wsgi:application --bind 0.0.0.0:8000
