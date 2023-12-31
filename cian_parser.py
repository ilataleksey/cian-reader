import requests
from bs4 import BeautifulSoup as bs
from Offer import Offer


def search(page_url):
    print(f"Поиск предложений по ссылке:\n{page_url}")
    page_number = 1
    all_offers = []

    while True:
        print(f"страница поиска: {page_number}")
        # работаем с объявлениями на странице поиска
        page_offers = pars_search_page(page_url)

        for offer in page_offers:
            all_offers.append(offer)

        # ищем пагинатор, если есть, то переходим на следующую страницу и повторяем процедуру
        request = requests.get(page_url)
        soup = bs(request.text, "html.parser")

        pagination = soup.find(attrs={"data-name": "Pagination"})
        if pagination is None:
            break
        next_page_link_tag = pagination.find("a", string="Дальше")
        if next_page_link_tag is None:
            break
        else:
            page_url = page_url.replace(f"p={page_number}", f"p={page_number + 1}")
            page_number += 1

    return all_offers


def pars_search_page(page_url):
    request = requests.get(page_url)
    soup = bs(request.text, "html.parser")

    # находим блок, с которого начинаются рекламные предложения
    removed_tags = soup.select("div[data-name='Suggestions']")
    # удаляем всю рекламу, если ее нет, то идем дальше
    removed_tags[0].decompose() if len(removed_tags) else "pass"

    offers = soup.find_all(attrs={"data-testid": "offer-card"})
    if len(offers) == 0:
        print(f"Не найдено объявлений по заданным параметрам.\n"
              f"Попробуйте задать другие параметры и повторить поиск.")
    else:
        offer_links = []
        page_offers = []
        for index, offer in enumerate(offers):
            offer_link = offer.a.get("href")
            offer_links.append(offer_link)
            offer = pars_offer(offer_link)
            page_offers.append(offer)
            print(f"Обработка объявления на странице {index + 1}/{len(offers)}")

        return page_offers


def pars_offer(offer_url):
    # отправляем get запрос на сайт
    request = requests.get(offer_url)
    # достаем все теги со страницы объявления
    soup = bs(request.text, "html.parser")

    # создаем объект
    offer = Offer()

    # достаем название объявления
    topic_tag = soup.find_all("h1")
    offer.topic = topic_tag[0].text

    # сохраняем в объект ссылку
    offer.link = offer_url

    # достаем описание объявления
    description_tag = soup.select("div[data-id='content']")
    offer.description = description_tag[0].contents[0].text

    # достаем стоимость объявления
    price_tag = soup.select("div[data-testid='price-amount']")
    price = price_tag[0].text
    # очищаем от символа ₽ и пробела на конце
    if "₽" in price:
        price = price.replace("₽", "")
    # очищаем от NBSP - Non-breaking space
    offer.price = int((price.replace(u"\xa0", "").strip()))

    # достаем данные о квартире и о доме
    flat_and_house_type_tags = soup.select("div[data-name='OfferSummaryInfoGroup']")

    # делим теги на группы по объекту описания
    flat_type_tags = []
    house_type_tags = []
    for type_tag in flat_and_house_type_tags:
        if type_tag.select("h2")[0].text == "О квартире":
            flat_type_tags = type_tag.select("div[data-name='OfferSummaryInfoItem']")
        elif type_tag.select("h2")[0].text == "О доме":
            house_type_tags = type_tag.select("div[data-name='OfferSummaryInfoItem']")

    # создаем словарь на основе данных о квартире
    flat_info = {}
    for tag in flat_type_tags:
        flat_info[tag.contents[0].text] = tag.contents[1].text
    offer.flat = flat_info
    # создаем словарь на основе данных о доме
    house_info = {}
    for tag in house_type_tags:
        house_info[tag.contents[0].text] = tag.contents[1].text
    offer.house = house_info

    return offer
