import unittest

from htmlnode import *
from utils import *

class Test_Markdown_images_and_links(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")],matches)
    
    def test_split_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT, )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_links(self):
        node = TextNode( "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT, )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )
    
    def test_text_to_textnodes(self):
        node = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(node)
        self.assertListEqual([
                                TextNode("This is ", TextType.TEXT),
                                TextNode("text", TextType.BOLD),
                                TextNode(" with an ", TextType.TEXT),
                                TextNode("italic", TextType.ITALIC),
                                TextNode(" word and a ", TextType.TEXT),
                                TextNode("code block", TextType.CODE),
                                TextNode(" and an ", TextType.TEXT),
                                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                                TextNode(" and a ", TextType.TEXT),
                                TextNode("link", TextType.LINK, "https://boot.dev"),
                            ],new_nodes)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_headings_level1(self):
        text = "# Here is a Heading 1"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.heading, block_type)

    def test_headings_level2(self):
        text = "## Here is a Heading 2"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.heading, block_type)

    def test_headings_level3(self):
        text = "### Here is a Heading 3"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.heading, block_type)

    def test_headings_level4(self):
        text = "#### Here is a Heading 4"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.heading, block_type)

    def test_headings_level5(self):
        text = "##### Here is a Heading 5"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.heading, block_type)

    def test_headings_level6(self):
        text = "###### Here is a Heading 6"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.heading, block_type)

    def test_paragraph(self):
        text = "Here is a Heading 6"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.paragraph, block_type)

    def test_code(self):
        text = "```Here is a Heading 6```"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.code, block_type)
    
    def test_quote(self):
        text = "> Here is a Heading"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.quote, block_type)

    def test_unordered_list_simple(self):
        text = "- Here is a Heading"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.unordered_list, block_type)

    def test_unordered_list_multi(self):
        text = """- Here is a Heading
- One More Heading"""
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.unordered_list, block_type)
    
    def test_ordered_list_simple(self):
        text = "1. Here is a Heading"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.ordered_list, block_type)

    def test_ordered_list_multi(self):
        text = """1. Here is a Heading
2. One More Heading"""
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.ordered_list, block_type)