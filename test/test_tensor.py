import unittest

import allure
import pytest
from stere import Stere
from splinter import Browser
from src.pages.home_page import Home_Page

from src.pages.search_results import Search_Results


class TensorTestCase(unittest.TestCase):
    def setUp(self):
        self.browser_setup()
        self.navigate_to_home_page()

    def browser_setup(self):
        Stere.browser = Browser("chrome")
        Stere.url_navigator = 'visit'
        Stere.base_url = "http://www.yandex.ru/"

    def navigate_to_home_page(self):
        self.hp = Home_Page()
        self.hp.navigate()

    def tearDown(self):
        Stere.browser.quit()

    @allure.title('Поиск в яндексе')
    @allure.severity(allure.severity_level.NORMAL)
    def test_search(self):
        self.hp.search_form.input_query("Тензор")
        self.hp.search_form.submit()

        sr = Search_Results()
        top_result = sr.get_top_result()
        assert 'tensor.ru' in top_result.link.element['href']

    @allure.title('Картинки в яндексе')
    def test_pictures(self):
        self.hp.navigation.click_navigation("Картинки", True, Stere.browser)


