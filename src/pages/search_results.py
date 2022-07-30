import io
from typing import Union, T

import allure
from stere import Page
from stere.areas import RepeatingArea, Area, Repeating
from stere.fields import Button, Input, Link, Root, Text, Field
from test.utils.api_utils import download_bytes
from PIL import Image

from src.common.common_elements import Search


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
    def compare_images(self, should_equal, other_image):
        current_image = self.download_current_image()
        allure.attach(other_image, "Эталонное изображение", allure.attachment_type.JPG)
        allure.attach(current_image, "Текущее изображение", allure.attachment_type.JPG)
        current = Image.open(io.BytesIO(current_image)).convert('RGB')
        other = Image.open(io.BytesIO(other_image)).convert('RGB')
        if other.size > current.size:
            other = other.resize(current.size)
        elif other.size < current.size:
            current = current.resize(other.size)
        equal = list(current.getdata()) == list(other.getdata())
        prefix = ''
        if should_equal:
            assert equal is True, "Текущая картинка не равна эталонной"
        else:
            prefix = 'не '
            assert equal is False, "Текущая картинка равна эталонной"
        allure.attach(f"Текущая картинка {prefix}равна эталонной", "Сравнение изображений", allure.attachment_type.TEXT)


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
        assert site in top_result_link, f"Ссылка в первом результате поиска не содержит подстроку {site}"
        allure.attach(top_result_link, "Ссылка в первом результате поиска", allure.attachment_type.TEXT)
