import requests
from bs4 import BeautifulSoup

host = "https://www.booking.com"
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.135 Safari/537.36',
    }


def turn_to_digit(dirty_string: str):
    clear_string = ""
    for i in dirty_string:
        if i.isdigit():
            clear_string += i
    return int(clear_string)

# fix date
def set_params(place,
               checkin_year,
               checkin_month,
               checkin_monthday,
               checkout_year,
               checkout_month,
               checkout_monthday,
               number_of_adults,
               number_of_children,
               number_of_rooms
               ):

    """set params for the parsing request"""

    params = {
        "ss": place,
        "checkin_year": checkin_year,
        "checkin_month": checkin_month,
        "checkin_monthday": checkin_monthday,
        "checkout_year": checkout_year,
        "checkout_month": checkout_month,
        "checkout_monthday": checkout_monthday,
        "group_adults": number_of_adults,
        "group_children": number_of_children,
        "no_rooms": number_of_rooms
    }
    return params


def get_number_of_pages(params, search_page_url=f"{host}/searchresults.ru.html"):
    """get the number of searched pages from pagination"""

    response = requests.get(url=search_page_url, headers=headers, params=params)
    search_page_html = response.content

    with open("aaaa.html", "wb") as file:
        file.write(search_page_html)
        print("file")

    search_page_soup = BeautifulSoup(search_page_html, "lxml")
    pagination_items = search_page_soup.find_all("li", class_="bui-pagination__item sr_pagination_item")
    if len(pagination_items) == 0:
        return 1
    last_page_number = int(pagination_items[-1].find('div', class_='bui-u-inline').text)
    return last_page_number


def get_data_from_page(current_page_number, params: dict, search_page_url=f"{host}/searchresults.ru.html"):
    """get required data (titles and prices) from a single page"""
    params["offset"] = str(current_page_number * 25)
    response = requests.get(url=search_page_url, headers=headers, params=params)
    # print(response.url)
    search_page_html = response.content
    search_page_soup = BeautifulSoup(search_page_html, "lxml")
    hotel_cards = search_page_soup.find_all("div", class_=['sr_item', 'sr_item_new', 'sr_item_default',
                                                           'sr_property_block', 'sr_flex_layout'])

    if len(hotel_cards) == 0:
        print("Информация отсутствует.")

    hotel_names = list()
    hotel_prices = list()
    for hotel_card in hotel_cards:
        hotel_names.append(hotel_card.find("span", class_="sr-hotel__name").text)

        # create a better way
        price_container = hotel_card.find_all("div", class_="prco-inline-block-maker-helper")[1]
        hotel_prices.append(price_container.find("div", class_=['bui-price-display__value',
                                                                'prco-inline-block-maker-helper']).text)

    return hotel_names, hotel_prices
