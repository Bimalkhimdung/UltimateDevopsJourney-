import os
import django
from django.contrib.auth.hashers import make_password

# Django setting location

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

new_password = 'realhrsoft'
static_salt = 'fixedsalt'

hashed_password = make_password(new_password,salt=static_salt)

print(f"Hashed password: {hashed_password}")