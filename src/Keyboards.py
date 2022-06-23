import json
import typing

class InlineKeyboardMarkup:
    def __init__(self) -> None:
        self.components: list[list[dict[str, typing.Any]]] = [[]]

    def addButton(self, button_content: dict[str, typing.Any]) -> None:
        self.components[0].append(button_content)

    @property
    def buttons(self) -> list[dict[str, typing.Any]]:
        return self.components[0]

    def getButtonsAsString(self) -> str:
        if self.buttons:
            return json.dumps(self.buttons)
        return ""


if __name__ == "__main__":
    kb = InlineKeyboardMarkup()

    kb.addButton({"text": "Action 1", "url": "http://mail.ru"})
    kb.addButton({"text": "Action 2", "callbackData": "call_back_id_2", "style": "attention"})
    
    print(kb.buttons)

    print(kb.getButtonsAsString())
