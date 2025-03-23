import unittest
from page_generation_utils import *

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md ="""
# This is the title

## This is a header that's not the title

And this is just a paragraph"""
        self.assertEqual(extract_title(md), "This is the title")

    def test_extract_title_after_line(self):
        md = """
We wrote something above it, but

# This is the title"""
        self.assertEqual(extract_title(md), "This is the title")
    
    def test_extract_title_no_title(self):
        md = """
This is a markdown file
Without a title"""
        with self.assertRaises(Exception):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()