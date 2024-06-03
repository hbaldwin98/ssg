class TextNode:
    def __init__(self, text: str, text_type: str, url: str):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, o):
        return (self.text == o.text
                and self.text_type == o.text_type
                and self.url == o.url)

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'
