import allure
from elements.base_element import BaseElement
from playwright.sync_api import expect
from tools.logger import get_logger

logger = get_logger("IMAGE")


class Image(BaseElement):
    @property
    def type_of(self) -> str:
        return "image"

    def check_visible(self, nth: int = 0, **kwargs):
        step = f'Checking that {self.type_of} "{self.name}" is visible'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            expect(locator).to_be_visible()
            # Проверяем, что картинка не "битая"
            is_loaded = locator.evaluate(
                "node => node.complete && node.naturalWidth > 0"
            )
            assert (
                is_loaded is True
            ), "Файл картинки не найден или не может быть отрисован"
