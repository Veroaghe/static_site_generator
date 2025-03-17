from textnode import TextNode, TextType
from htmlnode import LeafNode

def main():
    node = TextNode("This is some anchor text", TextType.BOLD, "https://www.boot.dev")
    leaf_node = text_node_to_html_node(node)
    print(leaf_node.to_html())


def text_node_to_html_node(text_node):
    if text_node is None:
        raise Exception("invalid text_node")

    text = text_node.text
    
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, value=text)
        case TextType.BOLD:
            return LeafNode("b", text)
        case TextType.ITALIC:
            return LeafNode("i", text)
        case TextType.CODE:
            return LeafNode("code", text)
        case TextType.LINK:
            return LeafNode("a", text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url, "alt":text})

main()