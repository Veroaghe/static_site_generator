import unittest
from htmlnode import HTMLNode

class Test_HTMLNode(unittest.TestCase):
    node1 = HTMLNode("a", "Learn Back-end dev here.", props={"href":"https://boot.dev", "target":"_blank"})
    node2 = HTMLNode(value="no tag test")

    def test_props_to_html(self):
        node1_attributes = self.node1.props_to_html()
        expected_outcome = ' href="https://boot.dev" target="_blank"'
        self.assertTrue(node1_attributes == expected_outcome)
    
    def test_node_is_HTMLNode(self):
        self.assertIsInstance(self.node1, HTMLNode)

    def test_exception_on_missing_value_and_children(self):
        # HTMLNode needs either a value or a list of children; otherwise an Exception is raised
        # By default, all HTMLNode arguments are None
        self.assertRaises(Exception, HTMLNode)
    
    def test_no_tag_input(self):
        # when no tag is given on node creation, default tag should be "p"
        self.assertTrue(self.node2.tag == "p")
    
    def test_representation(self):
        expr = "HTMLNode(" in self.node1.__repr__()
        self.assertTrue(expr)