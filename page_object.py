from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


class FindHelpers:
    """поиск с ожиданием элементов на странице"""
    def __init__(self, driver):
        self.driver = driver

    def find_element_with_wait(self, selector, wait_time=10):
        """поиск элемента с ожиданием"""
        return WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located(selector), 'Не дождались появления элемента')

    def find_elements_with_wait(self, selector, wait_time=10):
        """поиск нескольких элементов с ожиданием"""
        return WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_all_elements_located(selector), 'Не дождались появления элементов')


class HeadPage(FindHelpers):

    def __init__(self, driver):
        FindHelpers.__init__(self, driver)

    status_code_window = (By.CLASS_NAME, "response-code")
    response_window = (By.CSS_SELECTOR, '[data-key="output-response"]')
    request_buttons = (By.CLASS_NAME, 'endpoints')

    def click_request_button(self, button_name):

        request_button = self.find_element_with_wait((By.CSS_SELECTOR, f'[data-id="{button_name}"]'))
        request_button.click()

    def compare_status_code(self, api_status_code):

        # status_code = self.find_element_with_wait(self.status_code_window)
        WebDriverWait(self.driver, 5).until(
            EC.text_to_be_present_in_element(self.status_code_window, str(api_status_code)),
            'Не дождались появления статус кода')

    def get_response_text(self):

        response = self.find_element_with_wait(self.response_window, 5)
        WebDriverWait(self.driver, 5).until(
            EC.text_to_be_present_in_element(self.response_window, "{"), 'Не дождались появления текста')

        return json.loads(response.text)
