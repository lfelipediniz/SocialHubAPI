"""
WSGI config for codeleap_careers project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialhubapi.settings')

# Import auto_migrate to run migrations automatically
import auto_migrate

application = get_wsgi_application()
