import os

class Configuration(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI= 'postgresql://postgres:admin''@localhost:5432/testflask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False