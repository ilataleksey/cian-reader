import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


def main():
    URL = "https://www.cian.ru/sale/flat/288041113/"

    # отправляем get запрос на сайт URL
    request = requests.get(URL)
    print(request.status_code)

    # достаем все теги со страницы объявления
    soup = bs(request.text, "html.parser")

    # достаем название объявления
    topic_tag = soup.find_all("h1")
    topic = topic_tag[0].text

    # достаем описание объявления
    prompt_tag = soup.select("div[data-id='content']")
    prompt = prompt_tag[0].contents[0].text

    # достаем стоимость объявления
    price_tag = soup.select("div[data-testid='price-amount']")
    price = price_tag[0].text
    # очищаем от символа ₽ и пробела на конце
    if "₽" in price:
        price = price.replace("₽", "")
    # очищаем от NBSP - Non-breaking space
    price = int((price.replace(u"\xa0", "").strip()))

    # достаем данные о квартире и о доме
    flat_and_house_type_tags = soup.select("div[data-name='OfferSummaryInfoGroup']")

    # делим теги на группы по объекту описания
    for type_tag in flat_and_house_type_tags:
        if type_tag.select("h2")[0].text == "О квартире":
            flat_type_tags = type_tag.select("div[data-name='OfferSummaryInfoItem']")
        elif type_tag.select("h2")[0].text == "О доме":
            house_type_tags = type_tag.select("div[data-name='OfferSummaryInfoItem']")

    # создаем словарь на основе данных о квартире
    flat_info = {}
    for tag in flat_type_tags:
        flat_info[tag.contents[0].text] = tag.contents[1].text

    # создаем словарь на основе данных о доме
    house_info = {}
    for tag in house_type_tags:
        house_info[tag.contents[0].text] = tag.contents[1].text

    print(f"Наименование:  {topic} \n\n"
          f"Описание: {prompt} \n\n"
          f"Цена: {price} \n\n"
          f"Описание квартиры: {flat_info.items()} \n\n"
          f"Описание дома: {house_info.items()}")


if __name__ == "__main__":
    main()
