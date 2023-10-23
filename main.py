import cian_parser as cp
import pandas as pd


def main():
    PAGE_NUMBER = 1

    rooms_count = 1
    region_name = {
        "moscow": 1,
    }
    deal_type = {
        "sale": "sale",
        "rent": "rent"
    }
    offer_type = "flat"
    min_price = 1
    max_price = 6000000

    # попадаем на стартовую страницу поиска по заданным критериям
    start_url = f"https://www.cian.ru/cat.php?currency=2&deal_type={deal_type['sale']}&engine_version=2&maxprice={max_price}&minprice={min_price}&object_type%5B0%5D=2&offer_type={offer_type}&p={PAGE_NUMBER}&region={region_name['moscow']}&room{rooms_count}=1"

    # вызываем функцию для обработки страницы поиска
    # каскадным вызовом функций возвращается список объектов
    all_offers = cp.search(start_url)

    flat_info = set()
    house_info = set()
    for index, offer in enumerate(all_offers):
        print(f"Наименование объявления {index+1}: {offer.topic}")
        for key in offer.flat.keys():
            flat_info.add(key)
        for key in offer.house.keys():
            house_info.add(key)

    print(flat_info)
    print(house_info)


if __name__ == "__main__":
    main()
