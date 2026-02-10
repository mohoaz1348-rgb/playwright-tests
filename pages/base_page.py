from typing import Pattern
import allure

from playwright.sync_api import Response, expect, Page
from tools.logger import get_logger

logger = get_logger("BASE_PAGE")


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def visit(self, url: str) -> None | Response:
        step = f'Opening the URL - "{url}"'
        with allure.step(step):
            logger.info(step)
            # self.page.goto(url, wait_until="networkidle")
            return self.page.goto(url)

    def reload(self):
        step = f'Reloading page with URL - "{self.page.url}"'
        with allure.step(step):
            logger.info(step)
            self.page.reload(wait_until="domcontentloaded")

    def check_current_url(self, expected_url: Pattern[str]):
        step = f'Checking that current url matches pattern "{expected_url.pattern}"'

        with allure.step(step):
            logger.info(step)
            expect(self.page).to_have_url(expected_url)

    def drag_and_drop(self, loc1: str, loc2: str):
        step = f'Checking that elements with locators "{loc1}", "{loc2}" are draggable'
        with allure.step(step):
            logger.info(step)
            e1 = self.page.locator(loc1)
            expect(e1).to_have_attribute("draggable", "true")
            e2 = self.page.locator(loc2)
            expect(e2).to_have_attribute("draggable", "true")

        step = f'Dragging element with locator "{loc1}" to the element with locator "{loc2}"'

        with allure.step(step):
            logger.info(step)
            self.page.drag_and_drop(loc1, loc2)
