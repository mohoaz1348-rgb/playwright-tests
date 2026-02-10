import string
import re
import allure
from typing import List
from spellchecker import SpellChecker

from playwright.sync_api import Page, Locator, expect
from tools.logger import get_logger

logger = get_logger("BASE_ELEMENT")


class BaseElement:
    def __init__(self, page: Page, locator: str, name: str) -> None:
        self.page = page
        self.locator = locator
        self.name = name

    @property
    def type_of(self) -> str:
        return "base element"

    def get_locator(self, nth: int = 0, **kwargs) -> Locator:
        locator = self.locator.format(**kwargs)
        step = f'Getting locator with "{locator}" for {self.type_of} at index {nth}'

        with allure.step(step):
            logger.info(step)
            return self.page.locator(locator).nth(nth)

    def get_locators(self, **kwargs) -> Locator:
        locator = self.locator.format(**kwargs)
        step = f'Getting locator with "{locator}" for {self.type_of}'

        with allure.step(step):
            logger.info(step)
            return self.page.locator(locator)

    def click(self, nth: int = 0, **kwargs):
        step = f'Clicking {self.type_of} with name "{self.name}"'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            locator.click()

    def hover(self, nth: int = 0, **kwargs):
        step = f'Hover {self.type_of} with name "{self.name}"'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            locator.hover()

    def check_visible(self, nth: int = 0, **kwargs):
        step = f'Checking that {self.type_of} "{self.name}" is visible'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            expect(locator).to_be_visible()

    def check_have_text(self, text: str, nth: int = 0, **kwargs):
        step = f'Checking that {self.type_of} "{self.name}" have text "{text}"'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            expect(locator).to_have_text(text)

    def check_contain_text(self, text: str, nth: int = 0, **kwargs):
        step = f'Checking that {self.type_of} "{self.name}" contain text "{text}"'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            expect(locator).to_contain_text(text)
    
    def check_have_texts(self, texts: List[str], **kwargs):
        step = f'Checking that {self.type_of} "{self.name}" have texts "{texts}"'

        with allure.step(step):
            locator = self.get_locators(**kwargs)
            logger.info(step)
            expect(locator).to_have_text(texts)

    def to_have_count(self, count: int, **kwargs):
        step = f'Checking that {self.type_of} "{self.name}" exists on page in quantity "{count}"'

        with allure.step(step):
            logger.info(step)
            expect(self.get_locators(**kwargs)).to_have_count(count)

    def drag_to(self, dest_locator: Locator, nth: int = 0, **kwargs):
        step = f'Dragging {self.type_of} "{self.name}" to the element with locator "{str(dest_locator)}"'

        with allure.step(step):
            logger.info(step)
            locator = self.get_locator(nth, **kwargs)
            locator.drag_to(dest_locator)

    def check_hidden(self, nth: int = 0, **kwargs):
        step = f'Checking that {self.type_of} "{self.name}" is hidden'

        with allure.step(step):
            logger.info(step)
            locator = self.get_locator(nth, **kwargs)
            expect(locator).to_be_hidden()

    def check_response_after_click(self, response: int, nth: int = 0, **kwargs):
        step = f'Checking that response after click on {self.type_of} "{self.name}" is "{str(response)}"'

        with allure.step(step):
            logger.info(step)
            with self.page.expect_navigation() as info:
                self.click(nth, **kwargs)
            msg = f"Ожидали {str(response)}, а получили {info.value.status}"
            assert info.value.status == response, msg

    def check_spell(self, nth: int = 0, **kwargs):
        step = f'Spell checking text of {self.type_of} "{self.name}"'

        with allure.step(step):
            logger.info(step)
            # 1. Извлекаем весь видимый текст
            text = self.get_locator(nth, **kwargs).inner_text()
            print(text)

            raw_words = text.split()
            # Разрешенные знаки в начале слова
            allowed_start = "([{'«„" 
            # Разрешенные знаки в конце слова
            allowed_end = ".,!?;:)]}'»“"

            spell = SpellChecker(language='en')  # или 'ru'
            misspelled : List[str] = []

            for word in raw_words:
                # 1. Проверяем "прилипшие" знаки в начале
                if word[0] in string.punctuation and word[0] not in allowed_start:
                    print(f"Ошибка пунктуации: знак '{word[0]}' в начале слова '{word}'")
                    misspelled.append(word)

                # 2. Чистим слово ТОЛЬКО для проверки орфографии
                clean_word = word.strip(string.punctuation + "«»„“")
                
                # 3. Проверяем само слово в словаре
                if clean_word and not spell.known([clean_word.lower()]):
                    print(f"Опечатка в слове: {clean_word}")
                    misspelled.append(clean_word)

            assert not misspelled, f"Найдено {len(misspelled)} опечаток: {misspelled}"
