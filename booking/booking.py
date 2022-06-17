from datetime import date
from msilib.schema import tables
import booking.config as config
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport
import time
import pandas as pd


class Booking(webdriver.Chrome):
    def __init__(self, driver_path= config.DRIVER_LOCATION, tear_down=False):
        self.driver_path = driver_path
        self.tear_down = tear_down
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Booking, self).__init__(self.driver_path, options = options)
        self.implicitly_wait(15)
        self.maximize_window()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.tear_down:
            self.quit()

    def land_first_page(self):
        self.get(config.BASE_URL)
    
    def change_currency(self, currency=None):
        currency_element = self.find_element(By.CSS_SELECTOR,  \
            'button[data-tooltip-text = "Choose your currency"]'
        )
        currency_element.click()

        selected_currency_element = self.find_element(By.CSS_SELECTOR, \
            f'a[data-modal-header-async-url-param*="selected_currency={currency}"]' #use *= for substring
        )
        selected_currency_element.click()

    def change_language(self, language=None):
        language_element = self.find_element(By.CSS_SELECTOR, \
            'button[data-modal-id = "language-selection"]'
        )
        language_element.click()

        selected_language_element = self.find_element(By.CSS_SELECTOR, \
            f'div[class="bui-inline-container__main"][lang={language}]'    
        )
        selected_language_element.click()

    def select_place_to_go(self, place_to_go):
        search_field = self.find_element(By.ID, 'ss')
        search_field.clear()
        search_field.send_keys(place_to_go)
        
        first_result = self.find_element(By.CSS_SELECTOR, 'li[data-i="0"]')
        first_result.click()

    def select_dates(self, check_in_date, check_out_date):
        check_in_click_distance, check_out_click_distance = self._count_click_away(check_in_date, check_out_date)

        date_board_next_element = self.find_element(By.CSS_SELECTOR, \
            'div[data-bui-ref="calendar-next"]'
        )

        self._navigate_date_board(
            check_in_click_distance, date_board_next_element, check_in_date
        )
        
        self._navigate_date_board(
            check_out_click_distance, date_board_next_element, check_out_date
        )

    def _navigate_date_board(self, click_distance, date_board_next_element, register_date):
        if click_distance > 0:
            for _ in range(click_distance):
                date_board_next_element.click()

        register_element = self.find_element(
            By.CSS_SELECTOR, f'td[data-date="{register_date}"]'
        )

        register_element.click()

    def _count_click_away(self, check_in_date, check_out_date):
        check_in_month_diff = self._calculate_month_diff(date.today(), check_in_date)
        check_out_month_diff = self._calculate_month_diff(check_in_date, check_out_date)
        check_in_click_distance = 0 if check_in_month_diff <= 2 else check_in_month_diff-1
        check_out_click_distance = 0 if check_out_month_diff <= 2 else check_out_month_diff-1
        return check_in_click_distance, check_out_click_distance

    def _calculate_month_diff(self, date1, date2):
        if isinstance(date1, str):
            date1 = datetime.strptime(date1.strip(), "%Y-%m-%d")
        if isinstance(date2, str):
            date2 = datetime.strptime(date2.strip(), "%Y-%m-%d")
        return (date2.year - date1.year) * 12 + (date2.month-date1.month)

    def select_adults(self, count=1):
        selection_element = self.find_element(By.ID, 'xp__guests__toggle')
        selection_element.click()

        while True:
            decrease_adults_element = self.find_element(By.CSS_SELECTOR, \
                'button[aria-label="Decrease number of Adults"]'
            )
            decrease_adults_element.click()

            adults_value_element = self.find_element(By.ID, 'group_adults')
            adults_value = adults_value_element.get_attribute('value') #get the adult count

            if int(adults_value) == 1:
                break
        
        increase_adults_element = self.find_element(By.CSS_SELECTOR, \
            'button[aria-label="Increase number of Adults"]'
        )
        for _ in range(count-1):
            increase_adults_element.click()
            
    def submit(self):
        submit_element = self.find_element(By.CSS_SELECTOR,
            'button[type="submit"]'
        )
        submit_element.click()

    def apply_filtration(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(4, 5)
        time.sleep(1)
        filtration.sort_price_lowest_first()

    def report_results(self):

        report = BookingReport(driver=self)
        print(pd.DataFrame(report.pull_deal_info(), columns=[
            'hotel_name',
            'currency',
            'price',
            'score',
            'star'
        ]))
        

        

        

