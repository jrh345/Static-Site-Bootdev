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
        out_string = ''
        for i in self.props:
            out_string += f" {i.key}={i.value} "
        return out_string

    def __repr__(self):
        print(self.props_to_html)

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False

        return (
                self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)



class LeafNode(HTMLNode):
    def __init__(self,tag:[str]=None, value: [str]=None, props: Optional[dict]=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError

        if not self.tag:
            return str(self.value)

        return super().props_to_html()
    def __repr__(self):
        
