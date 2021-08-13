from parsing_module import set_params, parse_all_pages
import time
import asyncio
import aiohttp
from input_handler import get_place, get_check_in_date, get_check_out_date
from input_handler import get_number_adults, get_number_of_children, get_number_of_rooms


def main():
    """
    The main entry point of the application
    """
    place = get_place()
    check_in_date = get_check_in_date()
    check_out_date = get_check_out_date()
    number_of_adults = get_number_adults()
    number_of_children = get_number_of_children()
    number_of_rooms = get_number_of_rooms()

    # start_time = time.time()

    params = set_params(place,
                        check_in_date,
                        check_out_date,
                        number_of_adults,
                        number_of_children,
                        number_of_rooms)
    asyncio.run(parse_all_pages(params))

    # print(time.time() - start_time)


if __name__ == '__main__':
    main()
