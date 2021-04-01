import time
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client

from config import *


class Item:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __str__(self):
        return self.name

    def is_in_stock(self):
        req = requests.get(self.url, headers=HEADERS)
        soup = BeautifulSoup(req.content, features='html.parser')

        add_to_cart_button = soup.find('button', {'class': 'add-to-cart-button'})

        return add_to_cart_button.text != 'Sold Out'

    @property
    def in_stock_message(self):
        return f"{self.name} in stock:\n\n{self.url}"

    def sleep(self, seconds):
        pass


founders_3070 = Item("3070 Founder's Edition", "https://www.bestbuy.com/site/nvidia-geforce-rtx-3070-8gb-gddr6-pci-express-4-0-graphics-card-dark-platinum-and-black/6429442.p?skuId=6429442")
evga_3070_ftw3_ultra = Item("EVGA 3070 FTW3 Ultra", "https://www.bestbuy.com/site/evga-geforce-rtx-3070-ftw3-ultra-gaming-8gb-gddr6-pci-express-4-0-graphics-card/6439301.p?skuId=6439301")
evga_3070_xc3_ultra = Item("EVGA 3070 XC3 Ultra", "https://www.bestbuy.com/site/evga-geforce-rtx-3070-xc3-ultra-gaming-8gb-gddr6-pci-express-4-0-graphics-card/6439299.p?skuId=6439299")


founders_3080 = Item("3080 Founder's Edition", "https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440")
evga_3080_ftw3_ultra = Item("EVGA 3080 FTW3 Ultra", "https://www.bestbuy.com/site/evga-geforce-rtx-3080-ftw3-ultra-gaming-10gb-gddr6-pci-express-4-0-graphics-card/6436196.p?skuId=6436196")
evga_3080_xc3_ultra = Item("EVGA 3080 XC3 Ultra", "https://www.bestbuy.com/site/evga-geforce-rtx-3080-xc3-ultra-gaming-10gb-gddr6-pci-express-4-0-graphics-card/6432400.p?skuId=6432400")

test = Item('Test', 'https://www.bestbuy.com/site/nintendo-switch-monster-hunter-rise-deluxe-edition-system-gray-gray/6454044.p?skuId=6454044')

def main():
    twilio_client = Client(ACCOUNT_SSID, AUTH_TOKEN)
    cards = [founders_3070, evga_3070_ftw3_ultra, evga_3070_xc3_ultra, founders_3080, evga_3080_ftw3_ultra, evga_3080_xc3_ultra, test]

    while True:
        for card in cards:
            time.sleep(1)

            if card.is_in_stock():
                twilio_client.messages.create(
                    body = card.in_stock_message,
                    from_ = PHONE_FROM,
                    to = PHONE_TO 
                )
                print(card.in_stock_message)

            else:
                print(card.name + " not in stock.")

if __name__ == '__main__':
    main()
