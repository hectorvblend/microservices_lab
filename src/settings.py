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


# PUB/SUB Config
GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID', "MY_PROJECT_ID")
PUBSUB_TOPIC_NAME = os.getenv('PUBSUB_TOPIC_NAME', "MY_TOPIC_NAME")
PUBSUB_SUBSCRIPTION_NAME = os.getenv('PUBSUB_SUBSCRIPTION_NAME', "MY_SUBSCRIPTION_NAME")
WATCHDOG_MONITOR_INTERVAL_SEC = 600
JOB_MAX_ATTEMPTS = 3
JOB_TIMEOUT_SEC = 3600

# Deepseek ENV:
DEEPSEEK_PORT=os.getenv('DEEPSEEK_PORT', '11434')
DEEPSEEK_HOST=os.getenv('DEEPSEEK_HOST', 'localhost')
DEEPSEEK_MODEL=os.getenv('DEEPSEEK_MODEL', 'deepseek-r1:1.5b')
