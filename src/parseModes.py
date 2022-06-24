import typing
import json


class GenericMarkup:
    def __init__(self, content: str) -> None:
        self.content = content

    @property
    def getContent(self) -> str:
        return self.content

    def __str__(self) -> str:
        return self.content

    def __repr__(self) -> str:
        return self.__str__()


class Markdown(GenericMarkup):
    def __init__(self, content: str) -> None:
        super().__init__(content)

    @staticmethod
    def default():
        return Markdown("MarkdownV2")


class HtmlMarkup(GenericMarkup):
    def __init__(self, content: str) -> None:
        super().__init__(content)


class Formatting:
    content = ""


if __name__ == "__main__":
    md = Markdown.default()
    print(md.content)
