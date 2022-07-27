import unittest

from stere import Stere
from splinter import Browser
from selenium.webdriver.common.keys import Keys
from src.pages.home_page import Home_Page


# https://github.com/cobrateam/splinter/blob/master/samples/test_google_search.py

class TensorTestCase(unittest.TestCase):
    def setUp(self):
        Stere.browser = Browser("chrome")
        Stere.url_navigator = 'visit'
        Stere.base_url = "http://www.yandex.ru/"
        self.hp = Home_Page()
        self.hp.navigate()

    def tearDown(self):
        Stere.browser.quit()

    def test_search(self):
        browser = Browser("chrome")
        browser.visit("http://www.yandex.ru")
        search_bar = browser.find_by_xpath("//form[@role='search']//input[not(@type='hidden')]").first
        assert search_bar.visible
        search_bar.click()
        search_bar.fill("Тензор")
        suggestions = browser.find_by_xpath(
            "//li[contains(@id, 'suggest-item-') and @role='option' and @data-type='fulltext']")
        assert suggestions.visible
        search_bar.type(Keys.ENTER)
        results = browser.find_by_xpath('//ul[@id="search-result"]')
        assert results.visible
        top_result = browser.find_by_xpath("//li[contains(@class, 'serp-item')]").first
        assert top_result.links.find_by_href("https://tensor.ru/")
        browser.quit()

    def test_pictures(self):
        self.hp.click_navigation("Картинки", True, Stere.browser)


