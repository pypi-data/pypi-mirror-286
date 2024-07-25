from enum import Enum
from time import sleep
from typing import List, Union

import undetected_chromedriver as uc
from selenium.webdriver import Keys
from selenium.webdriver.remote.webelement import WebElement


class FieldType(Enum):
    TEXT = "text"
    RADIO = "radio"
    CHECKBOX = "checkbox"
    SELECT = "select"
    DATE = "date"


class FieldConfig:
    def __init__(self, key: str, type: FieldType, value: Union[str, List[int]]):
        self.key = key
        self.type = type
        self.value = value


def get_active_element(driver: uc.Chrome) -> WebElement:
    """
    Get active element
    :param driver: uc.Chrome
    :return: WebElement
    """

    return driver.switch_to.active_element


def process_text_field(value: str, driver: uc.Chrome) -> None:
    """
    Process text field
    :param value:
    :param driver:
    :return: None
    """

    active_field = get_active_element(driver)
    active_field.send_keys(value)


def process_radio_buttons_field(value: List[int], driver: uc.Chrome) -> None:
    """
    Process radio buttons field
    :param value: List[int]
    :param driver: uc.Chrome
    :return: None
    """

    active_field = get_active_element(driver)

    for index, option_value in enumerate(value):
        if option_value == 1:
            if index == 0:
                active_field.send_keys(Keys.ARROW_DOWN)
                active_field = get_active_element(driver)
                active_field.send_keys(Keys.ARROW_UP)
        else:
            active_field.send_keys(Keys.ARROW_DOWN)

        if option_value == 1:
            active_field = get_active_element(driver)
            active_field.send_keys(Keys.TAB)
            break


def process_checkbox_field(value: List[int], driver: uc.Chrome) -> None:
    """
    Process checkbox field
    :param value: List[int]
    :param driver: uc.Chrome
    :return: None
    """

    variants_quantity = len(value)

    for index, option_value in enumerate(value):
        if option_value == 1:
            active_field = get_active_element(driver)
            active_field.send_keys(Keys.SPACE)

        if index < variants_quantity - 1:
            active_field = get_active_element(driver)
            active_field.send_keys(Keys.TAB)


def process_select_field(value: List[int], driver: uc.Chrome) -> None:
    """
    Process select field
    :param value: List[int]
    :param driver: uc.Chrome
    :return: None
    """

    active_field = get_active_element(driver)
    variants_quantity = len(value)

    active_field.send_keys(Keys.SPACE)
    active_field.send_keys(Keys.ARROW_DOWN)
    sleep(0.5)

    for index, option_value in enumerate(value):
        active_field = get_active_element(driver)

        if option_value == 1:
            active_field.send_keys(Keys.SPACE)
            break

        if index < variants_quantity - 1:
            active_field.send_keys(Keys.ARROW_DOWN)
            sleep(0.5)


def process_date_field(value: str, driver: uc.Chrome) -> None:
    """
    Process date field
    :param value: str
    :param driver: uc.Chrome
    :return: None
    """

    active_field = get_active_element(driver)
    active_field.send_keys(value)


def process_form_fields_with_hotkeys(fields_list: List[FieldConfig], driver: uc.Chrome) -> None:
    """
    Process form fields with hotkeys
    :param fields_list: List[FieldConfig]
    :param driver: uc.Chrome
    :return: None
    """

    # Example of fields_list
    #
    # fields_list: List[FieldConfig] = [
    #     FieldConfig("first_name", FieldType.TEXT, "John"),
    #     FieldConfig("last_name", FieldType.TEXT, "Doe"),
    #     FieldConfig("job_title", FieldType.TEXT, "Software Developer"),
    #     FieldConfig("education_level", FieldType.RADIO, [1, 0, 0]),
    #     FieldConfig("favourite_subjects", FieldType.CHECKBOX, [0, 0, 1, 1, 0]),
    #     FieldConfig("experience", FieldType.SELECT, [0, 0, 1, 0]),
    #     FieldConfig("date", FieldType.DATE, "01-09-2022"),
    # ]
    #
    # Example of form: https://docs.google.com/forms/d/e/1FAIpQLSfP0lcoj1XrdXtKCSwSkCaPEgGaGkY267U6yLCH3WkIz-58vg/viewform
    #
    # [
    #     {
    #         "field_type": FieldType.TEXT,
    #         "field_name": "First name",
    #     },
    #     {
    #         "field_type": FieldType.TEXT,
    #         "field_name": "Last name",
    #     },
    #     {
    #         "field_type": FieldType.TEXT,
    #         "field_name": "Job title",
    #     },
    #     {
    #         "field_type": FieldType.RADIO,
    #         "field_name": "Education level",
    #         "options": ["High school", "College", "University"],
    #     },
    #     {
    #         "field_type": FieldType.CHECKBOX,
    #         "field_name": "Favourite subjects",
    #         "options": ["English", "Maths", "Physics", "Chemistry", "Biology"],
    #     },
    #     {
    #         "field_type": FieldType.SELECT,
    #         "field_name": "Experience",
    #         "options": ["Less than 1 year", "1-3 years", "3-5 years", "More than 5 years"],
    #     },
    #     {
    #         "field_type": FieldType.DATE,
    #         "field_name": "Date",
    #     },
    # ]

    body = get_active_element(driver)

    body.send_keys(Keys.TAB)
    body.send_keys(Keys.TAB)
    body.send_keys(Keys.TAB)

    for field_config in fields_list:
        if field_config.type == FieldType.TEXT:
            process_text_field(field_config.value, driver)
        elif field_config.type == FieldType.RADIO:
            process_radio_buttons_field(field_config.value, driver)
        elif field_config.type == FieldType.CHECKBOX:
            process_checkbox_field(field_config.value, driver)
        elif field_config.type == FieldType.SELECT:
            process_select_field(field_config.value, driver)
        elif field_config.type == FieldType.DATE:
            process_date_field(field_config.value, driver)

        active_field = get_active_element(driver)
        sleep(0.1)
        active_field.send_keys(Keys.TAB)
        sleep(0.1)

    submit_button = get_active_element(driver)

    submit_button.click()
