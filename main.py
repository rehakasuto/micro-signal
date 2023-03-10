__author__ = "Reha Kasuto"
__version__ = "0.2.3"

from types import SimpleNamespace

import requests
import json
import common as c
from datetime import datetime
import telegram_functions as tf

print(f"©Micro Signal OMEGA Scalp islemler icin tasarlanmis uyarici calismaya basladi. {datetime.now()} - v{__version__}")
print(f"Calisiyor ...")

settings = json.load(open("settings.json", "r"), object_hook=lambda d: SimpleNamespace(**d))

t = settings.telegram
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
                main_message = f"{symbol} icin {interval} mumlarda degisim orani {change_ratio}"
                c.log_info(f'{datetime.now()} - {main_message}', True)
                if t.isActive:
                    tf.send_message_to_telegram(t.token, f"🔴 <b>{symbol}</b> 🔴 \n {interval} mumlarda değişim oranı <b>{change_ratio}</b>")
    except Exception as e:
        c.log_error(f"{datetime.now()} || {e}")
        pass
