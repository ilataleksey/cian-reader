import cian_parser as cp
import csv
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
    max_price = 5000000

    # попадаем на стартовую страницу поиска по заданным критериям
    start_url = f"https://www.cian.ru/cat.php?currency=2&deal_type={deal_type['sale']}&engine_version=2&maxprice={max_price}&minprice={min_price}&object_type%5B0%5D=2&offer_type={offer_type}&p={PAGE_NUMBER}&region={region_name['moscow']}&room{rooms_count}=1"

    # вызываем функцию для обработки страницы поиска
    # каскадным вызовом функций возвращается список объектов
    all_offers = cp.search(start_url)

    flat_info = set()
    house_info = set()

    for offer in all_offers:
        for key in offer.flat.keys():
            flat_info.add(key)
        for key in offer.house.keys():
            house_info.add(key)
    header = ["topic", "price", "link", "description", *flat_info, *house_info]

    all_offers_list = []
    for offer in all_offers:
        offer_dic = {}
        for column in header:
            try:
                offer_dic[column] = getattr(offer, column)
            except AttributeError:
                if column in offer.flat.keys():
                    offer_dic[column] = offer.flat[column]
                else:
                    try:
                        offer_dic[column] = offer.house[column]
                    except KeyError:
                        offer_dic[column] = None
        all_offers_list.append(offer_dic)

    write_csv(all_offers_list, header)


def write_csv(all_offers, header):
    file_name = "cian_report.csv"

    with open(file_name, "w") as w_file:

        file_writer = csv.DictWriter(w_file, fieldnames=header)
        file_writer.writeheader()
        for offer in all_offers:
            file_writer.writerow(offer)

    # print(flat_info)
    # print(house_info)


if __name__ == "__main__":
    main()
