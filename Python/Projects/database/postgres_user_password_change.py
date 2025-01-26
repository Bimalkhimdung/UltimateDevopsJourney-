import os
import django
from django.contrib.auth.hashers import make_password

# Django setting location

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

new_password = 'realhrsoft'
static_salt = 'fixedsalt'

hashed_password = make_password(new_password,salt=static_salt)

print(hashed_password)

#aayulogic = 'pbkdf2_sha256$260000$fixedsalt$wkZjsBGJnOsCOA4AOokZ2ZPL0I3YqtIkII1th50TVvk='
#reahrsoft = 'pbkdf2_sha256$260000$V8oiIdp0Wk6xKkzDcTyTRC$cvyOom6vxU3kV9RaWP1WRm7Mjg2e9zIepNnJWxsAJJ0='