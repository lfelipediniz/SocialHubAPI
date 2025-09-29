#!/usr/bin/env python3
import os
import psycopg
from decouple import config

def test_connection():
    print("=== Testing Database Connection ===")
    
    # Get environment variables
    db_host = config('DB_HOST', default='localhost')
    db_port = config('DB_PORT', default='5432')
    db_name = config('DB_NAME', default='dbsocialhub')
    db_user = config('DB_USER', default='dbsocialhub_user')
    db_password = config('DB_PASSWORD', default='')
    
    print(f"Host: {db_host}")
    print(f"Port: {db_port}")
    print(f"Database: {db_name}")
    print(f"User: {db_user}")
    print(f"Password: {'*' * len(db_password) if db_password else 'EMPTY'}")
    print(f"Password length: {len(db_password)}")
    
    # Test connection
    try:
        conn = psycopg.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password,
            sslmode='require'
        )
        print("✅ Connection successful!")
        conn.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        
        # Try with different password variations
        print("\n=== Trying password variations ===")
        
        # Try with the password you provided
        test_password = "ThskOnLy0KKXqRjK3MyAv1STbF7DDgos"
        print(f"Trying password: {test_password}")
        try:
            conn = psycopg.connect(
                host=db_host,
                port=db_port,
                dbname=db_name,
                user=db_user,
                password=test_password,
                sslmode='require'
            )
            print("✅ Connection successful with provided password!")
            conn.close()
        except Exception as e2:
            print(f"❌ Still failed: {e2}")

if __name__ == "__main__":
    test_connection()
