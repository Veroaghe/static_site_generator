# To indent lists in HTML, the indented list needs to be a child of an <li> tag


from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType


class InvalidTextNodeError(Exception):
    def __init__(self, node, msg="Invalid input: needs to be an instance of TextNode"):
        self.node = node
        self.msg = msg
        super().__init__(self, msg)
    
    def __str__(self):
        return f'''
        {self.msg}
        Input: {[self.node]}'''


class UnsupportedBlockTypeError(Exception):
    def __init__(self, block_type, msg="Unsupported block_type:"):
        self.block_type = block_type
        self.msg = msg
        super().__init__(self, msg)
    
    def __str__(self):
        return f'''
    {self.msg}
    Input: {[self.block_type]}
    Supported BlockTypes: {list(BlockType)}'''


def text_node_to_html_node(text_node):
    if text_node is None or not isinstance(text_node, TextNode):
        raise InvalidTextNodeError(text_node)

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


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)
    pass


def block_to_html_node(block):
    block_type = block_to_block_type(block)

    match block_type:
        case BlockType.PARAGRAPH:
            lines = block.split("\n")
            paragraph = " ".join(lines) # \n are converted into space for HTML
            child_nodes = text_to_children(paragraph)
            return ParentNode("p", child_nodes)

        case BlockType.HEADING:
            heading_num = len(block.split()[0])
            text = block[heading_num + 1:]
            child_nodes = text_to_children(text)
            return ParentNode(f"h{heading_num}", child_nodes)

        case BlockType.CODE:
            # To represent multiple lines of code, wrap the <code> element within a <pre> element.
            # The <code> element by itself only represents a single phrase of code or line of code.
            if not block.startswith("```") or not block.endswith("```"):
                raise ValueError("invalid code block")
            text = "\n".join(block.split("\n")[1:])[:-3] # Removes first line entirely (because there might be a language identifier after the opening ```)
            raw_text_node = TextNode(text, TextType.TEXT)
            child = text_node_to_html_node(raw_text_node)
            code = ParentNode("code", [child])
            return ParentNode("pre", [code])

        case BlockType.QUOTE:
            lines = block.split("\n")
            new_lines = [line[1:].strip() for line in lines]
            text = " ".join(new_lines) # \n are converted into space for HTML
            children = text_to_children(text)
            return ParentNode("blockquote", children)

        case BlockType.UNORDERED_LIST:
            li_nodes = block_to_list_of_li_nodes(block)
            return ParentNode("ul", li_nodes)

        case BlockType.ORDERED_LIST:
            li_nodes = block_to_list_of_li_nodes(block)
            return ParentNode("ol", li_nodes)

        case _:
            raise UnsupportedBlockTypeError(block_type)


def text_to_children(text):
    '''
    Convert a text into a list of textnodes.
    Convert each textnode into an HTMLNode.
    Return the list of HTMLNodes
    '''
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]


def block_to_list_of_li_nodes(block):
    '''
    - Splits block into lines
    - removes the bullet or number of each line
    - converts each line in a list of HTMLNodes
        - is passed as children to a ParentNode with li tag
    - li ParentNodes are gathered in a list, li_nodes.

    Returns a list of these li_nodes,
    '''
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        split_line = line.split()
        new_line = " ".join(split_line[1:])
        children = text_to_children(new_line)
        li_nodes.append(ParentNode("li", children))
    return li_nodes


if __name__ == "__main__":
    text = """
- test
- test
- test
"""
    
    print(markdown_to_html_node(text))