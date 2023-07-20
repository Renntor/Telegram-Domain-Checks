from bs4 import BeautifulSoup
import httpx
import re


class WhoisSearch:

    url = 'https://whois.ru/'
    alter_url = 'https://www.nic.ru/whois/?searchWord='

    def __init__(self, domain):
        self.domain = domain.lower()

    def get_date(self) -> str:
        """
        Возвращает дату конца аренды домена
        :return: str
        """
        try:
            date = httpx.get(self.url+self.domain, timeout=100.0).text
            soup = BeautifulSoup(date, 'lxml').find(class_='raw-domain-info-pre').text
            text_search = re.findall(r'paid-till:     \d{4}-\d\d-\d\dT\d\d:\d\d:\d\d', soup)[0][-19:]
            return text_search.replace('T', ' ')
        except (AttributeError, IndexError):
            date = httpx.get(self.alter_url+self.domain, timeout=100.0).text
            try:
                soup = BeautifulSoup(date, 'lxml').find(class_='_3U-mA _23Irb').text
                text_date = re.findall(r'Expiration Date: \d{4}-\d\d-\d\dT\d\d:\d\d:\d\d', soup)[0][17:]
                return text_date.replace('T', ' ')
            except (AttributeError, IndexError):
                return 'Информация отсутствует'

