import requests
from datetime import datetime
import time
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
coins = ["BTCUSDT", "ETHUSDT", "LTCUSDT"]
H_price_treshold = {"BTCUSDT": 101600.0, "ETHUSDT": 3300.0, "LTCUSDT": 300.0}
L_price_treshold = {"BTCUSDT": 101000.0, "ETHUSDT": 3000.0, "LTCUSDT": 50.0}
check_interval = 60
# counter = 0
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

BOT_TOKEN = TELEGRAM_BOT_TOKEN
BOT_CHAT_ID = CHAT_ID


def send_telegram_message(message):
    """Send alert message to telegram."""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": BOT_CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Telegram message sent successfully.")
        else:
            print(
                f"Failed to send Telegram message. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending Telegram message: {e}")


def send_email(subject, body, to_email):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    from_email = EMAIL_ADDRESS
    password = EMAIL_PASSWORD
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully.")

    except Exception as e:
        print("Failed to send email:", e)


while True:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for coin in coins:
        try:
            response = requests.get(
                f"https://api.binance.com/api/v3/ticker/price?symbol={coin}")
            data = response.json()
            price = float(data['price'])
            print(f"Current price of {coin} on Binance: ${price}")

            with open(r"C:\something not nice\hello world\crypto_price_log.txt", "a") as file:
                file.write(f"{current_time} - {coin} Price: ${price}\n")

                print(f"Price logged successfully at {current_time}.")

            if price > H_price_treshold[coin]:
                send_telegram_message(
                    f"Alert: {coin} price has exceeded the threshold! Current Price: {price}")

                print("")

            elif price < L_price_treshold[coin]:

                send_telegram_message(
                    f"Alert: {coin} price has fallen below the threshold!. Current Price: {price}")
                print("")
            else:
                print("All crypto prices is within the normal range.")
        except Exception as e:
            error_message = f"[{current_time}] error fetching data for {coin}: {e}\n"
            print(error_message)
            with open(r"C:\something not nice\hello world\error_log.txt", "a") as error_file:
                file.write(error_message)

   # counter += 1
    # if counter >= 3:
     #   print("Completed 10 checks, exiting.")
      #  break

    time.sleep(check_interval)
