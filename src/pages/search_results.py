from stere import Page
from stere.areas import Area, RepeatingArea
from stere.fields import Button, Input, Link, Root, Text


class Search_Results(Page):
    def __init__(self):
        self.results = RepeatingArea(
            root=Root('xpath', "//li[contains(@class, 'serp-item')]"),
            title=Text('xpath', ".//span[contains(@class, 'organic__title')]"),
            link=Link('xpath', ".//a[contains(@class, 'path__item')]")
        )
        assert self.results.areas[0].title.is_visible

    def get_top_result(self):
        return self.results.areas[0]
