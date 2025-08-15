import unittest

from htmlnode import *
from utils import *

class Test_split_nodes_delimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)]
        self.assertEqual(new_nodes,expected)

    def test_bold(self):
        node = TextNode("This is text with a **code block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.BOLD), TextNode(" word", TextType.TEXT)]
        self.assertEqual(new_nodes,expected)

    def test_italic(self):
        node = TextNode("This is text with a _code block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.ITALIC), TextNode(" word", TextType.TEXT)]
        self.assertEqual(new_nodes,expected)