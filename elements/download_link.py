import os
import allure
from playwright.sync_api import Download, Page
from elements.base_element import BaseElement
from config import Settings
from tools.logger import get_logger

logger = get_logger("DOWNLOAD LINK")


class DownloadLink(BaseElement):
    def __init__(self, page: Page, locator: str, name: str) -> None:
        super().__init__(page, locator, name)
        self.dl: Download | None = None 
    
    @property
    def type_of(self) -> str:
        return "download link"

    def download(self, nth: int = 0, **kwarg):
        step = "Downloading file ..."
        with allure.step(step):
            logger.info(step)
            with self.page.expect_download() as download_info:
                self.click(nth, **kwarg)

            self.dl = download_info.value

        print(f"Имя файла: {self.dl.suggested_filename}")
        print(f"URL скачивания: {self.dl.url}")

        save_path = os.path.join(Settings().downloads_dir, self.dl.suggested_filename)
        self.dl.save_as(save_path)

        assert os.path.exists(save_path)
        assert os.path.getsize(save_path) > 0
