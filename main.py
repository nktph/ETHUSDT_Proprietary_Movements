import requests
import time
import numpy as np
from scipy.stats import linregress

# Константы для запросов
BASE_URL = 'https://fapi.binance.com'
SYMBOL = 'ETHUSDT'
INTERVAL = '1m'

# Начальное значение цены
price_list = []
last_price = None

# Функция для определения собственных движений цены
def get_trend(price_list):
    x = np.arange(len(price_list))
    slope, _, rvalue, _, _ = linregress(x, price_list)
    return slope * 60, rvalue ** 2

# Функция для получения цены
def get_price():
    try:
        response = requests.get(f'{BASE_URL}/fapi/v1/klines', params={'symbol': SYMBOL, 'interval': INTERVAL})
        data = response.json()
        close_price = float(data[-1][4])
        return close_price
    except Exception as e:
        print(f'Ошибка при получении цены: {e}')
        time.sleep(5)
        return None

# Главный цикл программы
while True:
    # Получаем текущую цену
    current_price = get_price()

    if current_price is not None:
        # Добавляем текущую цену в список цен
        price_list.append(current_price)

        # Удаляем старые значения цен
        if len(price_list) > 60:
            price_list.pop(0)

        # Определяем изменение цены за последний час
        price_change = (current_price - price_list[0]) / price_list[0] * 100

        # Определяем собственные движения цены
        trend, r_squared = get_trend(price_list)

        # Выводим сообщение о изменении цены, если изменение составляет более 1%
        if abs(price_change) > 1:
            print(f'Изменение цены за последний час: {price_change:.2f}%')

        # Выводим сообщение о собственных движениях цены
        if r_squared > 0.5:
            if trend > 0:
                print('Тенденция роста цены. Текущая цена:'+str(current_price))
            elif trend < 0:
                print('Тенденция падения цены. Текущая цена:'+str(current_price))
            else:
                print('Цена стабильна')

    # Ждем 5 секунд перед следующим запросом
    time.sleep(5)
