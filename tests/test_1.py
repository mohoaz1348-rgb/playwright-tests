import re
import allure
import pytest

from elements.file_upload import UploadFile
from elements.image import Image
from elements.dropdown import Dropdown
from elements.checkbox import Checkbox
from elements.slider import Slider
from pages.base_page import BasePage
from elements.base_element import BaseElement
from elements.input import Input
from elements.button import Button
from elements.download_link import DownloadLink


@allure.title("add/remove elements")
def test_add_remove_elements(base_page: BasePage):
    base_page.visit("add_remove_elements/")
    add = Button(base_page.page, 'button[onclick="addElement()"]', "Add Element")
    add.click()
    delete = Button(base_page.page, "button.added-manually", "Delete")
    delete.check_visible(0)
    add.click()
    delete.check_visible(1)
    delete.to_have_count(2)
    delete.click(1)
    delete.to_have_count(1)
    delete.click(0)
    delete.to_have_count(0)


@allure.title("check images on page")
def test_images(base_page: BasePage):
    base_page.visit("broken_images")
    image = Image(base_page.page, "img", "some image")
    count = base_page.page.locator("img").count()
    i = 0
    while i < count:
        image.check_visible(i)
        i += 1


@allure.title("test checkboxes")
def test_checkboxes(base_page: BasePage):
    base_page.visit("checkboxes")
    checkbox = Checkbox(base_page.page, 'input[type="checkbox"]', "some checkbox")
    checkbox.check_visible(0)
    checkbox.not_to_be_checked(0)
    checkbox.check_visible(1)
    checkbox.to_be_checked(1)
    checkbox.click(0)
    checkbox.to_be_checked(0)
    checkbox.click(1)
    checkbox.not_to_be_checked(1)


@allure.title("drag and drop")
def test_drag_and_drop(base_page: BasePage):
    base_page.visit("drag_and_drop")
    a_element = BaseElement(base_page.page, "#column-a", "A-block")
    b_element = BaseElement(base_page.page, "#column-b", "B-block")
    a_element.check_have_text("A")
    b_element.check_have_text("B")
    # assert page.inner_text("#column-a header") == "A"
    # assert page.inner_text("#column-b header") == "B"
    # base_page.drag_and_drop("#column-a", "#column-b")
    a_element.drag_to(b_element.get_locator())
    a_element.check_have_text("B")
    b_element.check_have_text("A")


@allure.title("dropdown")
def test_dropdown(base_page: BasePage):
    base_page.visit("dropdown")
    dropdown = Dropdown(base_page.page, "select#dropdown", "Options")
    dropdown.select_option_by_value("1")
    dropdown.check_have_value("1")
    dropdown.check_number_of_options(3)
    dropdown.check_text_of_all_options(
        ["Please select an option", "Option 1", "Option 2"]
    )
    dropdown.check_for_duplicates()


def close_ad(base_page: BasePage):
    close = Button(base_page.page, "div.modal-footer p", "Close")
    close.click()
    modal_window = BaseElement(base_page.page, "div.modal", "Ad")
    modal_window.check_hidden()


@allure.title("modal window")
def test_modal_window(base_page: BasePage):
    base_page.visit("entry_ad")
    close_ad(base_page)


@allure.title("modal window")
def test_modal_window_2(base_page: BasePage):
    base_page.page.add_locator_handler(
        base_page.page.locator("div.modal"), lambda: close_ad(base_page)
    )
    base_page.visit("entry_ad")
    base_page.page.wait_for_timeout(2000)
    base_page.page.get_by_role("heading").click()


@allure.title("download")
def test_download_link(base_page: BasePage):
    base_page.visit("download")
    dl_link = DownloadLink(base_page.page, '//a[text()="test_upload.txt"]', "some link")
    # dl_link = DownloadLink(base_page.page, 'a[href="download/testfile.txt"]', "some link")
    dl_link.download()


@allure.title("upload")
def test_upload(base_page: BasePage):
    base_page.visit("upload")
    UPLOAD = "for_upload/test_upload.txt"
    UploadFile(base_page.page, "input#file-upload", "Upload").upload_file(UPLOAD)
    Button(base_page.page, "input#file-submit", "Upload").click()
    BaseElement(base_page.page, "div#uploaded-files", "Uploaded Files").check_visible()


@allure.title("slider")
def test_slider(base_page: BasePage):
    base_page.visit("horizontal_slider")
    slider = Slider(base_page.page, 'input[type="range"]', "Slider")
    slider.fill("3.5")
    slider.check_have_value("3.5")
    span = BaseElement(base_page.page, "span#range", "Span")
    span.check_have_text("3.5")
    max_value = slider.get_locator().get_attribute("max")
    base_page.page.wait_for_timeout(500)
    if max_value:
        slider.fill("5")
        slider.check_have_value("5")
    span.check_have_text("5")


@pytest.mark.parametrize("target_value", ["1", "2.5", "5"])
@allure.title("slider_params")
def test_slider_params(base_page: BasePage, target_value: str):
    base_page.visit("horizontal_slider")
    slider = Slider(base_page.page, 'input[type="range"]', "Slider")
    slider.fill(target_value)
    slider.check_have_value(target_value)
    span = BaseElement(base_page.page, "span#range", "Span")
    span.check_have_text(target_value)


@pytest.fixture(params=["1.5", "3", "4.5"])
def target_value(request):
    return request.param


@allure.title("slider_params")
def test_slider_params_by_fixture(base_page: BasePage, target_value):
    base_page.visit("horizontal_slider")
    slider = Slider(base_page.page, 'input[type="range"]', "Slider")
    slider.fill(target_value)
    slider.check_have_value(target_value)
    span = BaseElement(base_page.page, "span#range", "Span")
    span.check_have_text(target_value)


class LoginMsgs:
    SUCCESS = "You logged into a secure area!"
    WRONG_USER = "Your username is invalid!"
    WRONG_PASS = "Your password is invalid!"


@pytest.mark.parametrize(
    "login, pwd, msg",
    [
        ("tomsmith", "SuperSecretPassword!", LoginMsgs.SUCCESS),
        ("invalid_user", "12345", LoginMsgs.WRONG_USER),
        ("tomsmith", "nstnst", LoginMsgs.WRONG_PASS),
    ],
)
@allure.title("login")
def test_login(base_page: BasePage, login: str, pwd: str, msg: str):
    base_page.visit("login")

    username = Input(base_page.page, "input#username", "username")
    username.fill(login)
    username.check_have_value(login)
    password = Input(base_page.page, "input#password", "password")
    password.fill(pwd)
    password.check_have_value(pwd)
    submit = Button(base_page.page, 'button[type="submit"]', "login")
    submit.click()

    match msg:
        case LoginMsgs.SUCCESS:
            base_page.check_current_url(re.compile(".*/secure"))
            logout = Button(base_page.page, "a.button", "logout")
            logout.click()
            base_page.check_current_url(re.compile(".*/login"))

        case LoginMsgs.WRONG_USER:
            err_msg = BaseElement(base_page.page, "div.flash.error", "Error panel")
            err_msg.check_visible()
            err_msg.check_contain_text(LoginMsgs.WRONG_USER)

        case LoginMsgs.WRONG_PASS:
            err_msg = BaseElement(base_page.page, "div.flash.error", "Error panel")
            err_msg.check_visible()
            err_msg.check_contain_text(LoginMsgs.WRONG_PASS)


@allure.title("hover")
def test_hover(base_page: BasePage):
    base_page.visit("hovers")
    image = Image(base_page.page, "div.figure img", "some image")
    image.hover(1)
    link = BaseElement(base_page.page, "div.figcaption a", "some link")
    link.check_visible(1)
    link.check_hidden(0)
    link.check_hidden(2)
    link_href = link.get_locator(1).get_attribute("href")
    link.click(1)
    if link_href:
        base_page.check_current_url(re.compile(f".*{link_href}"))


@pytest.mark.debug
@allure.title("jquery menu")
def test_jquery_menu(base_page: BasePage):
    base_page.visit("jqueryui/menu")
    tpl = '//li[@class="ui-menu-item"]//a[text()="{name}"]'
    item = DownloadLink(base_page.page, tpl, "some item")
    item.hover(name="Enabled")
    item.check_visible(name="Downloads")
    item.hover(name="Downloads")
    item.check_visible(name="PDF")
    item.download(name="PDF")


def handle_confirm(dialog):
    print(f"Текст в окне: {dialog.message}")
    assert dialog.message == "I am a JS Confirm"
    dialog.dismiss()


@allure.title("alert_confirm_prompt")
def test_alert_confirm_prompt(base_page: BasePage):
    base_page.visit("javascript_alerts")
    tpl = '//button[contains(text(),"{name}")]'
    button = Button(base_page.page, tpl, "some button")
    result = BaseElement(base_page.page, "#result", "result")

    base_page.page.once("dialog", lambda dialog: dialog.accept())
    button.click(name="Alert")
    result.check_contain_text("success")

    base_page.page.once("dialog", handle_confirm)
    button.click(name="Confirm")
    result.check_contain_text("Cancel")

    base_page.page.once("dialog", lambda dialog: dialog.accept("Ahaha!"))
    button.click(name="Prompt")
    result.check_contain_text("Ahaha!")


@pytest.mark.parametrize("value", ["200", "301", "404", "500"])
@allure.title("http response after click")
def test_response_after_click(base_page: BasePage, value: str):
    response = base_page.visit("status_codes")
    assert response != None
    assert response.status == 200, f"Ожидали 200, а получили {response.status}"
    tpl = f'//a[text()="{value}"]'
    link = BaseElement(base_page.page, tpl, f"link with name {value}")
    link.check_response_after_click(int(value))


@pytest.mark.repeat(4)
@allure.title("spell_check")
def test_check_spell(base_page: BasePage):
    base_page.visit("typos")
    body = BaseElement(base_page.page, 'body', "body")
    body.check_spell()
