import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MODE = ''
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = True
    ALLOWED_HOSTS = []

class DevelopmentConfig(Config):
    MODE = 'development'
    DEBUG = True
    SECRET_KEY = 'aecee04baae4eb3c056af0fc1cf4f067425393d4ce5cedf352d167ae8ca9ab25' # only for dev it is not secure !!!!!!!!!
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

class ProductionConfig(Config):
    MODE = 'production'
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

def get_config():
    mode = os.getenv('MODE', 'development')
    if mode == 'production':
        if not os.getenv('SECRET_KEY'):
            raise ValueError('SECRET_KEY is required in production mode')
        return ProductionConfig()
    return DevelopmentConfig()