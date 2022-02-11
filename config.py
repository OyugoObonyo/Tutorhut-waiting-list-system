"""
A module containing the config class
"""
import os

class Config(object):
    """
    class with the various configuration variables for the application
    """
    SHEETY_URL = os.environ.get('SHEETY_URL')
    SHEETY_TOKEN = os.environ.get('SHEETY_TOKEN')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


