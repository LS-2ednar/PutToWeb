import unittest

from htmlnode import *
from utils import *

class Test_Markdown_to_html(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
                html,
                "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
                html,
                "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


    def test_unordered_list_basic(self):
        md = """
- Item one
- Item two
- Item three
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item one</li><li>Item two</li><li>Item three</li></ul></div>",
        )

    def test_unordered_list_with_formatting(self):
        md = """
- **Bold** item
- Item with _italic_ text
- Item with a [link](https://example.com)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ul><li><b>Bold</b> item</li><li>Item with <i>italic</i> text</li><li>Item with a <a href="https://example.com">link</a></li></ul></div>',
        )

    def test_ordered_list_basic(self):
        md = """
1. First
2. Second
3. Third
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>",
        )

    def test_ordered_list_with_code_and_italic(self):
        md = """
1. Item with `code`
2. Item with _italic_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item with <code>code</code></li><li>Item with <i>italic</i></li></ol></div>",
        )

    def test_heading_h1(self):
        md = "# This is a heading 1"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>This is a heading 1</h1></div>")

    def test_heading_h3(self):
        md = "### This is a heading 3"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h3>This is a heading 3</h3></div>")

    def test_quote_basic(self):
        md = """
> This is a blockquote
> with multiple lines
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote with multiple lines</blockquote></div>",
        )

    def test_quote_with_formatting(self):
        md = """
> A quote with **bold**, _italic_, and `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>A quote with <b>bold</b>, <i>italic</i>, and <code>code</code></blockquote></div>",
        )