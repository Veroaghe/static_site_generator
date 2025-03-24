import unittest

from textnode import TextNode, TextType
from md_to_html import text_node_to_html_node, markdown_to_html_node

class Test_TextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
    
    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")
    
    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
    
    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.image.url")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src":"https://www.image.url", "alt":"This is an image"})
    
    def test_link(self):
        node = TextNode("This is an image", TextType.LINK, "https://www.some.url")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is an image")
        self.assertEqual(html_node.props, {"href":"https://www.some.url"})


class Test_MarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_unordered_list(self):
        md = """
- Line 1
- Line 2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><ul><li>Line 1</li><li>Line 2</li></ul></div>",
            )
    
    def test_ordered_list(self):
        md = """
1. Line 1
2. Line 2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><ol><li>Line 1</li><li>Line 2</li></ol></div>",
            )
    
    def test_lists_with_inline_markdown(self):
        md = """
1. Line 1 **bold**
2. Line 2 _italic_

- Line 3 `code`
- Line 4 _italic_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        # <pl>placeholder</pl>

        self.assertEqual(
            html,
            "<div><ol><li>Line 1 <b>bold</b></li><li>Line 2 <i>italic</i></li></ol><ul><li>Line 3 <code>code</code></li><li>Line 4 <i>italic</i></li></ul></div>",
            )

    def test_blockquote(self):
        md = """
>This is a **bold** quote
> This is _italic_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><blockquote>This is a <b>bold</b> quote This is <i>italic</i></blockquote></div>",
            )


if __name__ == "__main__":
    unittest.main()