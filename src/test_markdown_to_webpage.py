import unittest

from markdown_to_webpage import *



class Test_extract_title(unittest.TestCase):

    def test_simple_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_title_with_extra_spaces(self):
        self.assertEqual(extract_title("#   Hello World  "), "Hello World")

    def test_first_title_among_other_text(self):
        md = "Some intro text\n# My Title\nMore text"
        self.assertEqual(extract_title(md), "My Title")

    def test_multiple_titles_returns_first(self):
        md = "# First Title\n\n# Second Title"
        self.assertEqual(extract_title(md), "First Title")

    def test_subheader_not_matched(self):
        md = "## Subtitle\n### Sub-subtitle"
        with self.assertRaises(Exception) as ctx:
            extract_title(md)
        self.assertEqual(str(ctx.exception), "NO TITLE DEFINED")

    def test_no_title_raises_exception(self):
        md = "Just some plain text\nWithout a title"
        with self.assertRaises(Exception) as ctx:
            extract_title(md)
        self.assertEqual(str(ctx.exception), "NO TITLE DEFINED")

    def test_title_without_space_not_recognized(self):
        md = "#TitleWithoutSpace"
        with self.assertRaises(Exception):
            extract_title(md)