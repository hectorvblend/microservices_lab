#!/usr/bin/env python3
'''
This file is used to store all the environment variables.
'''
import os

if not os.getenv('ENVIRONMENT', False):
    from dotenv import load_dotenv
    load_dotenv('./env',)

# Server settings:
localhost = 'localhost'
ENVIRONMENT = os.getenv('ENVIRONMENT', localhost)
HOST = '0.0.0.0'
PORT = int(os.getenv('PORT', 8010))


# Database settings:
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST') if os.getenv('on_docker') else 'localhost'
DB_PORT = os.getenv('DB_PORT')