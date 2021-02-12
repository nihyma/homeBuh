# -*- coding: utf-8 -*-
import re
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, MessageFilter

class FilterGroup(MessageFilter):
    def __init__(self, group):
        self.GROUP = group
        super().__init__()

    def filter(self, message):
        return message.chat.id in self.GROUP

class FilterQR(MessageFilter):
    def filter(self, message):
        return re.fullmatch(r't=\d{8}T\d{4,6}&s=\d*[\.]\d*&fn=\d*&i=\d*&fp=\d*&n=\d*', message.text)

class TelegramBotPython:
    def __init__(self, config, api_client):
        self.TOKEN = config['TOKEN']
        self.CHANNEL_ID = config['CHANNEL_ID']
        self.DEFAULT_MSG = config['DEFAULT_MSG']
        self.FILTER_GROUP = FilterGroup(config['GROUP'])
        self.FILTER_QR = FilterQR()
        self.CLIENT = api_client

    def start(self):
        updater = Updater(token=self.TOKEN, use_context=True)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", self.start_command, filters=self.FILTER_GROUP))
        dp.add_handler(CommandHandler("help", self.help_command, filters=self.FILTER_GROUP))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command & self.FILTER_GROUP & self.FILTER_QR, self.qr_command))
        updater.start_polling()
        updater.idle()

    def start_command(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text('Please choose: {0}'.format(update.message.chat.id))

    def help_command(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text('Help!')

    def qr_command(self, update: Update, context: CallbackContext) -> None:
        flag, ticket = self.CLIENT.get_clean_json(update.message.text)
        if flag:
            context.bot.send_message(chat_id=self.CHANNEL_ID, text=ticket)
        else:
            pars_qr = dict(x.split('=') for x in update.message.text.split('&'))
            date_qr = pars_qr['t'][:8]
            sum_qr = pars_qr['s']
            msg = self.DEFAULT_MSG.format(sum_qr, date_qr, self.CLIENT.INN)
            context.bot.send_message(chat_id=self.CHANNEL_ID, text=msg)
