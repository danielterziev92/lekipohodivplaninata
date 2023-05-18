import datetime


def from_cyrillic_to_latin(value):
    symbols = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ж': 'j', 'з': 'z', 'и': 'i', 'й': 'i',
        'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'x', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sht', 'ъ': 'a', 'ь': 'y', 'ю': 'yu',
        'я': 'ya',
    }

    new_string = ''

    for ch in value:
        if ch.isnumeric():
            new_string += ch
            continue

        new_string += symbols.get(ch.lower(), ' ')

    return new_string


def from_str_to_date(value):
    date = None
    if isinstance(value, str):
        date = datetime.datetime.strptime(value, '%Y-%m-%d')

    return date.strftime('%d-%m-%Y')


print(from_cyrillic_to_latin('От тук до там 2'))
