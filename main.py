import pandas as pd
from parsing_module import set_params, get_number_of_pages, get_data_from_page, hotel_data
import time
import asyncio


async def parse_all_pages(params):
    """parse required information (titles and prices) from all found pages"""

    number_of_page = get_number_of_pages(params)
    print(f"Количество страниц: {number_of_page}")

    # all_hotel_names = list()
    # all_hotel_prices = list()
    tasks = []
    for current_page_number in range(number_of_page):
        task = asyncio.create_task(get_data_from_page(current_page_number, params))
        tasks.append(task)
        print(f"Обработана {current_page_number + 1} страница")
    await asyncio.gather(*tasks)

    all_hotel_names = [i[0] for i in hotel_data]
    all_hotel_prices = [i[1] for i in hotel_data]

    df = pd.DataFrame({"Отель": all_hotel_names, "Цена": all_hotel_prices})
    df.to_excel("output.xlsx", index=False)

    print("Готово")


def main():
    """
    The main entry point of the application
    """
    place = input("Введите место/название объекта: ")
    check_in_day, check_in_month, check_in_year = input("Введите дату заезда в формате дд.мм.гг: ").split('.')
    check_out_day, check_out_month, check_out_year = input("Введите дату отъезда в формате дд.мм.гг: ").split('.')
    number_of_adults = input("Введите количество взрослых: ")
    number_of_children = input("Введите количество детей: ")
    number_of_rooms = input("Введите количество номеров: ")
    params = set_params(place,
                        check_in_year,
                        check_in_month,
                        check_in_day,
                        check_out_year,
                        check_out_month,
                        check_out_day,
                        number_of_adults,
                        number_of_children,
                        number_of_rooms)
    asyncio.run(parse_all_pages(params))


if __name__ == '__main__':
    main()


# 40 min
# 70 min
# 60 min
# 120 min
# 90 min
# 60 min

# 60 min