import allure
from stere import Page
from stere.areas import Area, RepeatingArea
from stere.fields import Button, Input, Link, Root, Text


class Search_Results(Page):
    @allure.step('Перейти на страницу результатов поиска')
    def __init__(self):
        self.results = RepeatingArea(
            root=Root('xpath', "//li[contains(@class, 'serp-item')]"),
            title=Text('xpath', ".//span[contains(@class, 'organic__title')]"),
            link=Link('xpath', ".//a[contains(@class, 'path__item')]")
        )
        assert self.results.areas[0].title.is_visible

    def get_top_result(self):
        return self.results.areas[0]

    @allure.step('Проверить, что ссылка в первом результате поиска содержит {1}')
    def assert_top_result_leads_to_site(self, site):
        top_result = self.get_top_result()
        top_result_link = top_result.link.element['href']
        assert site in top_result_link
        allure.attach(top_result_link, "Ссылка в первом результате поиска", allure.attachment_type.TEXT)
