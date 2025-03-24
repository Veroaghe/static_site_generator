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


# def markdown_to_blocks(text): # MY CODE
#     blocks = text.split("\n\n")
#     # blocks = [re.sub(r"\s*\n\s*", "\n", block.strip()) for block in blocks if block != "" and block.strip()[:3] != "```"]

#     reformatted_blocks = []
#     for block in blocks:
#         stripped_block = block.lstrip()

#         if stripped_block[:3] == "```":
#             removable_space = len(block) - len(stripped_block) - 1
#             split_block = block.split("\n")
#             new_block = [split_block[0]] + [line[removable_space:] for line in split_block[1:-1]] + [split_block[-1].strip()]
#             block = "\n".join(new_block)
#             # print([block]) #TEST
#             reformatted_blocks.append(block)
#             continue

#         if block.strip() == "":
#             continue

#         reformatted_blocks.append(re.sub(r"\s*\n\s*", "\n", block.strip()))

    
#     return reformatted_blocks


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


# def block_to_block_type(block): # MY CODE
#     if block == "" or block is None:
#         raise BlockTypeError(block)

#     lines = block.strip().split("\n")
#     lines = [line for line in lines if line != ""]
#     # print(lines) #TEST
#     if len(lines) > 1:
#         if lines[0][0:2] == "- ": # testing for unordered list
#             for line in lines:
#                 if line[0:2] != "- ":
#                     return BlockType.PARAGRAPH
#             return BlockType.UNORDERED_LIST

#         elif lines[0][0] == ">": # testing for quotes
#             for line in lines:
#                 if line[0] != ">":
#                     return BlockType.PARAGRAPH
#             return BlockType.QUOTE

#         elif len(lines) >= 3 and lines[0][:3] == lines[-1].strip() == '```':
#                 return BlockType.CODE

#         else: # testing for ordered list
#             check = 1
#             for line in lines:
#                 split_line = line.split(".")
#                 try:
#                     num = int(split_line[0])
#                     if num != check or split_line[1][0] != " ":
#                         raise
#                     check += 1
#                 except:
#                     return BlockType.PARAGRAPH
#             return BlockType.ORDERED_LIST

#     split_block = block.split()
#     heading = split_block[0]
#     heading_length = len(split_block[0])
#     if heading == "#" * heading_length and 1 <= heading_length <= 6 and len(split_block) >= 2:
#         return BlockType.HEADING
    
#     return BlockType.PARAGRAPH


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
        ```python
        def is_this_a_valid_code_block():
            while True:
                break
            return True
        
        def another_function():
            return
        ```
        """
    
    output = markdown_to_blocks(text)
    print()
    print(output, block_to_block_type(output[0]))
    print()
    [print(out) for out in output]
    # print()
    print(text)

