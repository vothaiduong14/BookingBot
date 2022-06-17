# This module will include method to parse data from property cards

from booking.config import DRIVER_LOCATION
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
import html

class BookingReport:
    def __init__(self, driver:WebDriver):
        self.driver = driver
        self.deal_boxes = self.pull_deal_boxes()
    
    def pull_deal_boxes(self):
        return self.driver.find_elements(By.CSS_SELECTOR, 
            'div[data-testid=property-card]'
        )
    
    def pull_deal_info(self):
        collection = []
        for deal_box in self.deal_boxes:
            hotel_name = deal_box.find_element(By.CSS_SELECTOR,
                'div[data-testid="title"]'
            ).get_attribute('innerHTML').strip()
            hotel_name = html.unescape(hotel_name)

            hotel_price_and_currency = deal_box.find_element(By.CSS_SELECTOR,
                'div[data-testid="price-and-discounted-price"]'
            ).find_element(By.CSS_SELECTOR, '*').get_attribute('innerHTML').strip()
            hotel_currency, hotel_price = hotel_price_and_currency.split(";")

            hotel_score = deal_box.find_element(By.CSS_SELECTOR,
                'div[data-testid="review-score"]'
            ).find_elements(By.CSS_SELECTOR, '*')[0].get_attribute('innerHTML').strip()

            hotel_star = deal_box.find_element(By.XPATH,
                '//div[@data-testid="rating-stars" or @data-testid="rating-square"]'
            ).find_elements(By.CSS_SELECTOR, 'span[aria-hidden="true"]')

            collection.append(
                [
                    hotel_name,
                    hotel_currency[:3],
                    hotel_price,
                    hotel_score,
                    len(hotel_star),
                ]
            )

        return collection