import requests
import common as c


def send_message_to_telegram(token, message):
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id=-1001740351052&parse_mode=HTML"

        textdata = {"text": message}
        requests.request("POST", url, params=textdata)
    except Exception as e:
        message = str(e) + "Exeption occured while sending a message to Telegram"
        c.log_error(message)
