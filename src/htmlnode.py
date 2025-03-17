from functools import reduce

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        # if value is None and children is None:
        #     raise Exception("node objects need either a value or children assigned")

        self.tag = tag # str; HTML tag (e.g. "p", "h1", "a", ...)
        self.value = value # string representing the value of the HTML tag
        self.children = children  # list; HTMLNode objects representing the children of this node
        self.props = props # dict; optional attributes


    def to_html(self):
        raise NotImplementedError


    def props_to_html(self):
        if self.props is None:
            return None
        
        attributes = ""
        for prop in self.props:
            attributes += f' {prop}="{self.props[prop]}"'

        return attributes


    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"



class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    

    def to_html(self):
        if self.value is None:
            raise ValueError("A LeafNode must have a value string")

        if self.tag is None:
            return self.value
        
        attributes = ""
        if self.props is not None:
            attributes = self.props_to_html()
        
        return f"<{self.tag}{attributes}>{self.value}</{self.tag}>"
    

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.children}, {self.props})"



class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        # print(self.children)


    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode requires a tag")
        
        if self.children is None:
            raise ValueError("ParentNode requires a list of child node objects")
        
        attributes = ""
        if self.props is not None:
            attributes = self.props_to_html()
        
        return f'<{self.tag}{attributes}>{reduce(lambda current_result, node: current_result + node.to_html(), self.children, "")}</{self.tag}>'
    

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.value}, {self.children}, {self.props})"
