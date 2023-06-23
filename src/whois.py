import httpx
import ujson


class Whois:

    api = 'BuajwPQ2ELaMcEzvT7TwTMtQ7eiqFk1R' # ключ Whois
    headers = {'apikey': api}

    def __init__(self, name: str) -> None:
        self.__name = name

    def get_info_domain(self) -> dict:
        """
        Получение информации от whois
        :return: json файл с информации о домени
        """
        try:
            domain_info = httpx.get(f'https://api.apilayer.com/whois/query?domain={self.__name}', headers=self.headers)
            domain_json = ujson.loads(domain_info.text)
            return domain_json
        except BaseException as e:
            print(e)

    def __str__(self) -> str:
        return self.__name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.__name}')"
