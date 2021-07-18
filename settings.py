import os
from dotenv import load_dotenv, find_dotenv, set_key

# имя файла настроек по умолчанию
ENV = '.env'


def create_key(text, key, file_name=ENV):
    while True:
        key_value = input(f'{text}: ')
        if key_value == '':
            print(f'Значение не может быть пустым!')
        else:
            break

    os.environ[key] = key_value
    set_key(file_name, key, os.environ[key])


# читаем настройки из файла, если их нет, то запрашиваем у пользователя
exists_env = find_dotenv(ENV)

if exists_env != '':
    load_dotenv(exists_env)

else:
    create_key('Введите ключ доступа сообщества', 'TOKEN_GROUP')
    create_key('Введите ключ доступа пользователя', 'TOKEN_USER')
    create_key('Введите строку подключения к БД', 'DATABASE_URL')

TOKEN_GROUP = os.getenv('TOKEN_GROUP')
TOKEN_USER = os.getenv('TOKEN_USER')
DATABASE_URL = os.getenv('DATABASE_URL')


if __name__ == "__main__":
    print(TOKEN_GROUP, TOKEN_USER, DATABASE_URL)
