__author__ = "Reha Kasuto"
__version__ = "0.1.6"

from types import SimpleNamespace

import requests
import json
import common as c
from datetime import datetime

c.log_info(f"©Micro Signal alerter has started to working. {datetime.now()} - v{__version__}")
c.log_info(f"Running ...")

settings = json.load(open("settings.json", "r"), object_hook=lambda d: SimpleNamespace(**d))

interval = settings.interval
base_url = settings.baseUrl
volume_usdt = int(settings.volumeUsdt)
change_ratio_at_least = int(settings.changeRatioAtLeast)

while True:
    try:
        response = requests.get(f"{base_url}/ticker/24hr").json()
        filtered_data = [item for item in response if
                         item['symbol'].endswith('USDT') and float(item['quoteVolume']) > volume_usdt]

        for ticker in filtered_data:
            symbol = ticker['symbol']

            response = requests.get(f"{base_url}/klines?symbol={symbol}&interval={interval}&limit=2")
            klines = response.json()

            current_close_price = float(klines[1][4])
            previous_close_price = float(klines[0][4])
            calculated_change_ratio = (current_close_price - previous_close_price) / previous_close_price
            change_ratio = round(calculated_change_ratio * 100, 2)

            if change_ratio < 0:
                continue

            if change_ratio > change_ratio_at_least:
                c.log_info(f'{datetime.now()} - Change ratio for {symbol} on {interval} interval: {change_ratio}')
    except Exception as e:
        c.log_error(f"{datetime.now()} || {e}")
        pass
