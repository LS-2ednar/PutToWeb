from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, TEXT, TEXT_TYPE, URL=None):
        
        if not isinstance(TEXT, str):
            raise TypeError(f"Provided Text is not type string! Type: {type(TEXT)}")

        if isinstance(TEXT_TYPE,TextType):
            tt = TEXT_TYPE
        elif isinstance(TEXT_TYPE,"str"):
            try:
                tt = TextType(TEXT_TYPE.lower())
            except:
                raise ValueError(f"TEXT_TYPE for {TEXT_TYPE} does not exist")

        if not any(x.value == TEXT_TYPE.value for x in TextType):
            raise Exception(f"TextType {TEXT_TYPE} does not exist!")

        if URL:
            if not isinstance(URL, str):
                raise TypeError(f"Provided URL is not type string! Type: {type(URL)}")

        self.text = TEXT
        self.text_type = tt  
        self.url = URL

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return NotImplemented  # or: return False
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
       
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"