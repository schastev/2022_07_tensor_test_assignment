from typing import Union

import allure
from stere import Page
from stere.areas import Area, RepeatingArea
from stere.fields import Root, Text, Field
from src.pages.search_results import Search_Results


class Popular_Items(RepeatingArea):
    def __init__(self, root: Field, **kwargs: Union[Field, Area]):
        super().__init__(root, **kwargs)
        self.items = RepeatingArea(
            root=Root('xpath', "//div[contains(@class, 'PopularRequestList-Item')]"),
            title=Text('xpath', ".//div[contains(@class, 'PopularRequestList-SearchText')]")
        )

    def get_top_item(self):
        return self.items.areas[0].title.element.text

    @allure.step('Кликнуть на категорию "{1}')
    def click_category(self, cat_name):
        self.items.areas.containing('title', cat_name)[0].title.click()
        return Search_Results('image')


class Images_Page(Page):
    @allure.step('Перейти в раздел "Картинки"')
    def __init__(self, browser):
        self.popular_items = Popular_Items(
            root=Root('xpath', "//div[contains(@class, 'PopularRequestList-Item')]"),
            title=Text('xpath', ".//div[contains(@class, 'PopularRequestList-SearchText')]")
        )
        url = 'yandex.ru/images'
        assert url in browser.url
        allure.attach(f"Содержимое адресной строки браузера: {browser.url}", f"Проверка перехода на адрес {url}")
