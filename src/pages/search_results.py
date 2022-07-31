from typing import Union, T

import allure
from abc import ABC, abstractmethod
from stere.areas import RepeatingArea, Area, Repeating
from stere.fields import Button, Link, Root, Text, Field, Input

from src.common.common_elements import Search
from test.utils.api_utils import download_bytes
from test.utils.image_utils import compare_images


class Image_Viewer(Area):
    @allure.step("Кликнуть на картинку")
    def __init__(self, **kwargs: Union[Field, T, Repeating]):
        super().__init__(**kwargs)
        self.image_container = Area(
            next=Button('xpath', "//div[contains(@class, 'CircleButton_type_next')]"),
            prev=Button('xpath', "//div[contains(@class, 'CircleButton_type_prev')]"),
            image=Field('xpath', '//img[@class="MMImage-Origin"]')
        )
        assert self.image_container.image.is_visible, "Картинка не открылась после клика"

    def download_current_image(self):
        link = self.image_container.image.element['src']
        return download_bytes(link)

    @allure.step("Кликнуть на стрелку вправо")
    def next(self):
        self.image_container.next.click()

    @allure.step("Кликнуть на стрелку влево")
    def prev(self):
        self.image_container.prev.click()

    @allure.step("Сравнить текущую картинку с эталонной. Ожидаемый результат сравнения: {1}")
    def compare_images(self, should_equal, standard):
        current = self.download_current_image()
        equal = compare_images(standard, current)
        allure.attach(standard, "Эталонное изображение", allure.attachment_type.JPG)
        allure.attach(current, "Текущее изображение", allure.attachment_type.JPG)
        prefix = ''
        if should_equal:
            assert equal is True, "Текущая картинка не равна эталонной"
        else:
            prefix = 'не '
            assert equal is False, "Текущая картинка равна эталонной"
        allure.attach(f"Текущая картинка {prefix}равна эталонной", "Сравнение изображений", allure.attachment_type.TEXT)


class Search_Results(ABC):
    @allure.step('Перейти на страницу результатов поиска')
    def __init__(self):
        self.search_form = Search(
            root=Root('xpath', "//form[@role='search']"),
            query=Input('xpath', ".//input[not(@type='hidden')]"),
            submit=Button('xpath', ".//button")
        )
        self.results = None

    @abstractmethod
    def get_top_result(self):
        pass

    @abstractmethod
    def click_result(self, result):
        result.link.click()


class Image_Search_Results(Search_Results):
    def __init__(self):
        super().__init__()
        self.results = RepeatingArea(
            root=Root('xpath', "//div[@role='listitem' and @data-grid-position]"),
            link=Link('xpath', ".//a"),
            image=Field('xpath', ".//img")
        )

    def click_result(self, result):
        super(Image_Search_Results, self).click_result(result)
        return Image_Viewer()

    def get_top_result(self):
        top = self.results.areas[0]
        allure.attach(download_bytes(top.image.element['src']), "Выбран первый результат в выдаче")
        return top


class Text_Search_Results(Search_Results):
    def __init__(self):
        super().__init__()
        self.results = RepeatingArea(
            root=Root('xpath', "//li[contains(@class, 'serp-item')]"),
            title=Text('xpath', ".//span[contains(@class, 'organic__title')]"),
            link=Link('xpath', ".//a[contains(@class, 'path__item')]")
        )

    def get_top_result(self):
        top = self.results.areas[0]
        allure.attach(top.title.element.text, "Выбран первый результат в выдаче")
        return top

    def click_result(self, result):
        super(Text_Search_Results, self).click_result(result)

    @allure.step('Проверить, что ссылка в первом результате поиска содержит {1}')
    def assert_top_result_leads_to_site(self, site):
        top_result = self.get_top_result()
        top_result_link = top_result.link.element['href']
        assert site in top_result_link, f"Ссылка в первом результате поиска не содержит подстроку {site}"
        allure.attach(top_result_link, "Ссылка в первом результате поиска", allure.attachment_type.TEXT)
