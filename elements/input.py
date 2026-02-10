import allure

from playwright.sync_api import expect

from elements.base_element import BaseElement
from tools.logger import get_logger

logger = get_logger("INPUT")


class Input(BaseElement):
    @property
    def type_of(self) -> str:
        return "input"

    def fill(self, value: str, nth: int = 0, **kwargs):
        step = f'Filling {self.type_of} "{self.name}" with value {value}'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            locator.fill(value)

    def check_have_value(self, value: str, nth: int = 0, **kwargs):
        step = f'Checking that {self.type_of} "{self.name}" have the value "{value}"'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            expect(locator).to_have_value(value)
