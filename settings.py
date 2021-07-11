import os
from dotenv import dotenv_values, set_key

config = dotenv_values(".env")

TOKEN_GROUP = config['TOKEN_GROUP']
TOKEN_USER = config['TOKEN_USER']

# def check_token():
#     pass



# def load_param():
#     config = dotenv_values(".env")
#
#     if 'token_group' not in config:
#         print('Для работы приложения необходим токен сообщества')
#         return False
#
#     os.environ['token_group'] = config['token_group']
#     print(os.environ['token_group'])
#
#     return True
#
#
# def save_param(key, value):
#     os.environ[key] = value
#     set_key(".env", key, os.environ[key])

