import os
from cryptography import fernet

PATH = os.getcwd()
TEMPLATES_DIR = os.path.join(PATH, 'templates/')

SECRET_KEY = fernet.Fernet.generate_key()
