from vk_api.longpoll import VkLongPoll, VkEventType
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from pprint import pprint

from settings import TOKEN_GROUP, TOKEN_USER, DATABASE_URL
from vk.vk import Vk
from db.db_work import UsersVk, exists_user, add_user


HELP = """
Для начала поиска введите команду 'поиск' и укажите id пользователя в VK через пробел.
Если id не указан, то поиск будет сделан по данным вашего профиля.

Например, поиск 15364645
"""


def command_help(vk, user_id):
    hello = 'С возвращением' if exists_user(user_id) else 'Привет'
    vk.write_msg(user_id, f"{hello}, {vk.get_name(user_id)} \n {HELP}")


def command_hello(vk, user_id):
    if not exists_user(user_id):
        vk.write_msg(user_id, f"Привет, {vk.get_name(user_id)} \n {HELP}")


def command_search(vk, user_use, user_search):
    # запишем данные пользователя, который использует приложение в базу
    if not exists_user(user_use):
        user_vk = UsersVk(user_use)
        add_user(user_vk)

    # получаем данные из vk
    param = vk.get_user(user_search)
    users = vk.read_users(param)

    # обрабатываем данные

    return users


def write_inform(vk, user_id, users, start, step):
    for i, el in enumerate(users[start:start+step]):
        vk.write_msg(user_id, f'{el["name"]} {el["link"]}', attach=f'{",".join(el["photo"])}')

    if start+step <= len(users):
        vk.write_msg(user_id, 'Продолжить?', keyboard=vk.create_button_YesNo())

    return start+step


def get_command(text):
    s = text.split()
    command = [s[0].lower(), s[1:]]
    return command


def run_bot():
    vk = Vk(TOKEN_USER, TOKEN_GROUP)

    longpoll = VkLongPoll(vk.vk_group)

    users = []  # список найденных пользователей
    current_start = 0
    current_step = 5
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = get_command(event.text)

                if len(users) == 0:  # поиск еще не проводился
                    if request[0] == "поиск":
                        user_search = event.user_id if request[1] == [] else request[1]
                        users = command_search(vk, event.user_id, user_search)

                        # выводим информацию
                        vk.write_msg(event.user_id, f'Найдено {len(users)}')
                        current_start = write_inform(vk, event.user_id, users, current_start, current_step)
                    else:
                        command_help(vk, event.user_id)
                else:  # поиск проводился, пользователь смотрит результаты
                    if request[0] == "да":
                        current_start = write_inform(vk, event.user_id, users, current_start, current_step)

                        if current_start >= len(users):
                            users = []
                            current_ind = 0
                            vk.write_msg(event.user_id, 'Поиск завершен')

                    elif request[0] == "нет":
                        users = []
                        current_ind = 0
                        vk.write_msg(event.user_id, 'Поиск завершен')


if __name__ == '__main__':
    run_bot()
