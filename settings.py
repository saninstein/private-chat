import os
from cryptography import fernet

DEBUG = True
PATH = os.getcwd()
TEMPLATES_DIR = os.path.join(PATH, 'templates/')
MONGO_IP = 'localhost'
MONGO_PORT = 27017
SECRET_KEY = fernet.Fernet.generate_key()
