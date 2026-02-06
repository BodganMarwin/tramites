#!/bin/sh
set -e

# Wait for DB if POSTGRES_HOST is provided
if [ -n "$POSTGRES_HOST" ]; then
  echo "Waiting for postgres..."
  until nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.5
  done
fi

# Apply database migrations
echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate --noinput

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput
# Create superuser if not exists
python manage.py createsuperuser --noinput || true

python manage.py shell -c "
from django.contrib.auth import get_user_model;
import os
User = get_user_model();
u, created = User.objects.get_or_create(
    username=os.environ['DJANGO_SUPERUSER_USERNAME'],
    email=os.environ['DJANGO_SUPERUSER_EMAIL']
)
u.set_password(os.environ['DJANGO_SUPERUSER_PASSWORD'])
u.is_superuser = True
u.is_staff = True
u.save()
"
echo "Superuser created or already exists."

# Run the command passed to the docker container
exec "$@"
