from vk_api.longpoll import VkLongPoll, VkEventType
from pprint import pprint

import settings
from vk.vk import Vk

vk = Vk(settings.TOKEN_USER, settings.TOKEN_GROUP)

longpoll = VkLongPoll(vk.vk_group)


def print_help():
    help = """Пока я знаю только эти команды:
    1. поиск  
    Для начала поиска введите команду поиск и укажите id пользователя в VK через пробел. 
    Если id не указан, то поиск будет сделан для текущего пользователя.
    
    Например, поиск 15364645
    
    2. помощь
    Справка по работе с ботом.
    """
    return help


def write_inform(user_id, users, start, step):
    for i, el in enumerate(users[start:start+step]):
        vk.write_msg(user_id, f'{el["name"]} {el["link"]}')
        if len(el['photo']) > 0:
            vk.write_msg(user_id, attach=el['photo'])

    if start+step <= len(users):
        vk.write_msg(event.user_id, 'Продолжить?', keyboard=vk.create_button_YesNo())

    return start+step


def get_command(text):
    s = text.split()
    command = [s[0].lower(), s[1:]]
    return command


if __name__ == '__main__':
    users = []
    current_start = 0
    current_step = 5
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = get_command(event.text)

                if len(users) == 0: # поиск еще не проводился
                    if request[0] == "привет":
                        vk.write_msg(event.user_id, f"Привет, {event.user_id}")
                    elif request[0] == "поиск":
                        # определяем параметры поиска по профилю пользователя (текущего или указанного)
                        if request[1] == '':
                            param = vk.get_user(event.user_id)
                        else:
                            param = vk.get_user(request[1])

                        # запросить недостающие параметры для поиска!!!

                        # ищем в VK
                        users = vk.read_users(param)
                        vk.write_msg(event.user_id, f'Найдено {len(users)}')

                        current_start = write_inform(event.user_id, users, current_start, current_step)
                    else:
                        vk.write_msg(event.user_id, print_help())
                else: # поиск проводился, пользователь смотрит результаты
                    if request[0] == "да":
                        current_start = write_inform(event.user_id, users, current_start, current_step)
                    elif request[0] == "нет":
                        users = []
                        current_ind = 0
                        vk.write_msg(event.user_id, 'Результаты поиска очищены')