__author__ = "Reha Kasuto"
__version__ = "0.3.2"

import sys
from types import SimpleNamespace
import requests
import json
import common as c
from datetime import datetime
import telegram_functions as tf
import google_drive_functions as gdf

print(f"©Micro Signal OMEGA Scalp islemler icin tasarlanmis uyarici calismaya basladi. {datetime.now()} - v{__version__}")
print(f"Calisiyor ...")

settings = json.load(open("settings.json", "r"), object_hook=lambda d: SimpleNamespace(**d))

telegram_config = None
if hasattr(settings, 'telegram'):
    telegram_config = settings.telegram
interval = settings.interval
base_url = settings.baseUrl
volume_usdt = int(settings.volumeUsdt)
change_ratio_at_least = int(settings.changeRatioAtLeast)

app_license = None
license_key = None
license_email = None
if hasattr(settings, 'license'):
    app_license = settings.license
    if hasattr(app_license, "key"):
        license_key = app_license.key
    if hasattr(app_license, "email"):
        license_email = app_license.email

if app_license is None or app_license == "" or license_key is None or license_key == "" or license_email is None or license_email == "":
    c.log_error(f"{datetime.now()} || Lütfen lisans bilginizi giriniz.")
    sys.exit()

while True:
    try:
        response = requests.get(f"{base_url}/ticker/24hr").json()
        filtered_data = [item for item in response if
                         item['symbol'].endswith('USDT') and float(item['quoteVolume']) > volume_usdt]

        for ticker in filtered_data:
            license_data = gdf.get_data_by_email(license_email)
            if license_data is None or license_data[1] != license_key or datetime.now() > datetime.strptime(
                    license_data[2],
                    '%m-%d-%Y'):
                c.log_error(f"{datetime.now()} || Lisans bilginiz hatalı veya geçersizdir")
                sys.exit()

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
                if telegram_config is not None and telegram_config.isActive:
                    tf.send_message_to_telegram(telegram_config.token, f"🔴 <b>{symbol}</b> 🔴 \n {interval} mumlarda değişim oranı <b>{change_ratio}</b>")
    except Exception as e:
        c.log_error(f"{datetime.now()} || {e}")
        pass
