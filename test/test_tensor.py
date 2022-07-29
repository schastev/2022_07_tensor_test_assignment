import unittest

import allure
from stere import Stere
from splinter import Browser
from src.pages.home_page import Home_Page
from src.pages.images_page import Images_Page

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
        sr.assert_top_result_leads_to_site('tensor.ru')

    @allure.title('Картинки в яндексе')
    def test_pictures(self):
        self.hp.navigation.click_navigation("Картинки", True, Stere.browser)
        ip = Images_Page(Stere.browser)
        top_category = ip.popular_items.get_top_item()
        ip.popular_items.click_category(top_category)



