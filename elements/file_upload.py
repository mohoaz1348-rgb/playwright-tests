from elements.base_element import BaseElement
import allure
from tools.logger import get_logger

logger = get_logger("UPLOAD")


class UploadFile(BaseElement):
    @property
    def type_of(self) -> str:
        return "file uploader"

    def upload_file(self, file_path: str, nth: int = 0, **kwargs):
        step = f'Uploading file "{file_path}" ...'

        with allure.step(step):
            logger.info(step)
            locator = self.get_locator(nth, **kwargs)
            locator.set_input_files(file_path)
