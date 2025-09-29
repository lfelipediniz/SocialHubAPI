#!/usr/bin/env python3
import os
from decouple import config

def debug_env():
    print("=== Environment Variables Debug ===")
    
    # Check if we're in production
    debug = os.environ.get('DJANGO_DEBUG', 'True')
    print(f"DJANGO_DEBUG: {debug}")
    
    # Database variables
    db_host = config('DB_HOST', default='localhost')
    db_port = config('DB_PORT', default='5432')
    db_name = config('DB_NAME', default='dbsocialhub')
    db_user = config('DB_USER', default='dbsocialhub_user')
    db_password = config('DB_PASSWORD', default='')
    
    print(f"DB_HOST: {db_host}")
    print(f"DB_PORT: {db_port}")
    print(f"DB_NAME: {db_name}")
    print(f"DB_USER: {db_user}")
    print(f"DB_PASSWORD: {'*' * len(db_password) if db_password else 'EMPTY'}")
    print(f"DB_PASSWORD length: {len(db_password)}")
    
    # Show first and last characters of password for debugging
    if db_password:
        print(f"DB_PASSWORD first char: '{db_password[0]}'")
        print(f"DB_PASSWORD last char: '{db_password[-1]}'")
        print(f"DB_PASSWORD chars: {[ord(c) for c in db_password[:5]]}")
    
    # Check DATABASE_URL
    database_url = config('DATABASE_URL', default='')
    print(f"DATABASE_URL: {database_url[:50]}..." if len(database_url) > 50 else f"DATABASE_URL: {database_url}")

if __name__ == "__main__":
    debug_env()
