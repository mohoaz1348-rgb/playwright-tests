import allure

from elements.input import Input
from tools.logger import get_logger

logger = get_logger("SLIDER")


class Slider(Input):
    @property
    def type_of(self) -> str:
        return "slider"

    def fill(self, value: str, nth: int = 0, **kwargs):
        step = f'Filling {self.type_of} "{self.name}" with value {value}'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            locator.evaluate(
                f"node => {{ node.value = '{value}'; node.dispatchEvent(new Event('change')); }}"
            )
