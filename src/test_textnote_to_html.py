import unittest

from htmlnode import *
from utils import *

class Test_split_nodes_delimiter(unittest.TestCase):
    
    def test_plain_text(self):
        node = TextNode("Hello", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "Hello")

    def test_bold_text(self):
        node = TextNode("Bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b>Bold</b>")

    def test_italic_text(self):
        node = TextNode("Italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<i>Italic</i>")

    def test_inline_code(self):
        node = TextNode("x = 42", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<code>x = 42</code>")

    def test_link(self):
        node = TextNode("OpenAI", TextType.LINK, URL="https://openai.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            html_node.to_html(),
            '<a href="https://openai.com">OpenAI</a>'
        )

    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, URL="https://example.com/img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            html_node.to_html(),
            '<img src="https://example.com/img.png" alt="Alt text"></img>'
        )

    def test_invalid_type_raises(self):
        # Create a fake TextNode with unsupported type
        class FakeType:
            value = "fake"

        bad_node = TextNode("Bad", TextType.TEXT)  # start with normal
        bad_node.text_type = FakeType()  # monkey-patch to simulate bad type
        with self.assertRaises(Exception):
            text_node_to_html_node(bad_node)