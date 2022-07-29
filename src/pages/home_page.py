import allure
from stere import Page
from stere.fields import Button, Input, Link, Root, Text
from src.common.common_elements import Navigation, Search


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
