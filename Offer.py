class Offer(object):
    def __init__(self):
        self._topic = ""
        self._description = ""
        self._price = 0
        self._link = ""
        self._flat = {}
        self._house = {}

    def __str__(self):
        return (f"Наименование:  {self._topic} \n\n"
        f"Описание: {self._description} \n\n"
        f"Цена: {self._price} \n\n"
        f"Ссылка: {self._link} \n\n"
        f"Описание квартиры: {self._flat.items()} \n\n"
        f"Описание дома: {self._house.items()}")

    @property
    def topic(self):
        return self._topic

    @topic.setter
    def topic(self, text):
        self._topic = text

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, text):
        self._description = text

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, n):
        self._price = n

    @property
    def flat(self):
        return self._flat

    @flat.setter
    def flat(self, dic):
        self._flat = dic

    @property
    def house(self):
        return self._house

    @house.setter
    def house(self, dic):
        self._house = dic

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, text):
        self._link = text
