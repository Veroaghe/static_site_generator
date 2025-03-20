
import re
from textnode import TextNode, TextType

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


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:

        text = node.text
        image_extraction = extract_markdown_images(text)

        if node.text_type is not TextType.TEXT or text == "" or image_extraction == []:
            new_nodes.append(node)
            continue
        
        start_index = 0

        for alt, url in image_extraction:
            image_index = text.find(f"![{alt}]({url})", start_index)
            if start_index != image_index:
                new_nodes.append(TextNode(text[start_index:image_index], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            start_index = image_index + len(f"![{alt}]({url})")

        if start_index != len(text):
            new_nodes.append(TextNode(text[start_index:], TextType.TEXT))
    
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:

        text = node.text
        link_extraction = extract_markdown_links(text)

        if node.text_type is not TextType.TEXT or text == "" or link_extraction == []:
            new_nodes.append(node)
            continue
        
        start_index = 0

        for alt, url in link_extraction:
            link_index = text.find(f"[{alt}]({url})", start_index)
            if start_index != link_index:
                new_nodes.append(TextNode(text[start_index:link_index], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, url))
            start_index = link_index + len(f"[{alt}]({url})")

        if start_index != len(text):
            new_nodes.append(TextNode(text[start_index:], TextType.TEXT))
    
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    delims = [("`", TextType.CODE), ("**", TextType.BOLD), ("_", TextType.ITALIC)]

    for delim, text_type in delims:
        nodes = split_nodes_delimiter(nodes, delim, text_type)
    
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


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