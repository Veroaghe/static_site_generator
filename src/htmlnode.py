

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        if value is None and children is None:
            raise Exception("objects needs either a value or children assigned")
        if tag is None:
            tag = "p"

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