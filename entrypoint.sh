#!/bin/sh

export SUPERUSER_NAME
export SUPERUSER_EMAIL
export SUPERUSER_PASSWORD

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000 &

sleep 5

python3 manage.py shell << EOF
from django.contrib.auth import get_user_model
import os

User = get_user_model()
superuser_name = os.getenv('SUPERUSER_NAME')
superuser_email = os.getenv('SUPERUSER_EMAIL')
superuser_password = os.getenv('SUPERUSER_PASSWORD')

if not User.objects.filter(username=superuser_name).exists():
    User.objects.create_superuser(superuser_name, superuser_email, superuser_password)
    print(f"Superuser '{superuser_name}' has been successfully created.")
else:
    print(f"User '{superuser_name}' already exists. Skipping superuser creation.")
EOF

wait