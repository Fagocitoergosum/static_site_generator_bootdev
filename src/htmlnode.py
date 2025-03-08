class HtmlNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        result=""
        if self.props:
            for attribute in self.props.keys():
                result=f'{result} {attribute}="{self.props[attribute]}"'
        return result
    
    def __repr__(self):
        return f"htmlnode.HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HtmlNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if not self.value and self.tag != "img":
            raise ValueError
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    

class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError
        if not self.children:
            raise ValueError(f"ParentNode {self.__repr__()} is not allowed to not have children")
        html_string=f"<{self.tag}{self.props_to_html()}>"
        for child_node in self.children:
            html_string += child_node.to_html()
        html_string += f"</{self.tag}>"
        return html_string