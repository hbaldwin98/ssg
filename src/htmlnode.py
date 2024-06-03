class HTMLNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list = None,
        props: dict = None
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ''

        props_html = ''

        for key, value in self.props.items():
            props_html += f' {key}="{value}"'

        return props_html.strip()

    def __repr__(self):
        output = ''
        output += f'Tag: {self.tag}\nValue: {self.value}'

        if self.children is not None:
            output += '\nChildren:\n'
            for child in self.children:
                print(child)

        if self.props is not None:
            output += '\nProps:'
            for key, value in self.props.items():
                output += f'\n{key}: {value}\n'

        return output


class LeafNode(HTMLNode):
    def __init__(self,
                 tag: str = None,
                 value: str = None,
                 props: dict = None
                 ):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError('Leaf node requires a value')

        if self.tag is None:
            return self.value

        output = f'<{self.tag}'

        if self.props is not None:
            output += f' {self.props_to_html()}'

        return f'{output}>{self.value}</{self.tag}>'
