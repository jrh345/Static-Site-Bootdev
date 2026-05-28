from typing import Optional

class HTMLNode():
    def __init__(self,tag: Optional[str]=None,value: Optional[str]=None,children: Optional[list]=None,props: Optional[dict] = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ''

        out_string = ''
        for k, v in self.props.items():
            out_string += f' {k}="{v}"'
        return out_string

    def __repr__(self):
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False

        return (
                self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)



class LeafNode(HTMLNode):
    def __init__(self, tag, value, props: Optional[dict]=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None or self.value == '':
            raise ValueError('Leaf nodes must have a value')

        if self.tag is None:
            return str(self.value)

        attrs = self.props_to_html()
        return f"<{self.tag}{attrs}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag={self.tag!r}, value={self.value!r}, props={self.props!r})"
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props: Optional[dict]=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Must have a tag")
        if self.children is None:
            raise ValueError("Must have children")

        attrs = self.props_to_html()
        child_str = ''.join(child.to_html() for child in self.children)
        return f"<{self.tag}{attrs}>{child_str}</{self.tag}>"