## Чат-бот "VKinder"
Бот ищет людей, подходящих под условия, на основании информации о пользователе из VK:

- возраст,
- пол,
- город,
- семейное положение.

Найденные результаты отправляются в чат вместе со ссылкой на найденного человека, также выводится 
топ-3 популярных фотографии профиля.

ID пользователей VK, которые воспользовались ботом, записывается в БД.


## Настройка приложения:
Для работы приложения необходимы группа в VK с подключенным ботом, ключ доступа пользователя и ключ доступа сообщества.
1. Создать группу в VK и ключ доступа сообщества. См. [инструкцию](vk_group_settings.md)
2. Создать ключ доступа пользователя. См. [инструкцию](vk_user_settings.md)
3. Настройки хранятся в файле .env. При отсутствии этого файла, необходимые настройки запрашиваются у пользователя 
   при запуске приложения. Пример файла настроек - .env.example.
4. Запустить файл main.py   
