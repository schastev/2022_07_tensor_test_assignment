import allure


@allure.step("Закрыть окно браузера с названием {2}")
def close_window(browser, window_name, title):
    init_length = len(browser.windows)
    browser.windows[window_name].close()
    assert len(browser.windows) == init_length - 1
