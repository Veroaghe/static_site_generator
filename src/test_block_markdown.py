import unittest
from block_markdown import BlockType
from block_markdown import markdown_to_blocks, block_to_block_type


class Test_SplitBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
            md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )
    
    def test_excessive_newlines(self):
            md = """
        This is **bolded** paragraph



        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line



        - This is a list
        - with items
        """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )
    
    def test_empty_text(self):
        blocks = markdown_to_blocks("")
        self.assertEqual(blocks, [])
    
    def test_only_newlines(self):
        blocks = markdown_to_blocks("\n\n\n\n\n\n")
        self.assertEqual(blocks, [])
    
    def test_double_leading_trailing_newlines(self):
        blocks = markdown_to_blocks("\n\ntext here\n\nsome more text\n\n")
        self.assertEqual(blocks, ["text here", "some more text"])

    def test_single_leading_trailing_newlines(self):
        blocks = markdown_to_blocks("\ntext here\n\nsome more text\n")
        self.assertEqual(blocks, ["text here", "some more text"])
    
    def test_remove_spaces_around_single_newline_chars(self):
        blocks = markdown_to_blocks("\ntext here\n\nsome more text     \n     last text     \n     last text\n\n\nI lied before")
        self.assertEqual(blocks, ["text here", "some more text\nlast text\nlast text", "I lied before"])


class Test_BlockToBlocktype(unittest.TestCase):
    def test_multiple_block_variations(self):
        test_cases = [
            ("This is **bolded** paragraph", BlockType.PARAGRAPH), # 1. Normal text with inline markdown
            ("```code block```", BlockType.PARAGRAPH), # 2. Invalid codeblock, the backticks need to be on separate lines
            ("```\nnot a valid\n```\ncode block", BlockType.PARAGRAPH), # 3. code block can't contain trailing text
            ("code block\n```\nnot valid\n```", BlockType.PARAGRAPH), # 4. code block can't contain leading text
            ("```\ncode block\n```", BlockType.CODE), # 5. valid code block
            ("### Heading", BlockType.HEADING), # 6. valid heading
            ("This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line", BlockType.PARAGRAPH), # 7. multiline paragraph
            ("# 'nother heading", BlockType.HEADING), # 8. Another valid heading
            ("#tag, not a heading", BlockType.PARAGRAPH), # 9. Invalid Heading, no space between tag and text
            ("> some\n> quoting", BlockType.QUOTE), # 10. Valid quote with spaces after >
            (">a\n> valid\n>quote\n> block", BlockType.QUOTE), # 11. Valid quote with a mix of spaces or not after >
            (">a\n>valid\n>quote\n>block", BlockType.QUOTE), # 12. Valid quote with no spaces after >
            ("- This is a list\n- with items", BlockType.UNORDERED_LIST), # 13. valid unordered list
            ("- This is not a list\n- with items\n* because of with different bullets", BlockType.PARAGRAPH), # 14. invalid unordered list because of unsupported bullet
            ("- even with different bullets\n- even with different bullets\n- even with different bullets", BlockType.UNORDERED_LIST), # 15. valid unordered list
            ("- even with different bullets\n1. numbered", BlockType.PARAGRAPH), # 16. invalid mix of list_types
            ("- a bullet and\nnormal text", BlockType.PARAGRAPH), # 17. mix of list and normal
            ("normal text and\n- a bullet", BlockType.PARAGRAPH), # 18. mix of list and normal
            ("1. invalid\n10. numbered\n3. list", BlockType.PARAGRAPH), # 19. invalid numbered list: numbers need to increment by 1
            ("1. valid\n2. numbered\n3. list", BlockType.ORDERED_LIST), # 20. valid numbered list
            ("2. invalid\n3. numbered\n4. list", BlockType.PARAGRAPH), # 21. invalid numbered list: need to start at 1
            ("## ", BlockType.PARAGRAPH), # 22. Invalid Heading: no text after heading hashtags
            ("```python\ncode block\n```", BlockType.CODE),
            ('```python\n        def is_this_a_valid_code_block():\n            return True\n        ```', BlockType.PARAGRAPH),
            ('```python\n        def is_this_a_valid_code_block():\n            return True\n```', BlockType.CODE),
            ("placeholder", BlockType.PARAGRAPH),
        ]

        test_num = 0
        for block, expected in test_cases:
            test_num += 1
            block_type = block_to_block_type(block)
            self.assertEqual(block_type, expected, msg=f"\n\ntest_case {test_num}:\n\n{[block]}")

if __name__ == "main":
    unittest.main()