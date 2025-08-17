import unittest

from htmlnode import *
from utils import *

class Test_split_nodes_delimiter(unittest.TestCase):
    def test_text_in_html(self):
        node = TextNode("Text Test", TextType.TEXT,)
        html = textnode_to_html(node)
        return self.assertEqual(html,"<p>Text Test</p>")

    def test_bold_in_html(self):
        node = TextNode("Bold Test", TextType.BOLD,)
        html = textnode_to_html(node)
        return self.assertEqual(html,"<b>Bold Test</b>")
    
    def test_italic_in_html(self):
        node = TextNode("Italic Test", TextType.ITALIC,)
        html = textnode_to_html(node)
        return self.assertEqual(html,"<i>Italic Test</i>")

    def test_code_in_html(self):
        node = TextNode("Code Test", TextType.CODE,)
        html = textnode_to_html(node)
        return self.assertEqual(html,"<code>Code Test</code>")

    def test_link_in_html(self):
        node = TextNode("Link Test", TextType.LINK,"www.google.com")
        html = textnode_to_html(node)
        return self.assertEqual(html,'<a href="www.google.com">Link Test</a>')

    def test_image_in_html(self):
        node = TextNode("Image Test", TextType.IMAGE,"www.google.com")
        html = textnode_to_html(node)
        return self.assertEqual(html,'<img src="www.google.com" alt="Image Test">')