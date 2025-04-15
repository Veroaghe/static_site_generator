# import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6


class BlockTypeError(Exception):
    def __init__(self, block, msg="Block has no block_type"):
        self.block = block
        self.msg = msg
        super().__init__(self, msg)
    
    def __str__(self):
        return f'''
    {self.msg}
    Input: {[self.block]}'''


def markdown_to_blocks(text): # BOOT.DEV Code
    blocks = text.split("\n\n")

    new_blocks = []
    stalled_blocks = [] # My Addition
    open_code_block = False # My Addition

    for block in blocks:
        if block == "":
            continue
        
        block = block.strip()

        ### Start check for multi-segmented code block ###
        if open_code_block:
            stalled_blocks.append(block)
            if block.endswith('```'):
                block = "\n\n".join(stalled_blocks)
                open_code_block = False

        if block.startswith('```') and not block.endswith('```') and not open_code_block:
            open_code_block = True
            stalled_blocks.append(block)
        ### End check for multi-segmented code block ###

        if not open_code_block:
            new_blocks.append(block)
    
    return new_blocks


def block_to_block_type(block): # BOOT.DEV Code
    if block == "" or block is None: # Except for these 2 lines
        raise BlockTypeError(block)

    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


if __name__ == "__main__":
    text = """
- Test
- test
    - indent
    - indent
- unindent
        """
    
    output = markdown_to_blocks(text)
    print()
    print(output, block_to_block_type(output[0]))
    print()
    [print(out) for out in output]
    # print()
    print(text)

