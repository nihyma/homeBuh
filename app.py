# -*- coding: utf-8 -*-
from bot.telegram import TelegramBotPython

#пример строки QR
#t=20190320T2303&s=5803.00&fn=9251440300007971&i=141637&fp=4087570038&n=1
# t — timestamp, время, когда вы осуществили покупку
# s — сумма чека
# fn — кодовый номер fss, потребуется далее в запросе к API
# i — номер чека, он нам потребуется далее в запросе к API
# fp — параметр fiscalsign, потребуется далее в запросе к API

def main():
    bot = TelegramBotPython()
    bot.start()

if __name__ == '__main__':
    main()