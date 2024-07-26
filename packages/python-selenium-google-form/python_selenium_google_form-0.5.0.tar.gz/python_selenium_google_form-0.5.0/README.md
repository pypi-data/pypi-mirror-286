# Introduction

The Python Selenium Google Form package is used to automate the completion of Google Forms. This package uses the Google Chrome browser.

## Installing

If you have pip on your system, you can simply install or upgrade the Python bindings:

```bash
    pip install python-selenium-google-form
```

Alternately, you can download the source distribution from PyPI <https://pypi.org/project/python-selenium-google-form/#files>, unarchive it, and run:

```bash
    python setup.py install
```

## Using

To use this package you should create Selenium driver and navigate to target Google Form. You can do it like me. I have 2 useful functions to simplify it:

```python
import undetected_chromedriver as uc

def get_driver(options: list) -> uc.Chrome:
    """
    Creating driver with settings
    :param options: uc.ChromeOptions
    :return: uc.Chrome
    """

    if options:
        driver_options: uc.ChromeOptions = uc.ChromeOptions()

        for option in options:
            driver_options.add_argument(option)

        return uc.Chrome(options=driver_options)

    else:
        return uc.Chrome()


def get_page(url: str, driver: uc.Chrome) -> None:
    """
    Loading page
    :param url: str
    :param driver: uc.Chrome
    :return: None
    """

    driver.get(url)
```

Using these functions and current package you can automate the completion of Google Forms. For example:

```python
from time import sleep
from typing import List

from python_selenium_google_form import process_form_fields_with_hotkeys, FieldConfig, FieldType

from selenium_methods import get_driver, get_page

WEB_DRIVER_OPTIONS = ["--start-maximized", "--disable-popup-blocking"]


def main() -> None:
    driver = get_driver(WEB_DRIVER_OPTIONS)
    driver.implicitly_wait(10)

    get_page(
        "https://docs.google.com/forms/d/e/1FAIpQLSfP0lcoj1XrdXtKCSwSkCaPEgGaGkY267U6yLCH3WkIz-58vg/viewform",
        driver)

    fields_list: List[FieldConfig] = [
        FieldConfig("first_name", FieldType.TEXT, "John"),
        FieldConfig("last_name", FieldType.TEXT, "Doe"),
        FieldConfig("job_title", FieldType.TEXT, "Software Developer"),
        FieldConfig("education_level", FieldType.RADIO, [1, 0, 0]),  # 1 means that field is selected, 0 - not selected
        FieldConfig("favourite_subjects", FieldType.CHECKBOX, [0, 0, 1, 1, 0]),  # 1 means that field is selected, 0 - not selected
        FieldConfig("experience", FieldType.SELECT, [0, 0, 1, 0]),  # 1 means that field is selected, 0 - not selected
        FieldConfig("date", FieldType.DATE, "01-09-2022"),
    ]

    process_form_fields_with_hotkeys(fields_list, driver)

    sleep(10)


main()
```
