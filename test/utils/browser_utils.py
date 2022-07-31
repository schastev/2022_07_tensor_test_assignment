import allure
from stere import Stere

from test.utils.browser_provider import get_browser


@allure.step("Закрыть окно браузера с названием {2}")
def close_window(browser, window_name, title):
    init_length = len(browser.windows)
    browser.windows[window_name].close()
    assert len(browser.windows) == init_length - 1


def browser_setup():
    Stere.browser = get_browser()
    Stere.url_navigator = 'visit'
    Stere.base_url = "http://www.yandex.ru/"
