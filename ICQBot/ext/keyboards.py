import json
from .util import CustomDict


class Button(CustomDict):
    def __init__(self, **kwargs):
        self.data = kwargs


class InlineKeyboardMarkup:
    """
    Inline Keyboard Markup
    Calls an callback when pressed
    Supports Rows and Columns
    """
    def __init__(self) -> None:
        self.components: list[list[Button]] = [[]]

    def addButton(self, button_content: Button, row=0) -> None:
        """
        Adds a button to the grid
        :param button_content: a dict containing the button content (like: {"text": "Hello world", "callbackData": "id_1"})
        :param row: the row where the button will be added
        """
        self.components[row].append(button_content)

    def addRow(self) -> None:
        """
        Creates a new row
        """
        self.components.append([])

    def getRowsLen(self) -> int:
        return len(self.components)

    def _printRows(self):
        """
        For test only
        See how the buttons are ordered
        """
        for x in self.components:
            print("---------------------")
            for y in x:
                print("|", end="")
                print(y['text'], end="|")
            print()

    @property
    def buttons(self) -> list[list[Button]]:
        """
        Get all the buttons
        """
        return self.components

    def getButtonsAsString(self) -> str:
        """
        Dumps buttons to string
        """
        if self.buttons[0]:
            dict_buttons = []
            for x in self.buttons:
                dict_buttons.append([y.data for y in x])
            _json = json.dumps(dict_buttons)
            return _json
        return ""


if __name__ == "__main__":
    ...