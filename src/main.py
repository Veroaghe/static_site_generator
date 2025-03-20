
from textnode import TextNode, TextType
from htmlnode import LeafNode
from inline_markdown import text_to_textnodes

def main():
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    nodes = text_to_textnodes(text)
    [print(node) for node in nodes]


def text_node_to_html_node(text_node):
    if text_node is None or not isinstance(text_node, TextNode):
        raise Exception("invalid node: needs to be an instance of TextNode")

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
        case _:
            raise Exception("text_node has an invalid text_type")


if __name__ == "__main__":
    main()