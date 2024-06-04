class HTMLNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list = None,
        props: dict = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""

        props_html = ""

        for key, value in self.props.items():
            props_html += f' {key}="{value}"'

        return props_html.strip()

    def __repr__(self):
        return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"


class LeafNode(HTMLNode):
    def __init__(self, tag: str = None, value: str = None, props: dict = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node requires a value")

        if self.tag is None:
            return self.value

        output = f"<{self.tag}"

        if self.props is not None:
            output += f" {self.props_to_html()}"

        return f"{output}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children, props: dict = None):
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag cannot be None")

        if self.children is None or len(self.children) == 0:
            raise ValueError("Must have at least one child")

        output = f"<{self.tag}"

        if self.props is not None:
            output += f" {self.props_to_html()}"

        output += ">"

        for child in self.children:
            output += child.to_html()

        return output + f"</{self.tag}>"
