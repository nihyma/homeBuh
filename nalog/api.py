# -*- coding: utf-8 -*-
import requests
import json
from config.nalog import CLIENT_SECRET, PASSWORD, INN

class NalogRuPython:
    HOST = 'irkkt-mobile.nalog.ru:8888'
    DEVICE_OS = 'iOS'
    CLIENT_VERSION = '2.9.0'
    DEVICE_ID = '7C82010F-16CC-446B-8F66-FC4080C66521'
    ACCEPT = '*/*'
    USER_AGENT = 'billchecker/2.9.0 (iPhone; iOS 13.6; Scale/2.00)'
    ACCEPT_LANGUAGE = 'ru-RU;q=1, en-US;q=0.9'

    def __init__(self):
        self.__session_id = None
        self.set_session_id()

    def set_session_id(self) -> None:
        if CLIENT_SECRET is None:
            raise ValueError('OS environments not content "CLIENT_SECRET"')
        if INN is None:
            raise ValueError('OS environments not content "INN"')
        if PASSWORD is None:
            raise ValueError('OS environments not content "PASSWORD"')

        url = f'https://{self.HOST}/v2/mobile/users/lkfl/auth'
        payload = {
            'inn': INN,
            'client_secret': CLIENT_SECRET,
            'password': PASSWORD
        }
        headers = {
            'Host': self.HOST,
            'Accept': self.ACCEPT,
            'Device-OS': self.DEVICE_OS,
            'Device-Id': self.DEVICE_ID,
            'clientVersion': self.CLIENT_VERSION,
            'Accept-Language': self.ACCEPT_LANGUAGE,
            'User-Agent': self.USER_AGENT,
        }

        resp = requests.post(url, json=payload, headers=headers)
        self.__session_id = resp.json()['sessionId']

    def _get_ticket_id(self, qr: str) -> str:
        url = f'https://{self.HOST}/v2/ticket'
        payload = {'qr': qr}
        headers = {
            'Host': self.HOST,
            'Accept': self.ACCEPT,
            'Device-OS': self.DEVICE_OS,
            'Device-Id': self.DEVICE_ID,
            'clientVersion': self.CLIENT_VERSION,
            'Accept-Language': self.ACCEPT_LANGUAGE,
            'sessionId': self.__session_id,
            'User-Agent': self.USER_AGENT,
        }
        resp = requests.post(url, json=payload, headers=headers)
        return resp.json()["id"]

    def get_ticket(self, qr: str) -> dict:
        ticket_id = self._get_ticket_id(qr)
        url = f'https://{self.HOST}/v2/tickets/{ticket_id}'
        headers = {
            'Host': self.HOST,
            'sessionId': self.__session_id,
            'Device-OS': self.DEVICE_OS,
            'clientVersion': self.CLIENT_VERSION,
            'Device-Id': self.DEVICE_ID,
            'Accept': self.ACCEPT,
            'User-Agent': self.USER_AGENT,
            'Accept-Language': self.ACCEPT_LANGUAGE,
        }
        resp = requests.get(url, headers=headers)
        return resp.json()

    def get_clean_json(self, qr: str):
        try:
        	ticket = self.get_ticket(qr)
        except:
        	return [False, 'Чек не найден в системе. Параметры: {0}.'.format(qr)]
        sale = dict()
        try:
            sale['shop_name'], sale['shop_inn'] = ticket['seller']['name'].replace('"','').upper(), ticket['seller']['inn']
            sale['sale_date'], sale['sale_sum'] = ticket['operation']['date'][:10].replace('-',''), ticket['operation']['sum']
            sale['item_list'] = [[i['name'].replace('"',''), i['sum']] for i in ticket['ticket']['document']['receipt']['items']]
        except:
            return [False, 'Чек не найден в системе. Параметры: {0}. Ответ: {1}'.format(qr, ticket)]
        return [True, json.dumps(sale).encode('ascii').decode('unicode_escape')]
