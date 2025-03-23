import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6


def markdown_to_blocks(text):
    blocks = text.split("\n\n")
    # blocks = [re.sub(r"\s*\n\s*", "\n", block.strip()) for block in blocks if block != "" and block.strip()[:3] != "```"]

    reformatted_blocks = []
    for block in blocks:
        block = block.strip()

        if block[:3] == "```":
            split_block = block.split("\n")
            split_block[-1] = split_block[-1].strip()
            block = "\n".join(split_block)
            reformatted_blocks.append(block)
            continue

        if block == "":
            continue

        reformatted_blocks.append(re.sub(r"\s*\n\s*", "\n", block.strip()))

    
    return reformatted_blocks


def block_to_block_type(block):
    lines = block.split("\n")
    if len(lines) > 1:
        if lines[0][0:2] == "- ": # testing for unordered list
            for line in lines:
                if line[0:2] != "- ":
                    return BlockType.PARAGRAPH
            return BlockType.UNORDERED_LIST

        elif lines[0][0] == ">": # testing for quotes
            for line in lines:
                if line[0] != ">":
                    return BlockType.PARAGRAPH
            return BlockType.QUOTE

        elif len(lines) >= 3 and lines[0][:3] == lines[-1] == '```':
                return BlockType.CODE

        else: # testing for ordered list
            check = 1
            for line in lines:
                split_line = line.split(".")
                try:
                    num = int(split_line[0])
                    if num != check or split_line[1][0] != " ":
                        raise
                    check += 1
                except:
                    return BlockType.PARAGRAPH
            return BlockType.ORDERED_LIST
        # else:
        #     print(len(lines), lines, lines[0][:3] == lines[-1] == '```')
        #     if len(lines) >= 3 and lines[0][:3] == lines[-1] == '```':
        #         return BlockType.CODE

    split_block = block.split()
    heading = split_block[0]
    heading_length = len(split_block[0])
    if heading == "#" * heading_length and 1 <= heading_length <= 6 and len(split_block) >= 2:
        return BlockType.HEADING
    
    return BlockType.PARAGRAPH



if __name__ == "__main__":
    text = """
        ```python
        def is_this_a_valid_code_block():
            return True
        ```
        """
    
    output = markdown_to_blocks(text)
    print()
    print(output)
    print()
    [print([out], block_to_block_type(out)) for out in output]

    print("##    ".split())

