import os
from dotenv import dotenv_values, set_key

config = dotenv_values(".env")

TOKEN_GROUP = config['TOKEN_GROUP']
TOKEN_USER = config['TOKEN_USER']
DATABASE_URL = config['DATABASE_URL']

