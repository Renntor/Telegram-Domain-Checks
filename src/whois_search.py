from bs4 import BeautifulSoup
import httpx
import re


class WhoisSearch:

    url = 'https://www.nic.ru/whois/?searchWord='

    def __init__(self, domain):
        self.domain = domain

    def get_date(self):
        """
        Возвращает дату конца аренды домена
        :return: str
        """
        date = httpx.get(self.url+self.domain).text
        soup = BeautifulSoup(date, 'lxml').find(class_='_3U-mA _23Irb').text
        text_date = re.findall(r'Expiration Date: \d{4}-\d\d-\d\dT\d\d:\d\d:\d\d', soup)[0][17:]
        return text_date.replace('T', ' ')
