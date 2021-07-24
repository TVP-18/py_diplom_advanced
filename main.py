from settings import TOKEN_GROUP, TOKEN_USER
from vk.bot import BotVk


if __name__ == '__main__':
    my_bot = BotVk(TOKEN_USER, TOKEN_GROUP)
    my_bot.run_bot()
