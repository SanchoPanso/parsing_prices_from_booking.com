import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pandas as pd

host = "https://www.booking.com"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/91.0.4472.135 Safari/537.36',
    }
hotel_data = []
page_count = 0


def turn_to_digit(dirty_string: str):
    clear_string = ""
    for i in dirty_string:
        if i.isdigit():
            clear_string += i
    return int(clear_string)


# fix date
def set_params(place: str,
               checkin_date: tuple,
               checkout_date: tuple,
               number_of_adults: str,
               number_of_children: str,
               number_of_rooms: str
               ):

    """set params for the parsing request"""

    params = {
        "ss": place,
        "checkin_year": checkin_date[2],
        "checkin_month": checkin_date[1],
        "checkin_monthday": checkin_date[0],
        "checkout_year": checkout_date[2],
        "checkout_month": checkout_date[1],
        "checkout_monthday": checkout_date[0],
        "group_adults": number_of_adults,
        "group_children": number_of_children,
        "no_rooms": number_of_rooms
    }
    return params


async def get_number_of_pages(params, search_page_url=f"{host}/searchresults.ru.html"):
    """get the number of searched pages from pagination"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url=search_page_url, headers=headers, params=params) as response:
            search_page_text = await response.text()
            search_page_html = await response.content.read()

    search_page_soup = BeautifulSoup(search_page_text, "lxml")
    pagination_items = search_page_soup.find_all("li", class_="bui-pagination__item sr_pagination_item")
    if len(pagination_items) == 0:
        return 1
    last_page_number = int(pagination_items[-1].find('div', class_='bui-u-inline').text)
    return last_page_number


async def get_data_from_page(current_page_number: int,
                             params: dict,
                             session: aiohttp.ClientSession,
                             search_page_url=f"{host}/searchresults.ru.html"):
    """get required data (titles and prices) from a single page"""
    global hotel_data, page_count
    params["offset"] = str(current_page_number * 25)
    async with session.get(url=search_page_url, headers=headers, params=params) as response:
        search_page_html = await response.text()

    search_page_soup = BeautifulSoup(search_page_html, "lxml")
    hotel_cards = search_page_soup.find_all("div", class_=['sr_item', 'sr_item_new', 'sr_item_default',
                                                           'sr_property_block', 'sr_flex_layout'])

    # if len(hotel_cards) == 0:
    #     print(f"Информация отсутствует в {current_page_number} стр")

    hotel_data = []
    for hotel_card in hotel_cards:
        hotel_name = hotel_card.find("span", class_="sr-hotel__name").text

        price_container = hotel_card.find_all("div", class_="prco-inline-block-maker-helper")[1]
        hotel_price = price_container.find("div", class_=['bui-price-display__value',
                                                          'prco-inline-block-maker-helper']).text
        hotel_data.append([hotel_name, hotel_price])

    page_count += 1
    print(f"Обработано {page_count} стр")
    return hotel_data


async def parse_all_pages(params):
    """parse required information (titles and prices) from all found pages"""

    number_of_page = await get_number_of_pages(params)
    print(f"Количество страниц: {number_of_page}")

    tasks = []
    async with aiohttp.ClientSession() as session:
        for current_page_number in range(number_of_page):   # number_of_page
            task = asyncio.create_task(get_data_from_page(current_page_number, params, session))
            tasks.append(task)
        await asyncio.gather(*tasks)

    all_hotel_names = [i[0] for i in hotel_data]
    all_hotel_prices = [i[1] for i in hotel_data]

    df = pd.DataFrame({"Отель": all_hotel_names, "Цена": all_hotel_prices})
    df.to_excel("output.xlsx", index=False)

    print("Готово")
