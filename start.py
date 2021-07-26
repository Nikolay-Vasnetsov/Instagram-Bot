"""=======================ВАЖНО!!! двохфакторна защита должна быть офф (2FA)======================"""
"""===ВАЖНО!!! НЕ включать несколько режимов одновременно или можете получить не то что ожидали==="""

# Впишите свои данные для входа
username = "your_login"
pwd = r"your_password"

"""========================Бот ищет посты по хештегу и ставт под ними лайки========================="""
# Включить режим - True, выключить - False
start_put_like_by_hashtags = True
# Хештег по которому искать посты
hashtag = "взаимныелайки"
# Сколько бот должен работать, 1 = 40 минут
work_time = 5


# Дальше ничего трогать не нужно
from bot import InstagramBot

my_bot = InstagramBot(username, pwd)

if start_put_like_by_hashtags:
    my_bot.login()
    my_bot.like_post_by_hashtag(hashtag, work_time)
