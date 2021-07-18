import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from pprint import pprint
from datetime import date
import datetime
from random import randrange


class Vk:

    def __init__(self, token_user, token_group):
        self.vk_user = vk_api.VkApi(token=token_user)
        self.vk_group = vk_api.VkApi(token=token_group)

    def create_button_empty(self):
        return VkKeyboard(inline=True).get_empty_keyboard()

    def create_button_YesNo(self):
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('Да', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Нет', color=VkKeyboardColor.NEGATIVE)
        return keyboard.get_keyboard()

    def write_msg(self, user_id, message='', attach='', keyboard=None):
        if keyboard is None:
            keyboard = self.create_button_empty()

        self.vk_group.method('messages.send', {
            'user_id': user_id,
            'message': message,
            'random_id': randrange(10 ** 7),
            'attachment': attach,
            'keyboard': keyboard})

    def get_user(self, user_id):
        result = self.vk_user.method('users.get', {'user_ids': user_id, 'fields': 'bdate, sex, city, relation'})
        user = {'id': result[0].get('id'),
                'city': self.get_city(result[0].get('city', 0)),
                'relation': result[0].get('relation', 0),
                'sex': result[0].get('sex', 0),
                'age': self.get_age(result[0].get('bdate', '')),
                'is_closed': result[0].get('is_closed')}
        return user

    def get_name(self, user_id):
        result = self.vk_user.method('users.get', {'user_ids': user_id})
        name = f'{result[0].get("first_name")} {result[0].get("last_name")}'
        return name

    def get_city(self, value):
        if value == 0:
            return 0
        return value.get('id', 0)

    def get_age(self, value):
        if value == '':
            return 0

        bithdate = list(map(int, value.split('.')))
        if len(bithdate) < 3:
            return 0

        bdate = datetime.date(bithdate[2], bithdate[1], bithdate[0])
        today = date.today()
        return today.year - bdate.year - ((today.month, today.day) < (bdate.month, bdate.day))

    def search_users(self, param, count=20):
        result = self.vk_user.method('users.search', {
            'count': count,
            'city': param['city'],
            'sex': param['sex'],
            'status': param['relation'],
            'age_from': param['age'],
            'age_to': param['age'],
            'fields': 'bdate, sex, city, relation, domain'
        })

        return result['items']

    def get_photos(self, user_id, count=20):
        photos = self.vk_user.method('photos.get', {
            'owner_id': user_id,
            'album_id': 'profile',
            'extended': 1,
            'count': count
        })
        return photos

    def read_photos(self, user_id, count=20):
        photos = []
        vk_photos = self.get_photos(user_id, count)
        for item in vk_photos['items']:
            photos.append([item['id'], item['likes']['count']+item['comments']['count']])
        # сортируем по популярности и возвращаем три первых
        photos.sort(key=lambda photo: photo[1], reverse=True)

        result = []
        for el in photos[:3]:
            result.append(f'photo{user_id}_{el[0]}')

        return result

    def read_users(self, param):

        users_dirty = self.search_users(param)

        # обрабатываем список найденных пользователей
        result = []
        for el in users_dirty:
            # фотографии читаем только с открытого профиля
            photos = []
            if not el.get('is_closed'):
                photos = self.read_photos(el['id'])

            result.append({
                'name': el.get('first_name', ''),
                'link': f'https://vk.com/{el["domain"]}',
                'id': el['id'],
                'photo': photos
            })
        return result


if __name__ == '__main__':
    pass

