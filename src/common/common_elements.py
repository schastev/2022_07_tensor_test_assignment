from typing import Union, T

import allure
from stere.areas import Area, RepeatingArea, Repeating
from stere.fields import Field, Root, Link
import test.utils.browser_utils as utils


class Navigation(RepeatingArea):
    def __init__(self, root: Field, **kwargs: Union[Field, Area]):
        super().__init__(root, **kwargs)

    @allure.step('Кликнуть на ссылку на раздел "{1}" на панели навигации в верхней части страницы')
    def click_navigation(self, section, close_prev_window, browser):
        window_name = browser.windows.current.name
        element = self.areas.containing("title", section)[0].link
        assert element.is_visible(3), f"Ссылка на раздел \"{section}\" не отображается"
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
        assert self.query.is_visible(3), "Строка поиска не отображается"
        self.query.fill(query)
        return Suggestions(
            root=Root('xpath', "//li[contains(@class, 'mini-suggest__item')]"),
            link=Link('xpath', './span'))

    def assert_query(self, query):
        assert self.query.element.value == query, f"Строка поиска не содержит \"{query}\""


class Suggestions(RepeatingArea):
    def __init__(self, root: Field, **kwargs: Union[Field, Area]):
        super().__init__(root, **kwargs)
        assert self.areas[0].link.is_visible(3), "Поисковые предложения не отображаются"
