from vk_api.longpoll import VkLongPoll, VkEventType
from pprint import pprint

import settings
from vk.vk import Vk
from db.db_work import UsersVk, exists_user, add_user

class BotVk():
    HELP = """
    Для начала поиска введите команду 'поиск' и укажите id пользователя в VK через пробел.
    Если id не указан, то поиск будет сделан по данным вашего профиля.

    Например, поиск 15364645
    """

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
        # запишем данные пользователя, который использует приложение в базу
        if not exists_user(user_id):
            user_vk = UsersVk(user_id)
            add_user(user_vk)

        # получаем данные из vk
        param = self.vk.get_user(user_search)
        # print(param)

        # проверим полноту данных для поиска
        # print(self.current_start)
        # self.vk.write_msg(user_id, f"Введи число")
        # for event1 in self.longpoll.listen():
        #     if event1.type == VkEventType.MESSAGE_NEW:
        #         if event1.to_me:
        #             request1 = event1.text
        #             print(request1, request1.isdigit())
        #             if request1.isdigit():
        #                 self.vk.write_msg(user_id, f"Есть число")
        #                 break
        #             else:
        #                 self.vk.write_msg(user_id, f"Это не число")
        # self.vk.write_msg(user_id, f"Начинаем поиск")

        # выполняем поиск
        self.current_start[user_id] = 0
        self.users[user_id] = self.vk.read_users(param)

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

    def run_bot(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:

                if event.to_me:
                    request = self.get_command(event.text)

                    if event.user_id not in self.users.keys():
                        if request[0] == "поиск":
                            self.command_search(event.user_id, event.user_id if request[1] == [] else request[1])
                        else:
                            self.command_help(event.user_id)
                    else:
                        if request[0] == "да":
                            self.command_yes(event.user_id)
                        elif request[0] == "нет":
                            self.command_no(event.user_id)


if __name__ == "__main__":
    my_bot = BotVk(settings.TOKEN_USER, settings.TOKEN_GROUP)

    my_bot.run_bot()
