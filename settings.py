import os
from dotenv import load_dotenv, find_dotenv, set_key

# имя файла настроек по умолчанию
ENV = '.env'


def create_key(text, key, file_name=ENV):
    key_value = input_value(f'{text}: ')

    os.environ[key] = key_value
    set_key(file_name, key, os.environ[key])


def create_key_url(key, file_name=ENV):
    print('Настройки для подключения БД')
    hostname = input_value('Адрес сервера: ')
    port = input_value('Порт сервера: ')
    database_name = input_value('Имя БД: ')
    user = input_value('Имя пользователя: ')
    password = input_value('Пароль: ')

    os.environ[key] = f'postgresql://{user}:{password}@{hostname}:{port}/{database_name}'
    set_key(file_name, key, os.environ[key])


def input_value(text):
    while True:
        value = input(text)
        if value == '':
            print(f'Значение не может быть пустым!')
        else:
            return value


# читаем настройки из файла, если их нет, то запрашиваем у пользователя
exists_env = find_dotenv(ENV)

if exists_env != '':
    load_dotenv(exists_env)

else:
    create_key('Ключ доступа сообщества', 'TOKEN_GROUP')
    create_key('Ключ доступа пользователя', 'TOKEN_USER')
    create_key_url('DATABASE_URL')


TOKEN_GROUP = os.getenv('TOKEN_GROUP')
TOKEN_USER = os.getenv('TOKEN_USER')
DATABASE_URL = os.getenv('DATABASE_URL')


if __name__ == "__main__":
    print(TOKEN_GROUP, TOKEN_USER, DATABASE_URL)
