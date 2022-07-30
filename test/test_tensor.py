import unittest

import allure
import splinter
from stere import Stere
from src.pages.home_page import Home_Page
from src.pages.images_page import Images_Page
from src.pages.captcha_page import Captcha_Page
from test.utils.browser_provider import get_browser

from src.pages.search_results import Search_Results


class TensorTestCase(unittest.TestCase):
    def setUp(self):
        self.browser_setup()
        self.navigate_to_home_page()

    def browser_setup(self):
        Stere.browser = get_browser()
        Stere.url_navigator = 'visit'
        Stere.base_url = "http://www.yandex.ru/"

    def navigate_to_home_page(self):
        self.hp = Home_Page()
        self.hp.navigate()
        try:
            assert Captcha_Page().form.checkbox.element.visible
        except splinter.exceptions.ElementDoesNotExist:
            pass
        else:
            assert False, "Открылась страница с капчей"

    def tearDown(self):
        Stere.browser.quit()

    @allure.title('Поиск в яндексе')
    @allure.severity(allure.severity_level.NORMAL)
    def test_search(self):
        self.hp.search_form.input_query("Тензор")
        self.hp.search_form.submit()

        sr = Search_Results('text')
        sr.assert_top_result_leads_to_site('tensor.ru')

    @allure.title('Картинки в яндексе')
    def test_pictures(self):
        self.hp.navigation.click_navigation("Картинки", True, Stere.browser)
        ip = Images_Page(Stere.browser)
        top_category = ip.popular_items.get_top_item()

        sr = ip.popular_items.click_category(top_category)
        sr.search_form.assert_query(top_category)
        top_result = sr.get_top_result()

        iv = sr.click_result(top_result)
        top_image = iv.download_current_image()
        iv.next()
        iv.compare_images(False, top_image)
        iv.prev()
        iv.compare_images(True, top_image)
