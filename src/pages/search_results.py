from typing import Union, T

import allure
from stere import Page
from stere.areas import RepeatingArea, Area, Repeating
from stere.fields import Button, Input, Link, Root, Text, Field

from src.common.common_elements import Search


class Image_Viewer(Area):
    def __init__(self, **kwargs: Union[Field, T, Repeating]):
        super().__init__(**kwargs)
        self.image_container = Area(
            next=Button('xpath', "//div[contains(@class, 'CircleButton_type_next')]"),
            prev=Button('xpath', "//div[contains(@class, 'CircleButton_type_prev')]"),
            image=Field('xpath', '//img[@class="MMImage-Origin"]')
        )


class Search_Results(Page):
    @allure.step('Перейти на страницу результатов поиска')
    def __init__(self, mode):
        self.search_form = Search(
            root=Root('xpath', "//form[@role='search']"),
            query=Input('xpath', ".//input[not(@type='hidden')]"),
            submit=Button('xpath', ".//button")
        )
        if mode == 'text':
            self.results = RepeatingArea(
                root=Root('xpath', "//li[contains(@class, 'serp-item')]"),
                title=Text('xpath', ".//span[contains(@class, 'organic__title')]"),
                link=Link('xpath', ".//a[contains(@class, 'path__item')]")
            )
        elif mode == 'image':
            self.results = RepeatingArea(
                root=Root('xpath', "//div[@role='listitem' and @data-grid-position]"),
                link=Link('xpath', ".//a")
            )
            self.mode = mode

    def get_top_result(self):
        return self.results.areas[0]

    def click_result(self, result):
        result.link.click()
        if self.mode == 'image':
            return Image_Viewer()

    # todo think of a way to assign methods to specific modes: this method is text-only
    @allure.step('Проверить, что ссылка в первом результате поиска содержит {1}')
    def assert_top_result_leads_to_site(self, site):
        top_result = self.get_top_result()
        top_result_link = top_result.link.element['href']
        assert site in top_result_link
        allure.attach(top_result_link, "Ссылка в первом результате поиска", allure.attachment_type.TEXT)
