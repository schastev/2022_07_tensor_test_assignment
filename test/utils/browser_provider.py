from splinter import Browser
from test.utils.config_utils import local_browser


def get_browser():

    if local_browser():
        return Browser("chrome")
    else:
        capabilities = {
            "browserName": "chrome",
            "browserVersion": "103.0",
            "selenoid:options": {
                "enableVideo": False,
                "enableVNC": True,
                "enableLog": True,
                "screenResolution": "1600x900x24"
            }
        }
        return Browser(driver_name="remote",
                       command_executor="http://localhost:4444/wd/hub",
                       desired_capabilities=capabilities)
