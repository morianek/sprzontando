import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MODE = ''
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = True
    ALLOWED_HOSTS = []
    EMAIL_BACKEND = ''
    EMAIL_HOST = ''
    EMAIL_PORT = 0
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_USE_TLS = False


class DevelopmentConfig(Config):
    MODE = 'development'
    DEBUG = True
    SECRET_KEY = 'aecee04baae4eb3c056af0fc1cf4f067425393d4ce5cedf352d167ae8ca9ab25' # only for dev it is not secure !!!!!!!!!
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_USE_TLS = False


class ProductionConfig(Config):
    MODE = 'production'
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
    EMAIL_USE_TLS = True


def get_config():
    mode = os.getenv('MODE', 'development')
    if mode == 'production':
        if not os.getenv('SECRET_KEY'):
            raise ValueError('SECRET_KEY is required in production mode')
        return ProductionConfig()
    return DevelopmentConfig()