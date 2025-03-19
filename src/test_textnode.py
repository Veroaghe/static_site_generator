import unittest

from textnode import TextNode, TextType
from main import text_node_to_html_node, split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_not_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_not_eq3(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        node2 = TextNode("This isn't the same text", TextType.BOLD, "https://boot.dev")
        self.assertNotEqual(node, node2)


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
    

class Test_SplitNodesDelimiter(unittest.TestCase):
    def test1(self):
        node = TextNode("`This` is text with a code block `word`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes[0].text, "This")
        self.assertEqual(new_nodes[0].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text, " is text with a code block ")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, "word")
        self.assertEqual(new_nodes[2].text_type, TextType.CODE)
    
    def test_ExceptionRaisedOnInvalidMarkdown(self):
        test_cases = [
            "`This` is text with a code block `word `",
            "`This ` is text with a code block `word`",
            "`This` is text with a code block ` word`",
            "` This` is text with a code block `word`",
            "`This` is text with ` a code block `word`",
        ]
        for test in test_cases:
            node = TextNode(test, TextType.TEXT)
            self.assertRaises(Exception, split_nodes_delimiter, [node], "`", TextType.CODE)
    
    def test_UnusedDelimiter(self):
        node = TextNode("`This` is text with a code block `word`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
    
    def test_DifferentDelimeters(self):
        test_text = "**Here**'s `a` _text_ **using** `different` _types_ `of` *delimeters*."
        test_cases = [
            ("**", TextType.BOLD, 4),
            ("_", TextType.ITALIC, 5),
            ("`", TextType.CODE, 7),
        ]
        for delim, text_type, result in test_cases:
            node = TextNode(test_text, TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], delim, text_type)
            self.assertEqual(len(new_nodes), result)
    
    def test_MultiplePasses(self):
        test_text = "**Here**'s `a` _text_ **using** `different` _types_ `of` *delimeters*."
        test_cases = [
            ("**", TextType.BOLD),
            ("_", TextType.ITALIC),
            ("`", TextType.CODE),
        ]

        nodes = [TextNode(test_text, TextType.TEXT)]
        for delim, text_type in test_cases:
            nodes = split_nodes_delimiter(nodes, delim, text_type)

        self.assertEqual(len(nodes), 14)
    
    def test_EmptyString(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node])


if __name__ == "__main__":
    unittest.main()