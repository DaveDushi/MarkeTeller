import json
import os

with open('conf.json', 'r') as f:
    data = json.load(f)


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my_secret_key'
    API_KEY = data["api_key"]
    DATABASE_URI = data["db_uri"]
    API_KEY_GPT = data["api_key_GPT"]
