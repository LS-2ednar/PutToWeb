import unittest

from htmlnode import *
from utils import *

class Test_Markdown_to_html(unittest.TestCase):
    def test_paragraphs_1(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,"<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",)

    def test_paragraphs_2(self):
        md = """
This is _italic_ paragraph
_also this text is italic_ in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,"<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",)

        def test_paragraphs_3(self):
        md = """
This is _italic_ paragraph
_also this text is italic_ in a p
tag here. Did we mention this **bold** stuff here?

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,"<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here. Did we mention this <b>bold</b> stuff here?</p></div>",)