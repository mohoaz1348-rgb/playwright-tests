import allure
import collections
from typing import List
from elements.base_element import BaseElement
from playwright.sync_api import expect
from tools.logger import get_logger

logger = get_logger("DROPDOWN")


class Dropdown(BaseElement):
    @property
    def type_of(self) -> str:
        return "dropdown"

    def select_option_by_value(self, val: str, nth: int = 0, **kwargs):
        step = f'Selecting option with value "{val}" in {self.type_of} with name "{self.name}"'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            locator.select_option(value=val)

    def check_have_value(self, value: str, nth: int = 0, **kwargs):
        step = f'Checking that {self.type_of} "{self.name}" have the value "{value}"'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            expect(locator).to_have_value(value)

    def check_number_of_options(self, count: int, nth: int = 0, **kwargs):
        step = f'Checking that {self.type_of} "{self.name}" have "{count}" options'

        with allure.step(step):
            logger.info(step)
            locator = self.get_locator(nth, **kwargs).locator("option")
            expect(locator).to_have_count(count)

    def check_text_of_all_options(self, texts: List[str], nth: int = 0, **kwargs):
        step = f'Checking that {self.type_of} "{self.name}" have texts {texts}'
        with allure.step(step):
            logger.info(step)
            locator = self.get_locator(nth, **kwargs).locator("option")
            expect(locator).to_have_text(texts)

    def check_for_duplicates(self, nth: int = 0, **kwargs):
        step = f'Checking {self.type_of} "{self.name}" for duplicates'

        with allure.step(step):
            logger.info(step)
            all_options = (
                self.get_locator(nth, **kwargs).locator("option").all_inner_texts()
            )
            # Ищем элементы, которые встречаются больше одного раза
            duplicates = [
                item
                for item, count in collections.Counter(all_options).items()
                if count > 1
            ]

            assert (
                not duplicates
            ), f"Ошибка! Следующие значения повторяются: {', '.join(duplicates)}"
