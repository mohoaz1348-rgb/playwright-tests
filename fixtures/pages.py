from typing import Generator
import uuid
import pytest
import allure
from playwright.sync_api import Playwright, Page, expect

from pages.base_page import BasePage
from config import Settings

CHROMIUM = "chromium"
FIREFOX = "firefox"
WEBKIT = "webkit"
ALL = "all"

# Список поддерживаемых браузеров
SUPPORTED_BROWSERS = [CHROMIUM, FIREFOX, WEBKIT]
BROWSERS_OPTION = "browsers"

def pytest_addoption(parser):
    parser.addoption(
        f"--{BROWSERS_OPTION}",
        action="store",
        default=CHROMIUM,
        help=f"Примеры: {CHROMIUM} | {FIREFOX},{WEBKIT} | {ALL}"
    )

def pytest_generate_tests(metafunc):
    fixture_name = "browser_page"

    if fixture_name in metafunc.fixturenames:
        raw_value = metafunc.config.getoption(BROWSERS_OPTION).lower()
        
        if raw_value == ALL:
            selected_browsers = SUPPORTED_BROWSERS
        else:
            selected_browsers = [b.strip() for b in raw_value.split(",")]
            
            # ВАЛИДАЦИЯ: проверяем каждое введенное слово
            for b in selected_browsers:
                if b not in SUPPORTED_BROWSERS:
                    # Выбрасываем ошибку Pytest с пояснением
                    pytest.exit(
                        f"\n Ошибка: Браузер '{b}' не поддерживается.\n"
                        f" Допустимые значения: {', '.join(SUPPORTED_BROWSERS)} или '{ALL}'"
                    )

        metafunc.parametrize(fixture_name, selected_browsers, indirect=True)

#@pytest.fixture(params=[CHROMIUM, FIREFOX])
@pytest.fixture
def browser_page(
    playwright: Playwright, settings: Settings, request
) -> Generator[Page, None, None]:
    expect.set_options(timeout=settings.expect_timeout)

    br = playwright.chromium
    if request.param == FIREFOX:
        br = playwright.firefox
    if request.param == WEBKIT:
        br = playwright.webkit

    browser = br.launch(headless=settings.headless)
    
    context = browser.new_context(
        base_url=f"{settings.app_url}", record_video_dir=settings.videos_dir
    )
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    # print(f"зашли в фикстуру - settings.headless = {settings.headless}")
    yield page

    tracing_file = settings.tracing_dir.joinpath(f"{uuid.uuid4()}.zip")
    context.tracing.stop(path=tracing_file)
    context.close()
    browser.close()

    allure.attach.file(tracing_file, name="trace", extension="zip")
    video = page.video
    if video:
        allure.attach.file(
            video.path(), name="video", attachment_type=allure.attachment_type.WEBM
        )


@pytest.fixture
def base_page(browser_page: Page) -> BasePage:
    return BasePage(page=browser_page)
