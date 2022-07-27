from splinter import Browser
from selenium.webdriver.common.keys import Keys

# https://github.com/cobrateam/splinter/blob/master/samples/test_google_search.py


def test_search():
    browser = Browser("chrome")
    browser.visit("http://www.yandex.ru")
    search_bar = browser.find_by_xpath("//form[@role='search']//input[not(@type='hidden')]").first
    assert search_bar.visible
    search_bar.click()
    search_bar.fill("Тензор")
    suggestions = browser.find_by_xpath("//li[contains(@id, 'suggest-item-') and @role='option' and @data-type='fulltext']")
    assert suggestions.visible
    search_bar.type(Keys.ENTER)
    results = browser.find_by_xpath('//ul[@id="search-result"]')
    assert results.visible
    top_result = browser.find_by_xpath("//li[contains(@class, 'serp-item')]").first
    assert top_result.links.find_by_href("https://tensor.ru/")
    browser.quit()

