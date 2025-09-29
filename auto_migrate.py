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
            # Debug environment variables
            from decouple import config
            db_host = config('DB_HOST', default='localhost')
            db_user = config('DB_USER', default='dbsocialhub_user')
            db_password = config('DB_PASSWORD', default='')
            
            print(f"DB_HOST: {db_host}")
            print(f"DB_USER: {db_user}")
            print(f"DB_PASSWORD length: {len(db_password)}")
            if db_password:
                print(f"DB_PASSWORD first char: '{db_password[0]}'")
                print(f"DB_PASSWORD last char: '{db_password[-1]}'")
                print(f"DB_PASSWORD repr: {repr(db_password)}")
                
                # Test with the exact password you provided
                expected_password = "ThskOnLy0KKXqRjK3MyAv1STbF7DDgos"
                print(f"Expected password: {repr(expected_password)}")
                print(f"Passwords match: {db_password == expected_password}")
                
                # Show character by character comparison
                if len(db_password) == len(expected_password):
                    for i, (actual, expected) in enumerate(zip(db_password, expected_password)):
                        if actual != expected:
                            print(f"Difference at position {i}: got '{actual}' (ord {ord(actual)}), expected '{expected}' (ord {ord(expected)})")
                            break
                    else:
                        print("Passwords are identical character by character")
                else:
                    print(f"Length mismatch: got {len(db_password)}, expected {len(expected_password)}")
            
            # Test DNS resolution first
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
