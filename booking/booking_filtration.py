# This class apply filtration to the search results.
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class BookingFiltration:
    def __init__(self, driver:WebDriver): #this is similar to type suggestion
        self.driver = driver # receive driver from the original booking class
        

    def apply_star_rating(self, *star_values):
        star_filtration_box = self.driver.find_element(By.CSS_SELECTOR, 
            'div[data-filters-group="class"]'
        )
        star_child_elements = star_filtration_box.find_elements(By.CSS_SELECTOR, '*') # get all elements

        for star_value in star_values: # allow picking multiple values
            for star_element in star_child_elements:
                if str(star_element.get_attribute('innerHTML')).strip() == f'{star_value} stars':
                    star_element.click()

    def sort_price_lowest_first(self):
        try: # this handles case when the sort option is visible
            price_sort_element = self.driver.find_element(By.CSS_SELECTOR,
                'li[data-id="price"]'
            )
        except NoSuchElementException:
            quick_sort_menu = self.driver.find_element(By.CSS_SELECTOR,
                'button[data-testid="sorters-dropdown-trigger"]'
            )
            quick_sort_menu.click()
            price_sort_element = self.driver.find_element(By.CSS_SELECTOR,
                'button[data-id="price"]'
            )
        price_sort_element.click()