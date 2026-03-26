import requests
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import mplfinance as mpf
from datetime import datetime

matplotlib.use('TkAgg')

def get_bybit_klines(symbol, interval, limit=200):
    base_url = "https://api.bybit.com"
    endpoint = "/v5/market/kline"

    params = {
        'category': 'linear',
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }

    response = requests.get(base_url + endpoint, params=params)
    data = response.json()

    if data['retCode'] != 0:
        raise Exception(f"API Error: {data['retMsg']}")

    klines = data['result']['list']

    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume', 'turnover'
    ])

    df = df.astype({
        'open': float, 'high': float, 'low': float, 'close': float,
        'volume': float, 'turnover': float
    })

    df['timestamp'] = pd.to_datetime(df['timestamp'].astype('int64'), unit='ms')
    df = df.sort_values('timestamp')
    df.set_index('timestamp', inplace=True)

    return df

def plot_crypto_chart(symbol, interval='15', limit=100):
    try:
        df = get_bybit_klines(symbol, interval, limit)

        print("Первая дата в данных:", df.index[0])
        print("Последняя дата в данных:", df.index[-1])

        mc = mpf.make_marketcolors(
            up='green', down='red',
            edge='inherit',
            wick='inherit',
            volume='in'
        )

        s = mpf.make_mpf_style(marketcolors=mc)

        fig, axes = mpf.plot(
            df,
            type='candle',
            style=s,
            title=f'{symbol} | {interval} минут | Последние {limit} свечей',
            ylabel='Цена (USDT)',
            volume=False,
            figsize=(12, 6),
            returnfig=True,
            #datetime_format='%Y-%m-%d %H:%M'
        )

        plt.savefig(f'{symbol}_candles.png')
        print(f"Свечной график сохранен как {symbol}_candles.png")

        plt.show()

    except Exception as e:
        print(f"Ошибка: {e}")

CRYPTO_SYMBOL = str(input("Введите пару (например BTCUSDT): ")).upper()
TIME_INTERVAL = str(input("Введите интервал (1, 3, 5, 15, 30, 60, 120, 240, 360, 720, D, M, W): "))
DATA_LIMIT = int(input("Введите лимит свечей (макс 200): "))

print(f"Загрузка данных для {CRYPTO_SYMBOL}...")
plot_crypto_chart(CRYPTO_SYMBOL, TIME_INTERVAL, DATA_LIMIT)
