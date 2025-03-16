from enum import Enum

class TextType(Enum):
    NORMAL_TEXT = 1
    BOLD_TEXT = 2
    ITALIC_TEXT = 3
    CODE_TEXT = 4
    PLAIN_LINK = 5
    IMAGE_LINK = 6

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"