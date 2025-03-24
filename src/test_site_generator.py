import unittest
from gencontent import extract_title

class Test_TitleExtractor(unittest.TestCase):
    def test_title_found(self):
        out = extract_title("# Hello")
        self.assertEqual(out, "Hello")
    
    def test_multiple_md_lines(self):
        out = extract_title("## Hello\n# World")
        self.assertEqual(out, "World")
    
    def test_raise_exception(self):
        self.assertRaises(Exception, extract_title, "## Hello\n## World")


if __name__ == "__main__":
    unittest.main()