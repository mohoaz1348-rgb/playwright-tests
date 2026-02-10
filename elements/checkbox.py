import allure
from elements.base_element import BaseElement
from playwright.sync_api import expect
from tools.logger import get_logger

logger = get_logger("CHECKBOX")


class Checkbox(BaseElement):
    @property
    def type_of(self) -> str:
        return "checkbox"

    def to_be_checked(self, nth: int = 0, **kwargs):
        step = f'Checking that {self.type_of} "{self.name}" is checked'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            expect(locator).to_be_checked()

    def not_to_be_checked(self, nth: int = 0, **kwargs):
        step = f'Checking that {self.type_of} "{self.name}" is checked'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            expect(locator).not_to_be_checked()
