import os
import django
from django.core.management import execute_from_command_line
import socket

def run_migrations():
    """Run migrations automatically when the server starts"""
    try:
        print("Running database migrations...")
        
        # Check if we're in production
        if os.environ.get('DJANGO_DEBUG', 'True').lower() == 'false':
            # Test DNS resolution first
            db_host = os.environ.get('DB_HOST', 'localhost')
            print(f"Testing DNS resolution for {db_host}")
            
            try:
                socket.gethostbyname(db_host)
                print(f"DNS resolution successful for {db_host}")
            except socket.gaierror as e:
                print(f"DNS resolution failed for {db_host}: {e}")
                print("Skipping migrations due to DNS error.")
                return
        
        execute_from_command_line(['manage.py', 'migrate'])
        print("Migrations completed successfully!")
        
    except Exception as e:
        print(f"Migration error: {e}")
        # Continue anyway to avoid blocking the server

# Run migrations when this module is imported
if __name__ != '__main__':
    run_migrations()
