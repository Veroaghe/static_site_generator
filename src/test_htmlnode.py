import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class Test_HTMLNode(unittest.TestCase):
    node1 = HTMLNode("a", "Learn Back-end dev here.", props={"href":"https://boot.dev", "target":"_blank"})
    node2 = HTMLNode(value="no tag test")

    def test_props_to_html(self):
        node1_attributes = self.node1.props_to_html()
        expected_outcome = ' href="https://boot.dev" target="_blank"'
        self.assertTrue(node1_attributes == expected_outcome)
    
    def test_node_is_HTMLNode(self):
        self.assertIsInstance(self.node1, HTMLNode)

    # def test_exception_on_missing_value_and_children(self):
    #     # HTMLNode needs either a value or a list of children; otherwise an Exception is raised
    #     # By default, all HTMLNode arguments are None
    #     self.assertRaises(Exception, HTMLNode)
    
    def test_representation(self):
        expr = "HTMLNode(" in self.node1.__repr__()
        self.assertTrue(expr)
    

class Test_LeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Learn back-end dev here.", props={"href":"https://boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev">Learn back-end dev here.</a>')
    
    def test_leaf_value_error(self):
        self.assertRaises(ValueError, LeafNode(None, None).to_html)
    
    def test_leaf_raw_text(self):
        node = LeafNode(None, "This should be printed raw.")
        self.assertEqual(node.to_html(), "This should be printed raw.")


class Test_ParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_multiple_grandchildren(self):
        grandchild_node1 = LeafNode("b", "grandchild_1")
        grandchild_node2 = LeafNode("i", "grandchild_2")
        child_node = ParentNode("span", [grandchild_node1, grandchild_node2])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild_1</b><i>grandchild_2</i></span></div>",
        )
    
    def test_to_html_double_child_nodes(self):
        grandchild_node1 = LeafNode("b", "grandchild_1")
        grandchild_node2 = LeafNode("i", "grandchild_2")
        child_node = ParentNode("span", [grandchild_node1, grandchild_node2])
        parent_node = ParentNode("div", [child_node, child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild_1</b><i>grandchild_2</i></span><span><b>grandchild_1</b><i>grandchild_2</i></span></div>",
        )
    
    def test_parentnode_no_tag_error(self):
        grandchild_node1 = LeafNode("b", "grandchild_1")
        grandchild_node2 = LeafNode("i", "grandchild_2")
        child_node = ParentNode("span", [grandchild_node1, grandchild_node2])
        parent_node = ParentNode(None, [child_node, child_node])
        self.assertRaises(ValueError, parent_node.to_html)
    
    def test_parentnode_no_children_error(self):
        parent_node = ParentNode("div", None)
        self.assertRaises(ValueError, parent_node.to_html)