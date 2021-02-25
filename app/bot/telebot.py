import re
from telebot import TeleBot

def filter_qr(message):
    return re.fullmatch(r't=\d{8}T\d{4,6}&s=\d*[\.]\d*&fn=\d*&i=\d*&fp=\d*&n=\d*', message)

class TelegramBotPython(TeleBot):
    def __init__(self, config, api_client):
        self.CHANNEL_ID = config.get('CHANNEL_ID', '')
        self.DEFAULT_MSG = config.get('DEFAULT_MSG', '{0} {1} {2}')
        self.FILTER_GROUP = config.get('GROUP')
        self.CLIENT = api_client
        super().__init__(config.get('TOKEN'))

def get_bot(config, api_client):
    bot = TelegramBotPython(config, api_client)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Please choose: {0}'.format(message.chat.id))

    @bot.message_handler(commands=['help'])
    def help_command(message) -> None:
        bot.send_message(message.chat.id, 'Help: {0}'.format(message.chat.id))

    @bot.message_handler(func=lambda message: message.chat.id in bot.FILTER_GROUP and filter_qr(message.text))
    def qr_command(message) -> None:
        flag = None
        if bot.CLIENT:
            flag, ticket = bot.CLIENT.get_clean_json(message.text)
        if flag:
            bot.send_message(bot.CHANNEL_ID, ticket)
        else:
            pars_qr = dict(x.split('=') for x in message.text.split('&'))
            date_qr = pars_qr['t'][:8]
            sum_qr = pars_qr['s']
            msg = bot.DEFAULT_MSG.format(sum_qr, date_qr, bot.CLIENT.INN)
            bot.send_message(bot.CHANNEL_ID, msg)

    return bot