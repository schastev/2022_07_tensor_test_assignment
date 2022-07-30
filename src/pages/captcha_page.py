from stere import Page
from stere.areas import Area
from stere.fields import Button


class Captcha_Page(Page):
    def __init__(self):
        self.form = Area(
            checkbox=Button('xpath', "//input[@class='CheckboxCaptcha-Button']")
        )

