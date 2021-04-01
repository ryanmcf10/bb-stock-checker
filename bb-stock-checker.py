import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from twilio.rest import Client

from config import *

twilio_client = Client(ACCOUNT_SSID, AUTH_TOKEN)

class Item:
    _sleep_start_time = None
    _consecutive_error_count = 0

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __str__(self):
        return self.name

    @property
    def in_stock_message(self):
        return f"{self.name} in stock:\n\n{self.url}"

    def is_in_stock(self):
        """
        Look at the status of the 'Add to Cart' button on the page.
        """
        req = requests.get(self.url, headers=HEADERS)
        soup = BeautifulSoup(req.content, features='html.parser')

        add_to_cart_button = soup.find('button', {'class': 'add-to-cart-button'})

        return add_to_cart_button.text != 'Sold Out'

    def sleep(self):
        """
        Set a timer to prevent receiving repeated texts about this Item after it is found in stock.
        """
        self._sleep_start_time = datetime.now()

    def is_sleeping(self):
        """
        Check if the Item is sleeping. Wake it up if enough time has passed.
        """
        if self._sleep_start_time is None:
            return False
        else:
            if (datetime.now() - self._sleep_start_time).seconds >= SLEEP_TIME_IN_MINUTES * 60:
                # Wake up
                self._sleep_start_time = None
                return False
            else:
                return True

    def record_success(self):
        self._consecutive_error_count = 0

    def record_error(self, error):
        """
        Check if Item should send a text notification due to too many errors.
        """
        self._consecutive_error_count += 1

        if self._consecutive_error_count == 10:
            self.sleep()

            message = f"Repeated error checking {self.name}:\n\n{error}"

            twilio_client.messages.create(
                body = message,
                from_ = PHONE_FROM,
                to = PHONE_TO
            )

def main():

    items = [
        Item("3070 Founder's Edition", "https://www.bestbuy.com/site/nvidia-geforce-rtx-3070-8gb-gddr6-pci-express-4-0-graphics-item-dark-platinum-and-black/6429442.p?skuId=6429442"),
        Item("EVGA 3070 FTW3 Ultra", "https://www.bestbuy.com/site/evga-geforce-rtx-3070-ftw3-ultra-gaming-8gb-gddr6-pci-express-4-0-graphics-item/6439301.p?skuId=6439301"),
        Item("EVGA 3070 XC3 Ultra", "https://www.bestbuy.com/site/evga-geforce-rtx-3070-xc3-ultra-gaming-8gb-gddr6-pci-express-4-0-graphics-item/6439299.p?skuId=6439299"),
        Item("3080 Founder's Edition", "https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-item-titanium-and-black/6429440.p?skuId=6429440"),
        Item("EVGA 3080 FTW3 Ultra", "https://www.bestbuy.com/site/evga-geforce-rtx-3080-ftw3-ultra-gaming-10gb-gddr6-pci-express-4-0-graphics-item/6436196.p?skuId=6436196"),
        Item("EVGA 3080 XC3 Ultra", "https://www.bestbuy.com/site/evga-geforce-rtx-3080-xc3-ultra-gaming-10gb-gddr6-pci-express-4-0-graphics-item/6432400.p?skuId=6432400"),
        #Item('Test', 'https://www.bestbuy.com/site/nintendo-switch-monster-hunter-rise-deluxe-edition-system-gray-gray/6454044.p?skuId=6454044')
    ]

    while True:
        for item in items:
            print("-"*60)
            print(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            if item.is_sleeping():
                print(f"{item} is sleeping.")
                continue

            time.sleep(1)

            print(f"Checking {item}.")

            try:
                if item.is_in_stock():
                    twilio_client.messages.create(
                        body = item.in_stock_message,
                        from_ = PHONE_FROM,
                        to = PHONE_TO 
                    )

                    item.sleep()

                    print("IN STOCK")

                else:
                    print("Not in stock.")

                item.record_success()

            except Exception as e:
                print(f"Failed.\n\n{e}")
                item.record_error(e)

if __name__ == '__main__':
    main()
