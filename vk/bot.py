from vk_api.longpoll import VkLongPoll, VkEventType

import settings
from vk.vk import Vk
from db.db_work import UsersVk, exists_user, add_user

class BotVk():
    HELP = """
    Для начала поиска введите команду 'поиск' и укажите id пользователя в VK через пробел.
    Если id не указан, то поиск будет сделан по данным вашего профиля.

    Например, поиск 15364645
    """
    available_sex = {
        1: 'женский',
        2: 'мужской'
    }
    available_relation = {
        1: 'не женат/не замужем',
        2: 'есть друг/есть подруга',
        3: 'помолвлен/помолвлена',
        4: 'женат/замужем',
        5: 'всё сложно',
        6: 'в активном поиске',
        7: 'влюблён/влюблена',
        8: 'в гражданском браке'
    }

    available_age = {
        'start': 18,
        'end': 99
    }

    def __init__(self, token_user, token_group):
        self.vk = Vk(token_user, token_group)
        self.longpoll = VkLongPoll(self.vk.vk_group)
        self.users = {}
        self.current_start = {}
        self.current_step = 5

    def get_command(self, text):
        s = text.split()
        command = [s[0].lower(), s[1:]]
        return command

    def command_help(self, user_id):
        hello = 'С возвращением' if exists_user(user_id) else 'Привет'
        self.vk.write_msg(user_id, f"{hello}, {self.vk.get_name(user_id)} \n {self.HELP}")

    def command_search(self, user_id, user_search):
        # запишем данные пользователя, который использует приложение, в базу
        if not exists_user(user_id):
            user_vk = UsersVk(user_id)
            add_user(user_vk)

        # получаем данные из vk
        param_vk = self.vk.get_user(user_search)

        # проверим полноту данных для поиска
        param_search = self.check_parameters(user_id, param_vk)

        if param_search is None:
            self.vk.write_msg(user_id, 'Поиск отменен...')
            return

        self.vk.write_msg(user_id, 'Выполняется поиск...')

        # выполняем поиск
        self.current_start[user_id] = 0
        self.users[user_id] = self.vk.read_users(param_search)

        # выводим информацию
        self.vk.write_msg(user_id, f'Найдено {len(self.users[user_id])}')
        self.current_start[user_id] = self.write_inform(user_id)

    def command_yes(self, user_id):
        self.current_start[user_id] = self.write_inform(user_id)

        if self.current_start[user_id] >= len(self.users[user_id]):
            self.reset_search(user_id)
            self.vk.write_msg(user_id, 'Поиск завершен')

    def command_no(self, user_id):
        self.reset_search(user_id)
        self.vk.write_msg(user_id, 'Поиск завершен')

    def write_inform(self, user_id):
        for i, el in enumerate(self.users[user_id][self.current_start[user_id]:self.current_start[user_id] + self.current_step]):
            self.vk.write_msg(user_id, f'{el["name"]} {el["link"]}', attach=f'{",".join(el["photo"])}')

        if self.current_start[user_id] + self.current_step <= len(self.users[user_id]):
            self.vk.write_msg(user_id, 'Продолжить?', keyboard=self.vk.create_button_YesNo())

        return self.current_start[user_id] + self.current_step

    def reset_search(self, user_id):
        self.users.pop(user_id)
        self.current_start.pop(user_id)

    def check_parameters(self, user_id, param):
        if param.get('relation', 0) == 0 or param.get('age', 0) == 0 or param.get('sex', 0) == 0:
            self.vk.write_msg(user_id, f"Профиль заполнен не полностью - не хватает данных для поиска!\n"
                                       f"Введите недостающие данные:")

        param_new = dict()
        param_new['is_closed'] = param['is_closed']
        param_new['city'] = param['city']

        if param.get('age', 0) == 0:
            param_new['age'] = self.input_data_range(user_id, 'Возраст', self.available_age)
            if param_new['age'] is None:
                return None
        else:
            param_new['age'] = param['age']

        if param.get('sex', 0) == 0:
            param_new['sex'] = self.input_data_list(user_id, 'Пол', self.available_sex)
            if param_new['sex'] is None:
                return None
        else:
            param_new['sex'] = param['sex']

        if param.get('relation', 0) == 0:
            param_new['relation'] = self.input_data_list(user_id, 'Семейное положение', self.available_relation)
            if param_new['relation'] is None:
                return None
        else:
            param_new['relation'] = param['relation']

        return param_new

    # ввод данных типа int с значениями из некоторого списка
    def input_data_list(self, user_id, name_param, available_values):
        string_values = '\n'.join([f'{a} - {b}' for a, b in available_values.items()])

        self.vk.write_msg(user_id, f"{name_param} (введите число из списка).\n{string_values}\n\n"
                                   f"Если хотите оказаться от поиска, введите команду 'выход'")

        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request = self.get_command(event.text)

                    if request[0] == 'выход':
                        return None

                    if request[0].isdigit():
                        # проверяем, что введено допустимое значение
                        if len(available_values) > 0 and int(request[0]) in available_values.keys():
                            self.vk.write_msg(user_id, f"Принято!")
                            return int(request[0])
                        else:
                            self.vk.write_msg(user_id, f"Значение должно быть из предложенного списка!")
                    else:
                        self.vk.write_msg(user_id, f"Надо ввести число из списка!")

    # ввод данных типа int в нужном диапазоне
    def input_data_range(self, user_id, name_param, available_values):
        self.vk.write_msg(user_id, f"{name_param} (введите число от {available_values['start']} "
                                   f"до {available_values['end']}).\n\n"
                                   f"Если хотите оказаться от поиска, введите команду 'выход'")

        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request = self.get_command(event.text)

                    if request[0] == 'выход':
                        return None

                    if request[0].isdigit():
                        # проверяем, что введено допустимое значение
                        if available_values['start'] <= int(request[0]) <= available_values['end']:
                            self.vk.write_msg(user_id, f"Принято!")
                            return int(request[0])
                        else:
                            self.vk.write_msg(user_id, f"Значение должно быть в указанном диапазоне!")
                    else:
                        self.vk.write_msg(user_id, f"Надо ввести число в указанном диапазоне!")

    def run_bot(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:

                if event.to_me:
                    request = self.get_command(event.text)

                    # поиск еще не выполняся
                    if event.user_id not in self.users.keys():
                        if request[0] == "поиск":
                            self.command_search(event.user_id, event.user_id if request[1] == [] else request[1])
                        else:
                            self.command_help(event.user_id)
                    # пользователь просматривает результат поиска
                    else:
                        if request[0] == "да":
                            self.command_yes(event.user_id)
                        elif request[0] == "нет":
                            self.command_no(event.user_id)


if __name__ == "__main__":
    my_bot = BotVk(settings.TOKEN_USER, settings.TOKEN_GROUP)

    my_bot.run_bot()
