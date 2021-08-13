import re


def get_place(prompt: str = "Введите место/название объекта: "):
    place = input(prompt)
    return place


def get_check_in_date(prompt: str = "Введите дату заезда в формате дд.мм.гггг: "):
    while True:
        check_in_date = input(prompt).strip()
        if re.match(r"\d{2}.\d{2}.\d{4}", check_in_date):
            return check_in_date.split('.')
        else:
            print("Неправильный формат данных")


def get_check_out_date(prompt: str = "Введите дату отъезда в формате дд.мм.гггг: "):
    while True:
        check_out_date = input(prompt).strip()
        if re.match(r"\d{2}.\d{2}.\d{4}", check_out_date):
            return check_out_date.split('.')
        else:
            print("Неправильный формат данных")


def get_number_adults(prompt: str = "Введите количество взрослых: "):
    while True:
        number_of_adults = input(prompt).strip()
        if number_of_adults.isdigit():
            return number_of_adults
        else:
            print("Неправильный формат данных")


def get_number_of_children(prompt: str = "Введите количество детей: "):
    while True:
        number_of_children = input(prompt).strip()
        if number_of_children.isdigit():
            return number_of_children
        else:
            print("Неправильный формат данных")


def get_number_of_rooms(prompt: str = "Введите количество номеров: "):
    while True:
        number_of_rooms = input(prompt).strip()
        if number_of_rooms.isdigit():
            return number_of_rooms
        else:
            print("Неправильный формат данных")


if __name__ == '__main__':
    get_place()
    get_check_in_date()
    get_number_adults()
