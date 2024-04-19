from settings import Settings

import telebot

token = Settings()
bot_token = token.bot_token.get_secret_value()
bot = telebot.TeleBot(bot_token)
