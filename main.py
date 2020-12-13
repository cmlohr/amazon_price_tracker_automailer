from bs4 import BeautifulSoup
import smtplib
import requests
import time

# while loop delay
SLEEP_TIME = 60  # in seconds

# Item I'm watching
SOURCE = "_YOUR_INPUT_"  # url of your item
HTML_CLASS = "_YOUR_INPUT_"  # inspect the html to get the class
TARGET_PRICE = 100.00  # Raise price to test code
ITEM = "_YOUR_INPUT_"  # Item name for the email

# Headers obtained from myhttpheader.com
ACCEPT_LANGUAGE = "_YOUR_INPUT_"  # your input
USER_AGENT = "_YOUR_INPUT_"  # your input

# smtplib mailer setup
FROM_EMAIL = "__YOUR_EMAIL__"  # your input
PASSWORD = "__YOUR_EMAIL_PW__"  # your input
GMAIL_SMTP = "smtp.gmail.com"  # set to google
TO_EMAIL = "__THE_EMAIL_RECIPIENT_"  # your input
PORT = "587"

# making the amazon get header
az_header = {
    "User-Agent": USER_AGENT,
    "Accept-Language": ACCEPT_LANGUAGE,
}

# scraping amazon and making some soup
amazon_query = requests.get(SOURCE, headers=az_header)
response = amazon_query.text
soupy_mess = BeautifulSoup(response, "lxml")
grab_price = soupy_mess.find(name="span", class_=HTML_CLASS)
price_text = grab_price.getText()
price = float(price_text.split("$")[1])


# price target check
def price_check():
    if price < TARGET_PRICE:
        return True

    else:
        return False


# using an infinite loop so the code may be run in the cloud continuously
while True:
    time.sleep(SLEEP_TIME)
    if price_check():
        with smtplib.SMTP(GMAIL_SMTP, port=PORT) as connect:
            connect.starttls()
            connect.login(user=FROM_EMAIL, password=PASSWORD)
            connect.sendmail(
                from_addr=FROM_EMAIL,
                to_addrs=TO_EMAIL,
                msg=f"Subject: Amazon price drop!\n\nYour watched item: {ITEM} is now {price}!\nCheck it out: {SOURCE}"
            )
