import ujson
import os


class Saver:

    file = os.path.join("..", 'src', 'domain.json')

    def adding_info_file(self, domain: dict) -> None:
        """
        Добавление домена в файл
        :param domain: словарь с названием домена и время жизни
        :return: None
        """
        if os.path.exists(self.file) is False:
            with open(self.file, 'w', encoding='utf-8') as f:
                f.write('[]')

        json_domain = ujson.load(open(self.file))
        json_domain.append(domain)

        with open(self.file, 'w', encoding='utf-8') as f:
            ujson.dump(json_domain, f, indent=2, ensure_ascii=False, escape_forward_slashes=False)

    def del_info_file(self, name: str) -> bool:
        """
        Удаление домена из списка
        :param name: имя домена
        :return: None
        """
        try:
            json_domain = ujson.load(open(self.file))
            for i in json_domain:
                if name in i:
                    json_domain.remove(i)
                    break
            with open(self.file, 'w', encoding='utf-8') as f:
                ujson.dump(json_domain, f, indent=2, ensure_ascii=False, escape_forward_slashes=False)
            return True
        except BaseException:
            return False

    def get_info_file(self) -> list:
        """
        Вывод списка доменов и время их жизни
        :return: None
        """
        with open(self.file, 'r', encoding='utf-8') as f:
            return ujson.load(f)
