from stere import Page
from stere.areas import Area, RepeatingArea
from stere.fields import Button, Input, Link, Root, Text
from src.pages.search_results import Search_Results

navigation = RepeatingArea(
    root=Root('xpath', "//li[@class= 'services-new__list-item']"),
    title=Text('xpath', ".//div[@class= 'services-new__item-title']"),
    link=Link('xpath', ".//a")
)


class Home_Page(Page):
    def __init__(self):
        self.search_form = Area(
            root=Root('xpath', "//form[@role='search']"),
            query=Input('xpath', ".//input[not(@type='hidden')]"),
            submit=Button('xpath', ".//button")
        )
        self.suggestions = RepeatingArea(
            root=Root('xpath', "//li[contains(@class, 'mini-suggest__item')]"),
            link=Link('xpath', './span')
        )
        self.top_bar = navigation

    def click_search_bar(self):
        search_form = self.search_form.root.element
        assert search_form.visible
        search_form.click()

    def search(self, search_query):
        self.search_form.perform(search_query)
        return Search_Results()

    def click_navigation(self, section, close_prev_window, browser):
        window_name = browser.windows.current.name
        element = self.top_bar.areas.containing("title", section)[0].link
        href = element.element['href']
        assert element.is_visible
        element.click()
        if close_prev_window:
            assert len(browser.windows) == 2
            browser.windows[window_name].close()
            assert len(browser.windows) == 1
        assert browser.url == href
        # not exactly what I'm being asked here,
        # but I'm trying to make the method immediately reusable,
        # and I can't do that without specifying addresses for each nav section, which is uncool
