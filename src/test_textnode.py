import unittest

from textnode import TextNode, TextType
from main import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from main import split_nodes_image, split_nodes_link

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


class test_LinkImageExtractors(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertListEqual(expected, matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(expected, matches)
    
    def test_combination_extraction(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev), an image ![rick roll](https://i.imgur.com/aKaOqIh.gif), another link [to youtube](https://www.youtube.com/@bootdotdev) and another ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        expected_images = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        links = extract_markdown_links(text)
        expected_links = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(expected_links, links)
        self.assertListEqual(expected_images, images)
    
    def test_empty_links(self):
        text = "empty link []()"
        matches = extract_markdown_links(text)
        expected = [('','')]
        self.assertListEqual(expected, matches)
    
    def test_empty_images(self):
        text = "empty link ![]()"
        matches = extract_markdown_images(text)
        expected = [('','')]
        self.assertListEqual(expected, matches)
    
    def test_no_links(self):
        text = "empty link ![]() and normal image ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        matches = extract_markdown_links(text)
        expected = []
        self.assertListEqual(expected, matches)
    
    def test_no_images(self):
        text = "empty link []() and normal link [to boot dev](https://www.boot.dev)"
        matches = extract_markdown_images(text)
        expected = []
        self.assertListEqual(expected, matches)
    
    def test_no_extra_square_brackets_allowed(self):
        test_cases = [
            ("[[to boot dev](https://www.boot.dev)", [('to boot dev', 'https://www.boot.dev')]),
            "[[to boot dev]](https://www.boot.dev)",
            "[to boot dev]](https://www.boot.dev)",
            "[to boot dev]((https://www.boot.dev)",
            "[to boot dev]((https://www.boot.dev))",
            ("[to boot dev](https://www.boot.dev))", [('to boot dev', 'https://www.boot.dev')]),
            "[to boot[] dev](https://www.boot.dev)",
            "[to boot dev](https://www.(boot).dev)",
        ]
        for test in test_cases:
            if isinstance(test, tuple):
                test, expected = test
            else:
                expected = []
            match = extract_markdown_links(test)
            self.assertEqual(match, expected)


class test_LinkAndImageSplitters(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text, [url](https://i.imgur.com/zjjcJKZ.png) [second url](https://i.imgur.com/3elNhQu.png), booya!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text, ", TextType.TEXT),
                TextNode("url", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" ", TextType.TEXT),
                TextNode(
                    "second url", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(", booya!", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_back_to_back_links(self):
        node = TextNode(
            "[url](https://i.imgur.com/zjjcJKZ.png)[second url](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("url", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second url", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_mixed_links(self):
        node = TextNode(
            "[url](https://i.imgur.com/zjjcJKZ.png)![second url](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        new_nodes = split_nodes_image(new_nodes)
        self.assertListEqual(
            [
                TextNode("url", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second url", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_repeated_links(self):
        node = TextNode(
            "[url](https://i.imgur.com/zjjcJKZ.png)[url](https://i.imgur.com/zjjcJKZ.png)![second url](https://i.imgur.com/3elNhQu.png)[url](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        new_nodes = split_nodes_image(new_nodes)
        self.assertListEqual(
            [
                TextNode("url", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("url", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second url", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("url", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )
    
    def test_empty_nodes(self):
        new_nodes = split_nodes_link([])
        new_nodes = split_nodes_image(new_nodes)
        self.assertListEqual(
            [],
            new_nodes,
        )
    
    def test_non_text_nodes(self):
        node = TextNode(
            "[url](https://i.imgur.com/zjjcJKZ.png)[url](https://i.imgur.com/zjjcJKZ.png)![second url](https://i.imgur.com/3elNhQu.png)[url](https://i.imgur.com/zjjcJKZ.png)",
            TextType.BOLD,
        )
        node2 = TextNode(
            "[url](https://i.imgur.com/zjjcJKZ.png)[url](https://i.imgur.com/zjjcJKZ.png)![second url](https://i.imgur.com/3elNhQu.png)[url](https://i.imgur.com/zjjcJKZ.png)",
            TextType.ITALIC,
        )
        new_nodes = split_nodes_link([node, node2])
        new_nodes = split_nodes_image(new_nodes)
        self.assertListEqual(
            [node, node2],
            new_nodes,
        )
    
    def test_empty_string(self):
        node = TextNode(
            "",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        new_nodes = split_nodes_image(new_nodes)
        self.assertListEqual(
            [node],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()