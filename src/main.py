
import re
from textnode import TextNode, TextType
from htmlnode import LeafNode

def main():
    pass


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

            
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT or node.text == "":
            new_nodes.append(node)
            continue

        text = node.text
        start_index = 0

        while True: 
            opening = text.find(delimiter, start_index)

            if opening == -1:
                if start_index == 0:
                    new_nodes.append(node)
                else:
                    new_nodes.append(TextNode(text[start_index:], node.text_type))
                break

            closing = text.find(delimiter, opening + len(delimiter))
            text_block = text[opening+len(delimiter):closing]

            if closing == -1 or len(text_block) != len(text_block.strip()):
                raise Exception(f"Invalid Markdown Syntax detected\nin:\n   {node.text}\nat:\n   {delimiter}{text_block}{delimiter}")

            if start_index != opening:
                new_nodes.append(TextNode(text[start_index:opening], node.text_type))
            
            new_nodes.append(TextNode(text_block, text_type))

            start_index = closing + len(delimiter)
            if start_index == len(text):
                break

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"""(?<!!) # negative lookbehind for an exclamation mark
                          \[ # escaped opening bracket
                          ([^\[\]]*) # group that includes any character except for brackets
                          \]\( # escaped closing bracket and escaped opening parentheses, back-to-back
                          ([^\(\)]*) # group that includes any character except for parentheses
                          \) # escaped closing parentheses
                          """, text, re.VERBOSE)


if __name__ == "__main__":
    main()