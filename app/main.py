# -*- coding: utf-8 -*-
from bot import telebot
from nalog import api
import yaml
import argparse

#пример строки QR
#t=20190320T2303&s=5803.00&fn=9251440300007971&i=141637&fp=4087570038&n=1
# t — timestamp, время, когда вы осуществили покупку
# s — сумма чека
# fn — кодовый номер fss, потребуется далее в запросе к API
# i — номер чека, он нам потребуется далее в запросе к API
# fp — параметр fiscalsign, потребуется далее в запросе к API

def create_arg_parser():
    parser = argparse.ArgumentParser(prog='homeBuh',
                                     description='Slip QR parser',
                                     epilog = '(c) NiHyma 2021')
    parser.add_argument('-c', '--config', type=argparse.FileType(), required=True, help='Path to config file')
    return parser

def init_config(config_path: str):
    yaml_data = config_path.read()
    data_loaded = yaml.safe_load(yaml_data)
    return data_loaded

def main() -> None:
    arg_parser = create_arg_parser()
    namespace = arg_parser.parse_args()
    config = init_config(namespace.config)
    try:
        api_client = api.NalogRuPython(config['nalod_api'])
    except:
        api_client = None
    bot = telebot.get_bot(config['telegram'], api_client)
    bot.polling()

if __name__ == '__main__':
    main()