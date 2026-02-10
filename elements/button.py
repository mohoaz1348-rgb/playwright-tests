from elements.base_element import BaseElement

class Button(BaseElement):
    @property
    def type_of(self) -> str:
        return "button"
