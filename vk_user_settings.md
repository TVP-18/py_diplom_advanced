# Как получить ключ доступа пользователя

## Для этого нужно:
1. Создать Standalone-приложение в VK https://vk.com/editapp?act=create
   ![image](img/vk_create_app_1.png)
2. Затем открыть Настройки и сделать всё как на скриншоте
![image](img/vk_create_app_2.png)
3. Для создания ключа доступа пользователя нужен параметр "ID Приложения"
4. В браузере в адресную строку введите  
https://oauth.vk.com/authorize?client_id=IDПриложения&display=page&scope=offline&response_type=token&v=5.131&state=123456
   Для параметра client_id укажите ID Приложения
   ![image](img/vk_create_app_3.png) 
5. После перехода по ссылке браузер вернет в адресной строке ключ доступа пользователя,
   параметр access_token
   ![image](img/vk_create_app_4.png) 
