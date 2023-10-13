class Promo(object):
    def __init__(self):
        self._topic = ""
        self._prompt = ""
        self._price = 0
        self._flat = {}
        self._house = {}

    def __str__(self):
        return (f"Наименование:  {self._topic} \n\n"
        f"Описание: {self._prompt} \n\n"
        f"Цена: {self._price} \n\n"
        f"Описание квартиры: {self._flat.items()} \n\n"
        f"Описание дома: {self._house.items()}")

    @property
    def topic(self):
        return self._topic

    @topic.setter
    def topic(self, text):
        self._topic = text

    @property
    def prompt(self):
        return self._prompt

    @prompt.setter
    def prompt(self, text):
        self._prompt = text

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