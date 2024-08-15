import os

class Config:
    DEBUG = True
    PORT = 4000
    MYSQL_HOST = ''
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'normatividad'
    ALLOWED_EXTENSIONS = {'pdf', 'doc'}
    SECRET_KEY = os.urandom(24)
