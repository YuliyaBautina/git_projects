import requests
import json
from config import keys


class ConvertionException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionException(f"Нельзя перевести валюту '{base}' в саму себя.")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту {quote}. Валюта отсутствует в списке доступных.")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту {base}. Валюта отсутствует в списке доступных.")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f"Количество '{amount}' должно быть числовым выражением. Отделяйте дробную часть суммы точкой.")

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        total__base = round((float(total_base) * float(amount)), 2)

        return total__base


class BaseConverter:
    @staticmethod
    def base_convert(base: str):
        if base == 'рубль':
            base = 'рублях'
        if base == 'доллар':
            base = 'долларах'
        if base == 'евро':
            base = 'евро'
        return base


class QuoteConvertor:
    @staticmethod
    def quote_convert(quote: str, amount: str):
        amount_end = int(amount) % 10
        if amount_end == 1 and int(amount) != 11 and quote == 'доллар':
            quote = 'доллара'
        if quote == 'доллар' and amount_end in (2, 3, 4, 5, 6, 7, 8, 9, 0):
            quote = 'долларов'
        if quote == 'доллар' and int(amount) == 11:
            quote = 'долларов'

        if amount_end == 1 and int(amount) != 11 and quote == 'рубль':
            quote = 'рубля'
        if amount_end in (2, 3, 4, 5, 6, 7, 8, 9, 0) and quote == 'рубль':
            quote = 'рублей'
        if quote == 'рубль' and int(amount) == 11:
            quote = 'рублей'

        return quote