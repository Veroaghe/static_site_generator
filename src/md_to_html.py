
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


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    # print([block], block_type) #TEST

    match block_type:
        case BlockType.PARAGRAPH:
            child_nodes = text_to_children(block)
            return ParentNode("p", child_nodes)

        case BlockType.HEADING:
            heading_num = len(block.split()[0]) # a number from 1 to 6, already validated by block_to_block_type
            text = block[heading_num + 1:]
            child_nodes = text_to_children(text)
            return ParentNode(f"h{heading_num}", child_nodes)

        case BlockType.CODE:
            # To represent multiple lines of code, wrap the <code> element within a <pre> element.
            # The <code> element by itself only represents a single phrase of code or line of code.
            lines = block.strip().split("\n")
            lines = [line for line in lines if line != ""]
            text = "\n".join(lines[1:-1]) + "\n"
            text_node = TextNode(text, TextType.CODE)
            children = [text_node_to_html_node(text_node)]
            return ParentNode("pre", children)

        case BlockType.QUOTE:
            lines = block.split("\n")
            new_lines = [line[1:].strip() for line in lines]
            text = "\n".join(new_lines)
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


if __name__ == "__main__":
    text = """
        ```python
        def is_this_a_valid_code_block():
            while True:
                break
            return True

        def another_function():
            return
        ```
        """
    
    print(markdown_to_html_node(text).children[0].children[0].value)