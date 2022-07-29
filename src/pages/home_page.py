from typing import Union, T

import allure
from stere import Page
from stere.areas import Area, RepeatingArea, Repeating
from stere.fields import Button, Input, Link, Root, Text, Field
import test.utils.browser_utils as utils


class Navigation(RepeatingArea):
    def __init__(self, root: Field, **kwargs: Union[Field, Area]):
        super().__init__(root, **kwargs)

    @allure.step('Кликнуть на ссылку на раздел "{1}" на панели навигации в верхней части страницы')
    def click_navigation(self, section, close_prev_window, browser):
        window_name = browser.windows.current.name
        element = self.areas.containing("title", section)[0].link
        assert element.is_visible
        allure.attach("Ссылка отображается", f"Проверка отображения ссылки на раздел {section}")
        element.click()
        if close_prev_window:
            utils.close_window(browser, window_name, browser.title)


class Search(Area):
    def __init__(self, **kwargs: Union[Field, T, Repeating]):
        super().__init__(**kwargs)
        self.query = kwargs.get('query')
        self.submit = kwargs.get('submit')

    @allure.step('Начать поиск')
    def submit(self):
        self.submit().perform()

    @allure.step('Ввести "{1}" в строку поиска')
    def input_query(self, query):
        assert self.query.is_visible
        allure.attach("Строка поиска отображается",
                      "Проверить отображение строки поиска",
                      allure.attachment_type.TEXT)
        self.query.fill(query)
        return Suggestions(
            root=Root('xpath', "//li[contains(@class, 'mini-suggest__item')]"),
            link=Link('xpath', './span'))


class Suggestions(RepeatingArea):
    def __init__(self, root: Field, **kwargs: Union[Field, Area]):
        super().__init__(root, **kwargs)
        assert self.areas[0].link.is_visible
        allure.attach("Предложения отображаются",
                      "Проверка отображения поисковых предложений",
                      allure.attachment_type.TEXT)


class Home_Page(Page):
    @allure.step('Перейти на главную страницу Яндекса')
    def __init__(self):
        self.search_form = Search(
            root=Root('xpath', "//form[@role='search']"),
            query=Input('xpath', ".//input[not(@type='hidden')]"),
            submit=Button('xpath', ".//button")
        )
        self.navigation = Navigation(
            root=Root('xpath', "//li[@class='services-new__list-item']"),
            title=Text('xpath', ".//div[@class= 'services-new__item-title']"),
            link=Link('xpath', ".//a")
        )
