import os
import django
from django.core.management import execute_from_command_line

def run_migrations():
    """Run migrations automatically when the server starts"""
    try:
        print("Running database migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        print("Migrations completed successfully!")
    except Exception as e:
        print(f"Migration error: {e}")
        # Continue anyway to avoid blocking the server

# Run migrations when this module is imported
if __name__ != '__main__':
    run_migrations()
